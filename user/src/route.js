const express = require("express");
const jwt = require("jsonwebtoken");
const sqlUtil = require("./tools/sqlUtil");
const redisTool = require("./tools/redisUtil");
const { SECRET_KEY } = require("../config");
const CACHE_KEY = "users";

const router = express.Router();

const generateToken = (info) => {
    try {
        // 生成Token，默认使用 HMAC SHA-256
        const token = jwt.sign(info, SECRET_KEY, { expiresIn: "8h" });
        return token;
    } catch (error) {
        throw error;
    }
};

const verifyToken = (request, response, next) => {
    const token = request.headers.authorization;

    if (!token) {
        return response.status(401).json({ message: "Unauthorized" });
    }

    jwt.verify(token, SECRET_KEY, (err, decoded) => {
        if (err) {
            return response.status(401).json({ message: "Invalid token" });
        }
        // 将token中的用户信息解析出来挂在request上
        request.userInfo = decoded;
        next();
    });
};

// 响应处理
const fullFilled = (response, data, pagination, code = 0) => {
    response.json({
        code,
        data,
        pagination,
        msg: "成功"
    });
};

// route异常处理
const errorHandler = (response, err) => {
    response &&
        response.status(500).json({
            code: 1,
            msg: err.toString()
        });
};

// 处理特定路径的路由
router.post("/login", async (request, response) => {
    try {
        const { username, password } = request.body;

        const sql = `SELECT id, name, username FROM user WHERE username = ? AND password = ?`;
        const user = await sqlUtil.execute(sql, [username, password]);
        if (!user || !user.length) {
            fullFilled(response, { msg: "用户名或密码错误" }, undefined, 1);
        } else {
            const { id, username } = user[0];
            const sql = `SELECT role.code as role, app.code as app FROM user_role
            LEFT JOIN user ON user.id = user_role.user_id
            LEFT JOIN app ON app.id = user_role.app_id
            LEFT JOIN role ON role.id = user_role.role_id
            WHERE user.id = ?`;
            const userRole = await sqlUtil.execute(sql, [id]);
            const roles = {};
            userRole.forEach((item) => (roles[item.app] = item.role));
            fullFilled(response, { token: generateToken({ id, username, roles }), userInfo: { ...user[0], roles } });
        }
    } catch (error) {
        console.info("error in login:", error);
        errorHandler(response, error);
    }
});

// 新增用户
router.post("/users", verifyToken, async (request, response) => {
    try {
        const { name, username, password, telephone, desc } = request.body;
        const sql =
            "INSERT INTO user(name, username, password, telephone, token, `desc`) VALUES(?, ?, ?, ?, ?, ?, ?)";
        const params = [name, username, password, telephone, desc];
        const value = await sqlUtil.execute(sql, params);
        // 成功后，直接删除 Redis 缓存中的数据，下次查询时会重新获取最新数据
        await redisTool.deleteKey(CACHE_KEY);
        fullFilled(response, value);
    } catch (error) {
        console.info("error in create users:", error);
        errorHandler(response, error);
    }
});

// 查询用户
router.get("/users/:id", verifyToken, (request, response) => {
    try {
        console.info(request.userInfo);
        const { id } = request.params;
        const sql = "SELECT id, name, username, telephone, `desc` FROM user WHERE id = ?";
        const query = sqlUtil.execute(sql, [id]);
        query.then(
            (value) => fullFilled(response, value),
            (error) => errorHandler(response, error)
        );
    } catch (error) {
        console.info("error in create users:", error);
        errorHandler(response, error);
    }
});

// 查询所有用户
router.get("/users", verifyToken, (request, response) => {
    try {
        const { pageSize, pageNo, keyword, orderField, orderSeq } = request.query;

        let sql = `SELECT id, name, username, telephone, \`desc\` FROM user WHERE 1=1`;

        // 拼接关键字模糊匹配条件
        if (keyword) {
            sql += " AND (name LIKE ? OR username LIKE ?)";
        }

        // 拼接排序条件
        if (orderField && orderSeq) {
            const validOrderSeq = orderSeq.toUpperCase() === "ASC" ? "ASC" : "DESC";
            sql += ` ORDER BY ${orderField} ${validOrderSeq}`;
        } else {
            sql += " ORDER BY id DESC"; // 默认按id倒序排序
        }

        // 拼接分页条件
        if (pageSize && pageNo) {
            const validPageSize = parseInt(pageSize);
            const validPageNo = parseInt(pageNo);
            const startIndex = (validPageNo - 1) * validPageSize;
            sql += ` LIMIT ${startIndex}, ${validPageSize}`;
        }

        // 如果没有传入pageSize和pageNo，则不分页，返回所有数据
        const query = sqlUtil.execute(sql, keyword ? [`%${keyword}%`, `%${keyword}%`] : []);
        query.then(
            (value) => fullFilled(response, value),
            (error) => errorHandler(response, error)
        );
    } catch (error) {
        console.info("error in create users:", error);
        errorHandler(response, error);
    }
});

// 修改用户
router.put("/users/:id", verifyToken, async (request, response) => {
    try {
        const { id } = request.params;
        // Get user data from request body
        const { name, username, password, telephone, desc } = request.body;
        const sql =
            "UPDATE user SET name = ?, username = ?, password = ?, telephone = ?, `desc` = ? WHERE id = ?";
        const params = [name, username, password, telephone, desc, id];
        const value = await sqlUtil.execute(sql, params);
        // 成功后，直接删除 Redis 缓存中的数据，下次查询时会重新获取最新数据
        await redisTool.deleteKey(CACHE_KEY);
        fullFilled(response, value);
    } catch (error) {
        console.error("Error in updating user:", error);
        errorHandler(response, error);
    }
});

// 删除用户
router.delete("/users/:id", verifyToken, async (request, response) => {
    try {
        const { id } = request.params;
        const sql = "DELETE FROM user WHERE id = ?";
        const value = await sqlUtil.execute(sql, [id]);
        // 成功后，直接删除 Redis 缓存中的数据，下次查询时会重新获取最新数据
        await redisTool.deleteKey(CACHE_KEY);
        fullFilled(response, value);
    } catch (error) {
        console.error("Error in deleting user:", error);
        errorHandler(response, error);
    }
});

// 查询全部用户并使用缓存
router.get("/all", verifyToken, async (request, response) => {
    try {
        // 尝试从 Redis 缓存中获取用户列表数据
        let userList = await redisTool.getValue(CACHE_KEY);
        console.info("userList:", userList);
        if (!userList) {
            // 如果缓存中没有数据，则从数据库中查询数据
            const sql = `SELECT id, name, username, telephone, \`desc\` FROM user`;

            const query = sqlUtil.execute(sql);
            userList = await query;

            // 将查询结果存入 Redis 缓存
            redisTool.setValue(CACHE_KEY, userList);
        }

        // 返回查询结果
        fullFilled(response, userList);
    } catch (error) {
        console.info("error in create users:", error);
        errorHandler(response, error);
    }
});

module.exports = router;

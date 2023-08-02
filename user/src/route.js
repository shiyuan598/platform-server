const express = require("express");
const jwt = require("jsonwebtoken");
const sqlUtil = require("./tools/sqlUtil");
const { SECRET_KEY } = require("../config");

const router = express.Router();

const generateToken = (user) => {
    try {
        // 生成Token，默认使用 HMAC SHA-256
        const token = jwt.sign(user, SECRET_KEY, { expiresIn: "8h" });
        return token;
    } catch (error) {
        throw error;
    }
};

const verifyToken = (request, response, next) => {
    const token = request.headers.authorization;
    console.info("token", token);

    if (!token) {
        return response.status(401).json({ message: "Unauthorized" });
    }

    jwt.verify(token, SECRET_KEY, (err, decoded) => {
        if (err) {
            return response.status(401).json({ message: "Invalid token" });
        }

        request.user = decoded;
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
router.get("/", (req, res) => {
    res.send("测试 " + Date.now());
});

// 处理特定路径的路由
router.post("/login", async (request, response) => {
    try {
        const { username, password } = request.body;

        const sql = `SELECT id, name, username, role FROM user WHERE username = ? AND password = ?`;
        const user = await sqlUtil.execute(sql, [username, password]);
        if (!user || !user.length) {
            fullFilled(response, { msg: "用户名或密码错误" }, undefined, 1);
        } else {
            fullFilled(response, { token: generateToken(user[0]) });
        }
    } catch (error) {
        console.info("error in login:", error);
        errorHandler(response, error);
    }
});

// 访问受保护的路由
router.post("/protected", verifyToken, (request, response) => {
    response.json({ msg: "haha" });
});

module.exports = router;

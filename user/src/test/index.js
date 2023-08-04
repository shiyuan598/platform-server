// client-app.js

const axios = require("axios");

const baseUrl = "http://localhost:9040";

let TOKEN = null;

// 模拟用户登录并获取令牌
async function login() {
    try {
        const response = await axios.post(`${baseUrl}/user/login`, {
            username: "root",
            password: "123"
        });

        const { code, data } = response.data;
        if (code !== 1) {
            const token = data.token;
            if (token) {
                TOKEN = token;
            }
        }
    } catch (error) {
        console.error(error.message);
        return null;
    }
}

const getUserById = (id) => {
    axios
        .get(`${baseUrl}/user/users/${id}`, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

const getUsers = () => {
    axios
        .get(`${baseUrl}/user/users?pageNo=1&pageSize=4&keyword=y&orderField=id&orderSeq=ASC`, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

const getAllUsers = () => {
    axios
        .get(`${baseUrl}/user/all`, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

const updateUser = (id) => {
    axios
        .put(
            `${baseUrl}/user/users/${id}`,
            { name: "杨多多", username: "yhdodo", password: 123, telephone: "15239177793", role: 1, desc: "不错不错" },
            {
                headers: {
                    authorization: TOKEN
                }
            }
        )
        .then((v) => {
            console.info(v.data);
        });
};

const deleteUserById = (id) => {
    axios
        .delete(`${baseUrl}/user/users/${id}`, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

login();

setTimeout(async () => {
    await deleteUserById(53);
    getAllUsers();
    // visitUpdateUser(33);
}, 1000);

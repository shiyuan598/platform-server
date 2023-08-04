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
            console.info("data:", data);
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

const visitGetUser = (id) => {
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

const visitGetUsers = () => {
    axios
        .get(`${baseUrl}/user/users`, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

const visitUpdateUser = (id) => {
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

login();

setTimeout(() => {
    visitGetUsers();
    // visitUpdateUser(33);
}, 1000);

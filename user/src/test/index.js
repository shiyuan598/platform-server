// client-app.js

const axios = require("axios");
const jwt = require("jsonwebtoken");
const { SECRET_KEY } = require("../../config");

let TOKEN = null;

// 模拟用户登录并获取令牌
async function login() {
    try {
        const response = await axios.post("http://localhost:9040/user/login", {
            username: "root",
            password: "123"
        });

        const { code, data } = response.data;
        if (code !== 1) {
            const token = data.token;
            if (token) {
                console.log("token:", token);
                const decodedToken = jwt.verify(token, SECRET_KEY);
                console.info("decodedToken:", decodedToken);
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
        .get(`http://localhost:9040/user/users/${id}`, {
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
        .put(`http://localhost:9040/user/users/${id}`, { name: "杨多多", username: "yhdodo", password: 123, telephone: "15239177793", role: 1, desc: "不错不错"}, {
            headers: {
                authorization: TOKEN
            }
        })
        .then((v) => {
            console.info(v.data);
        });
};

login();

setTimeout(() => {
    // visitGetUser(23);
    visitUpdateUser(33);
}, 1000);


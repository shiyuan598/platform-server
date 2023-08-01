// client-app.js

const axios = require("axios");

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
            }
        }
    } catch (error) {
        console.error(error.message);
        return null;
    }
}

// 主函数
(async () => {
    const token = await login();
})();

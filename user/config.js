// 开发环境配置
const development = {
    PORT: 9040,
    DATABASE: {
        host: "localhost",
        port: 3307,
        user: "root",
        password: "123456",
        database: "user"
    },
    REDIS: {
        host: "127.0.0.1",
        port: 6378,
    },
    SECRET_KEY: "vimaklmf22@#"
};
// 生产环境配置
const production = {
    PORT: 9044,
    DATABASE: {
        host: "localhost",
        port: 3307,
        user: "root",
        password: "123456",
        database: "user"
    },
    REDIS: {
        host: "127.0.0.1",
        port: 6378,
    },
    SECRET_KEY: "vimaklmf22@#"
};

const config = process.env.NODE_ENV === "production" ? production : development;

module.exports = config;

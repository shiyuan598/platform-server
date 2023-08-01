const { DATABASE } = require("./config");
console.info("DATABASE", DATABASE);
module.exports = {
    client: "mysql2",
    connection: DATABASE,
    debug: true, // 启用调试模式，输出更详细的日志
    migrations: {
        directory: "./migrations" // 指定迁移文件存放的目录
    }
};

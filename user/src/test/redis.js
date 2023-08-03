const redisTool = require("../tools/redisUtil");

console.info(redisTool);

async function exampleUsage() {
    // 设置值到Redis中，并设置过期时间为60秒
    await redisTool.setValue("userinfo", { name: "Alice", age: 25 }, 60);

    // 从Redis中获取值
    const userinfo = await redisTool.getValue("userinfo");
    console.log(userinfo);
}

// exampleUsage();

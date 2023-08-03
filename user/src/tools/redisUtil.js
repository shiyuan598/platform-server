const Redis = require("ioredis");
const config = require("../../config");

const prefix = 'USER:';
const redis = new Redis(config.REDIS);

// 设置值到Redis中，设置过期时间（单位：秒）
async function setValue(key, value, expireSeconds = 24 * 60 * 60) {
  try {
    if (expireSeconds) {
      return await redis.setex(prefix + key, expireSeconds, JSON.stringify(value));
    } else {
      return await redis.set(prefix + key, JSON.stringify(value));
    }
  } catch (error) {
    // 这里可以根据需要进行异常处理
    console.error('Error while setting value in Redis:', error.message);
    throw error;
  }
}

// 从Redis中获取值
async function getValue(key) {
  try {
    const value = await redis.get(prefix + key);
    return value ? JSON.parse(value) : null;
  } catch (error) {
    // 这里可以根据需要进行异常处理
    console.error('Error while getting value from Redis:', error.message);
    throw error;
  }
}

// 从Redis中删除指定的键
async function deleteKey(key) {
  try {
    await redis.del(prefix + key);
  } catch (error) {
    // 这里可以根据需要进行异常处理
    console.error('Error while deleting key from Redis:', error.message);
    throw error;
  }
}

// 导出方法供其他模块使用
module.exports = {
  setValue,
  getValue,
  deleteKey
};

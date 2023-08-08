from redis import Redis
import json

redis = Redis(host="127.0.0.1", port=6378)

data = redis.get("name")
data = redis.hgetall("girl")
print(data[b'name'])
value = json.dumps({'pp': [1, 2 ,3, 4], 'm': ['g', 's', 'q']})
redis.set('greentea', value, ex=60 * 60 * 4)
res = json.loads(redis.get('greentea').decode("utf-8"))
# print(res)
# print(res["pp"])
# print(res["pp"][0])
print(redis.set(name="dog", value="a dog"), "\n")

# dict1 = {'a': 1, 'b': 2}
# dict2 = {'c': 3, 'd': 4}

# res = dict1.update(dict2)
# print(dict1, {**dict1, **dict2})
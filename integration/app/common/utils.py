from urllib.parse import urlparse, parse_qs

# 把一个列表转为一个个的key-value
def generateEntries(keys, values):
    try:
        count = len(keys)
        data = []
        for item in values:
            keyValues = {}
            for i in range(count):
                keyValues[keys[i]] = item[i]
            data.append(keyValues)
        return data
    except:
        return []

# 获取url中的参数
def get_url_param_value(url, key):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    param_value = query_params.get(key, [""])[0]
    return param_value
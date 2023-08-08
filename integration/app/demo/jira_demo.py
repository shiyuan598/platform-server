import json
import requests

headers = {
    'Content-Type': 'application/json',
}

jira_response = requests.get('https://jira.zhito.com:8080/rest/api/2/issue/' +
                             'AI-74',
                             headers=headers,
                             auth=("wangshiyuan", "zhito26@#"))
print("response:", jira_response, jira_response.text)
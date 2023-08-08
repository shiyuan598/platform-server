import requests

url = "http://172.16.12.84:9011/monitor/status/update"
data = {
    "project": 1,
    "project_artifacts": 'HWL4_X86/cicd',
    "creator": 1,
    "vehicles": "J7A01"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=data, headers=headers, timeout=1)
    response.raise_for_status()
    print("Status updated successfully!", response.text)
except requests.exceptions.Timeout:
    print("Request timeout!")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
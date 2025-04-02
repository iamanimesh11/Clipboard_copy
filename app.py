import requests
url ="https://api.tomtom.com/routing/1/calculateRoute/28.5928230,77.4584486:28.6020117,77.4499369/json?key=EQEuzLbnAf2rBfIu244A8ds4A3sPD6BK"
response = requests.get(url, verify=False,timeout=30)  # Added timeout for reliability
response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
data = response.json()
print(data)
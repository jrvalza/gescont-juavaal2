
import requests

payload = {'gid': '2'}
r = requests.get('http://localhost:8000/appdesweb/building_select_by_gid/', params=payload)
print(r.text, r.json())



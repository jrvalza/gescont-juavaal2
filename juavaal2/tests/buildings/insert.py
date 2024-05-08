
import requests

payload = {'descripcion': 'desde python', 'geomWkt': 'POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))'}
r = requests.post('http://localhost:8000/appdesweb/building_insert/', data=payload)
print(r.status_code,r.text, r.json())




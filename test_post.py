import requests
r = requests.post('http://localhost:5000/api/harvest')
print(r.status_code, r.text)

import requests
r = requests.post('http://localhost:5001/api/harvest')
print(r.status_code, r.text)

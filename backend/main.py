import requests

BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"

sources = ['InciWeb']
r = requests.get(f'{BASE_URL}/events', params={'source': sources})
print(r.json())
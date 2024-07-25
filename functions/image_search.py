import requests

API_KEY = '99facfeff834ba35fc565500242209abc4e1f3ef73abb4c51f73e4268da252ab'# O'z API kalitingizni kiriting

def get_photos(q, API_KEY):
    url = 'https://serpapi.com/search'
    params = {
        'api_key': API_KEY,
        'engine': 'yandex_images',
        'text': q,  # To'g'ri o'zgaruvchi
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        images = data.get('images_results', [])
        return [image['original'] for image in images]
        
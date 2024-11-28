import requests
import json

def test_prediction():
    url = 'http://localhost:5000/predict'
    
    data = {
        'commodity': 'tomato_big(nepali)',
        'weather_data': {
            'maxt': 30.0,
            'mint': 20.0,
            'windspeed': 1.7,
            'humidity': 64.1,
            'precipitation': 0.0,
            'month': 1,
            'day': 1
        },
        'price_data': {
            'minimum': 40.0,
            'maximum': 45.0,
            'average': 42.5
        },
        'festival_name': "new_year's_day"
    }
    
    response = requests.post(url, json=data)
    print('Status Code:', response.status_code)
    print('Response:', json.dumps(response.json(), indent=2))

def test_get_commodities():
    url = 'http://localhost:5000/commodities'
    response = requests.get(url)
    print('Status Code:', response.status_code)
    print('Available Commodities:', json.dumps(response.json(), indent=2))

def test_get_festivals():
    url = 'http://localhost:5000/festivals'
    response = requests.get(url)
    print('Status Code:', response.status_code)
    print('Available Festivals:', json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print("Testing prediction endpoint:")
    test_prediction()
    print("\nTesting commodities endpoint:")
    test_get_commodities()
    print("\nTesting festivals endpoint:")
    test_get_festivals()
import requests
import json

# Test single prediction
test_input = {
    'maxt': 29.9,
    'mint': 20.1,
    'windspeed': 1.7,
    'humidity_': 64.1,
    'precipitation': 0.0,
    'month': 1,
    'day': 1,
    'year': 2017,
    'commodity': 'tomato_big(nepali)',
    'commodity_category': 'vegetables',
    'average': 42.5
}

# Make prediction
response = requests.post('http://localhost:5000/predict', 
                        json=test_input)
print("Single Prediction Response:")
print(json.dumps(response.json(), indent=2))

# Test batch prediction with different vegetables
batch_input = [
    {
        'maxt': 29.9,
        'mint': 20.1,
        'windspeed': 1.7,
        'humidity_': 64.1,
        'precipitation': 0.0,
        'month': 1,
        'day': 1,
        'year': 2017,
        'commodity': 'tomato_big(nepali)',
        'commodity_category': 'vegetables',
        'average': 42.5
    },
    {
        'maxt': 29.9,
        'mint': 20.1,
        'windspeed': 1.7,
        'humidity_': 64.1,
        'precipitation': 0.0,
        'month': 1,
        'day': 1,
        'year': 2017,
        'commodity': 'potato_red',
        'commodity_category': 'vegetables',
        'average': 26.5
    },
    {
        'maxt': 29.9,
        'mint': 20.1,
        'windspeed': 1.7,
        'humidity_': 64.1,
        'precipitation': 0.0,
        'month': 1,
        'day': 1,
        'year': 2017,
        'commodity': 'apple(jholey)',
        'commodity_category': 'fruits',
        'average': 105.0
    }
]

response = requests.post('http://localhost:5000/batch_predict', 
                        json=batch_input)
print("\nBatch Prediction Response:")
print(json.dumps(response.json(), indent=2))
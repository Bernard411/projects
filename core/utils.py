import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

from core.models import User, Item, Interaction

def get_recommendations(user_id):
    interactions = Interaction.objects.all()
    data = pd.DataFrame(list(interactions.values('user_id', 'item_id', 'rating')))
    
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['user_id', 'item_id', 'rating']], reader)

    trainset, testset = train_test_split(dataset, test_size=0.25)

    algo = SVD()
    algo.fit(trainset)

    item_ids = Item.objects.values_list('id', flat=True)
    recommendations = []
    
    for item_id in item_ids:
        if not Interaction.objects.filter(user_id=user_id, item_id=item_id).exists():
            est = algo.predict(user_id, item_id).est
            recommendations.append((item_id, est))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommended_items = [Item.objects.get(id=item[0]) for item in recommendations[:5]]
    
    return recommended_items

import requests

def fetch_weather_data(city):
    api_key = '7c3a479127bb331300be72a531799036'  # Ensure this is set correctly
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        if data.get('cod') != 200:
            return None
        return {
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
            'city': data['name'],
            'country': data['sys']['country'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
    except requests.exceptions.RequestException as e:
        return None

def generate_recommendations(user_data):
    city = user_data['city']
    gender = user_data['gender']
    temp_sensitivity = user_data.get('temp_sensitivity', 0)
    preferred_colors = user_data.get('preferred_colors', '').split(',')

    weather_data = fetch_weather_data(city)
    if not weather_data:
        return {'error': 'Could not fetch weather data for the specified city.'}

    temperature = weather_data['temperature'] + temp_sensitivity
    condition = weather_data['condition']

    recommendations = {
        'weather': weather_data,
        'formal': [],
        'casual': [],
        'sports': []
    }

    # Temperature-based recommendations
    if temperature < 0:
        if gender == 'male':
            recommendations['formal'].append('Heavy winter formal wear (e.g., thermal suits)')
            recommendations['casual'].append('Heavy winter casual wear (e.g., thermal jackets)')
            recommendations['sports'].append('Heavy winter sportswear (e.g., thermal activewear)')
        else:
            recommendations['formal'].append('Heavy winter formal wear (e.g., woolen dresses)')
            recommendations['casual'].append('Heavy winter casual wear (e.g., thermal jackets, long skirts)')
            recommendations['sports'].append('Heavy winter sportswear (e.g., thermal leggings, sports bras)')
    elif 0 <= temperature < 10:
        if gender == 'male':
            recommendations['formal'].append('Winter formal wear (e.g., suits, sweaters)')
            recommendations['casual'].append('Winter casual wear (e.g., sweaters, jackets)')
            recommendations['sports'].append('Winter sportswear (e.g., sports jackets, pants)')
        else:
            recommendations['formal'].append('Winter formal wear (e.g., dresses, sweaters)')
            recommendations['casual'].append('Winter casual wear (e.g., sweaters, jackets, long skirts)')
            recommendations['sports'].append('Winter sportswear (e.g., sports jackets, leggings)')
    elif 10 <= temperature < 20:
        if gender == 'male':
            recommendations['formal'].append('Light formal wear (e.g., suits, blazers)')
            recommendations['casual'].append('Light casual wear (e.g., jackets, long sleeve shirts)')
            recommendations['sports'].append('Light sportswear (e.g., track suits)')
        else:
            recommendations['formal'].append('Light formal wear (e.g., dresses, blazers)')
            recommendations['casual'].append('Light casual wear (e.g., cardigans, long sleeve shirts)')
            recommendations['sports'].append('Light sportswear (e.g., track suits, leggings)')
    else:
        if gender == 'male':
            recommendations['formal'].append('Summer formal wear (e.g., light suits, dress shirts)')
            recommendations['casual'].append('Summer casual wear (e.g., t-shirts, shorts)')
            recommendations['sports'].append('Summer sportswear (e.g., shorts, sports t-shirts)')
        else:
            recommendations['formal'].append('Summer formal wear (e.g., light dresses, blouses)')
            recommendations['casual'].append('Summer casual wear (e.g., t-shirts, skirts)')
            recommendations['sports'].append('Summer sportswear (e.g., shorts, sports bras, sports t-shirts)')

    # Condition-based recommendations
    if condition == 'Rain':
        recommendations['formal'].append('Waterproof formal wear')
        recommendations['casual'].append('Waterproof casual wear')
        recommendations['sports'].append('Waterproof sportswear')
    elif condition == 'Sunny':
        recommendations['formal'].append('Sunglasses and hats for formal wear')
        recommendations['casual'].append('Sunglasses and hats for casual wear')
        recommendations['sports'].append('Sunglasses and hats for sportswear')

    # Color recommendations
    if preferred_colors:
        recommendations['formal'].append(f'Preferred colors: {", ".join(preferred_colors)}')
        recommendations['casual'].append(f'Preferred colors: {", ".join(preferred_colors)}')
        recommendations['sports'].append(f'Preferred colors: {", ".join(preferred_colors)}')

    return recommendations

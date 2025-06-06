import requests
import pandas as pd
import time
import os

API_KEY = '93be52922464c8b6d8dc69c14553ab05'

cities = [
    {'city': 'BARNAUL', 'lat': 53.354, 'lon': 83.763},
    {'city': 'MOSKOW', 'lat': 55.7558, 'lon': 37.6173},
    {'city': 'LONDON', 'lat': 51.5074, 'lon': -0.1278},
    {'city': 'NY', 'lat': 40.7128, 'lon': -74.0060},
    {'city': 'TOKIO', 'lat': 35.6895, 'lon': 139.6917}
]

def fetch_and_save_data():
    records = []
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={city["lat"]}&lon={city["lon"]}&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()

        components = data['list'][0]['components']
        aqi = data['list'][0]['main']['aqi']

        records.append({
            'city': city['city'],
            'co': components['co'],
            'no': components['no'],
            'no2': components['no2'],
            'o3': components['o3'],
            'so2': components['so2'],
            'pm2_5': components['pm2_5'],
            'pm10': components['pm10'],
            'nh3': components['nh3'],
            'aqi': aqi,
            'timestamp': pd.Timestamp.now()
        })

    df = pd.DataFrame(records)

    if not os.path.exists('air_quality_data.csv'):
        df.to_csv('air_quality_data.csv', index=False)
    else:
        df.to_csv('air_quality_data.csv', mode='a', header=False, index=False)

    print(f"✅ Данные обновлены: {pd.Timestamp.now()}")

if __name__ == "__main__":
    while True:
        try:
            fetch_and_save_data()
            time.sleep(3600)  # Обновление каждый час
        except Exception as e:
            print(f"❌ Ошибка обновления: {e}")
            time.sleep(60)

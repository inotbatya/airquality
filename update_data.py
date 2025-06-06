import requests
import pandas as pd
import time
import os

API_KEY = '93be52922464c8b6d8dc69c14553ab05'
LAT, LON = 53.354, 83.763  # Барнаул
DATA_FILE = "air_quality_data.csv"

def fetch_and_save_data():
    url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    components = data['list'][0]['components']
    aqi = data['list'][0]['main']['aqi']

    df = pd.DataFrame([{
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
    }])

    if not os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)

    print(f"✅ Данные обновлены: {pd.Timestamp.now()}")

if __name__ == "__main__":
    while True:
        try:
            fetch_and_save_data()
            time.sleep(5)  # Обновление каждые 60 минут 
        except Exception as e:
            print(f"❌ Ошибка обновления: {e}")
            time.sleep(60)

import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

api_key = os.getenv("API_KEY")

cities = ['New York', 'London', 'Tokyo', 'Sydney']

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def filter_last_month_data(data):

    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    
    filtered_data = [item for item in data['list'] if datetime.fromtimestamp(item['dt']) >= one_month_ago]
    return filtered_data

def plot_temperature_change(city, data):
    dates = [datetime.fromtimestamp(item['dt']) for item in data]
    temperatures = [item['main']['temp'] for item in data]
    plt.plot(dates, temperatures, label=city)

for city in cities:
    data = get_weather_data(city)
    filtered_data = filter_last_month_data(data)
    plot_temperature_change(city, filtered_data)

plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Change Over Time (Last Month)')
plt.legend()

plt.gcf().autofmt_xdate()  
plt.tight_layout()  

plt.show()

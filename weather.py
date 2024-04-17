import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Загрузка значений из файла .env
load_dotenv()

# Получение API-ключа из файла .env
api_key = os.getenv("API_KEY")

# Список городов, для которых вы хотите получить данные о погоде
cities = ['New York', 'London', 'Tokyo', 'Sydney']

# Функция для получения данных о погоде для конкретного города
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

# Функция для фильтрации данных за последний месяц
def filter_last_month_data(data):
    # Получаем текущую дату и дату на месяц назад
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    
    # Фильтруем данные за последний месяц
    filtered_data = [item for item in data['list'] if datetime.fromtimestamp(item['dt']) >= one_month_ago]
    return filtered_data

# Функция для построения графика изменения температуры
def plot_temperature_change(city, data):
    dates = [datetime.fromtimestamp(item['dt']) for item in data]
    temperatures = [item['main']['temp'] for item in data]
    plt.plot(dates, temperatures, label=city)

# Получение данных о погоде для каждого города и построение графиков
for city in cities:
    data = get_weather_data(city)
    filtered_data = filter_last_month_data(data)
    plot_temperature_change(city, filtered_data)

# Настройка графика
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Change Over Time (Last Month)')
plt.legend()

plt.gcf().autofmt_xdate()  # автоматическая установка даты
plt.tight_layout()  # автоматическая настройка размеров графика

plt.show()

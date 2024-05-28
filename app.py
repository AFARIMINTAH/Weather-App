from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "YOUR_API_KEY"

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        weather_info = {
            "city": data['name'],
            "temperature": main['temp'],
            "pressure": main['pressure'],
            "humidity": main['humidity'],
            "weather_description": weather['description'],
            "wind_speed": wind['speed']
        }
        return weather_info
    else:
        return None

def get_forecast(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']
        forecast_info = []
        
        for forecast in forecast_list:
            date_time = forecast['dt_txt']
            main = forecast['main']
            weather = forecast['weather'][0]
            wind = forecast['wind']
            
            forecast_info.append({
                "date_time": date_time,
                "temperature": main['temp'],
                "pressure": main['pressure'],
                "humidity": main['humidity'],
                "weather_description": weather['description'],
                "wind_speed": wind['speed']
            })
        
        return forecast_info
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    forecast_data = None
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = get_weather(city_name, API_KEY)
        forecast_data = get_forecast(city_name, API_KEY)
    
    return render_template('weather.html', weather_data=weather_data, forecast_data=forecast_data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

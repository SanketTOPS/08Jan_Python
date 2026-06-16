from django.shortcuts import render
import requests
from django.contrib import messages
from datetime import datetime

def index(request):
    api_key = "62ecdc3c359673db0e16868ab8e77251"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
    
    weather_data = None
    city = ""
    
    if request.method == "POST":
        city = request.POST.get('city')
        if city:
            try:
                response = requests.get(url.format(city, api_key))
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        'city': data['name'],
                        'temperature': round(data['main']['temp']),
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'feels_like': round(data['main']['feels_like']),
                        'country': data['sys']['country'],
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon'],
                        'pressure': data['main']['pressure'],
                        'visibility': round(data.get('visibility', 0) / 1000, 1), # convert to km
                        'clouds': data['clouds']['all'],
                        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
                        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
                        'temp_min': round(data['main']['temp_min']),
                        'temp_max': round(data['main']['temp_max']),
                    }
                else:
                    messages.error(request, f"City '{city}' not found.")
            except Exception as e:
                messages.error(request, "An error occurred while fetching weather data.")
        else:
            messages.error(request, "Please enter a city name.")

    context = {
        'weather_data': weather_data,
        'city': city,
    }
    return render(request, 'weatherapp/index.html', context)

from django.shortcuts import render, redirect
from .models import City
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e6131fb9e703a878b2b21ac20d9bd430'
    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        new_city = request.POST.get('city')
        # Check if the city already exists
        if City.objects.filter(name__iexact=new_city).exists():
            error_message = f"The city '{new_city}' is already in the list."
        else:
            # Make an API call to validate the city
            r = requests.get(url.format(new_city)).json()
            if r.get('cod') == 200:  # City found
                City.objects.create(name=new_city)
            else:
                error_message = f"'{new_city}' is not a valid city name."

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'error_message': error_message,  # Pass error message to template
    }

    return render(request, 'weather/weather.html', context)

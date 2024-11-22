from django.shortcuts import render, redirect, get_object_or_404
from .models import City
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e6131fb9e703a878b2b21ac20d9bd430'
    error_message = None

    # Handle POST request for adding a new city
    if request.method == 'POST':
        new_city = request.POST.get('city').strip()
        if City.objects.filter(name__iexact=new_city).exists():
            error_message = f"The city '{new_city}' is already in the list."
        else:
            # Make an API call to validate the city
            r = requests.get(url.format(new_city)).json()
            if r.get('cod') == 200:  # City found
                City.objects.create(name=new_city)
            else:
                error_message = f"'{new_city}' is not a valid city name."

    # Retrieve all cities and their weather data
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        city_weather = {
            'id': city.id,  # Include city ID for deletion
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
    }

    if error_message:
        context['error_message'] = error_message

    return render(request, 'weather/weather.html', context)


def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('index')

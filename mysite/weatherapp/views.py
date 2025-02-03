import urllib.request
import json
from django.shortcuts import render
from urllib.error import HTTPError, URLError

def index(request):
    data = {}  # Ensure data is always initialized

    if request.method == 'POST':
        city = request.POST.get('city')  # Use .get() to avoid KeyError

        if city:  # Check if city is provided
            api_key = 'c55b9abe4b1a1c77ca5289c0d1101131'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'  # Added units=metric for °C

            try:
                source = urllib.request.urlopen(url).read()
                list_of_data = json.loads(source)

                # Check for API errors in the response
                if list_of_data.get("cod") != 200:
                    error_message = list_of_data.get("message", "Unknown error")
                    return render(request, "main/index.html", {"error": f"API Error: {error_message}"})

                # Prepare weather data
                data = {
                    "country_code": list_of_data['sys']['country'],
                    "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                    "temp": f"{list_of_data['main']['temp']} °C",
                    "pressure": list_of_data['main']['pressure'],
                    "humidity": list_of_data['main']['humidity'],
                    "main": list_of_data['weather'][0]['main'],
                    "description": list_of_data['weather'][0]['description'],
                    "icon": list_of_data['weather'][0]['icon'],
                }

            except HTTPError as e:
                return render(request, "main/index.html", {"error": f"HTTP Error: {e.code} - {e.reason}"})
            except URLError as e:
                return render(request, "main/index.html", {"error": f"Network Error: {e.reason}"})
            except Exception as e:
                return render(request, "main/index.html", {"error": f"Unexpected Error: {str(e)}"})
        else:
            return render(request, "main/index.html", {"error": "Please enter a city name."})

    return render(request, "main/index.html", data)

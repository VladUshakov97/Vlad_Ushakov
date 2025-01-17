import json
import requests
from geopy import distance
import folium
from dotenv import load_dotenv
import os 

load_dotenv('secret.env')

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None
    most_relevant = found_places[0]
    lon, lat = map(float, most_relevant['GeoObject']['Point']['pos'].split(" "))
    return lat, lon

def main():
    apikey = os.getenv('APIKEY')
    with open('coffee.json', 'r', encoding='CP1251') as my_file:
        coffee_data = json.load(my_file)
    coffee_list = []
    for coffee in coffee_data:
        if all(key in coffee for key in ['Name', 'Longitude_WGS84', 'Latitude_WGS84']):
            coffee_list.append({
                'Name': coffee['Name'],
                'Coordinates': (float(coffee['Latitude_WGS84']), float(coffee['Longitude_WGS84']))
            })
    user_address = input('Где вы находитесь?: ')
    user_coords = fetch_coordinates(apikey, user_address)
    for coffee in coffee_list:
        coffee['Distance'] = distance.distance(user_coords, coffee['Coordinates']).km
    sorted_coffee_list = sorted(coffee_list, key=lambda x: x['Distance'])
    top_5_coffee = sorted_coffee_list[:5]
    coffee_map = folium.Map(location=user_coords, zoom_start=14)
    folium.Marker(
        location=user_coords,
        popup="Вы здесь",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(coffee_map)
    for coffee in top_5_coffee:
        folium.Marker(
            location=coffee['Coordinates'],
            popup=f"{coffee['Name']} ({coffee['Distance']:.2f} км)",
            icon=folium.Icon(color="red", icon="coffee")
        ).add_to(coffee_map)
    coffee_map.save("coffee_map.html")

if __name__ == "__main__":
    main()

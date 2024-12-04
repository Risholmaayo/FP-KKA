from flask import Flask, render_template, request
import requests
import folium
from io import BytesIO
import base64

app = Flask(__name__)

# Ganti dengan API Key Google Maps Anda
API_KEY = 'AIzaSyB3mqQVlYPkVxLWtsUCva5iqzLgw4Nsg5g'

def get_route(start, end):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': start,  # Titik asal (nama tempat atau koordinat)
        'destination': end,  # Titik tujuan (nama tempat atau koordinat)
        'key': API_KEY,  # API Key
        'mode': 'driving'  # Jenis transportasi (driving, walking, bicycling, etc.)
    }
    
    # Mengirim permintaan ke API Directions
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        route = data['routes'][0]
        distance = route['legs'][0]['distance']['text']  # Mengambil jarak rute
        return route, distance  # Mengembalikan rute dan jarak
    else:
        return None, None

def create_map(route):
    # Mendapatkan lokasi start dan end
    start_location = route['legs'][0]['start_location']
    end_location = route['legs'][0]['end_location']
    
    # Membuat peta dengan Folium, zoom_start diatur lebih besar agar lebih detail
    m = folium.Map(location=[start_location['lat'], start_location['lng']], zoom_start=15)

    # Menambahkan marker untuk titik awal (Start)
    folium.Marker(
        location=[start_location['lat'], start_location['lng']],
        popup="Titik Awal",  # Popup saat marker diklik
        icon=folium.Icon(color='green', icon='cloud')
    ).add_to(m)

    # Menambahkan marker untuk titik tujuan (End)
    folium.Marker(
        location=[end_location['lat'], end_location['lng']],
        popup="Titik Tujuan",  # Popup saat marker diklik
        icon=folium.Icon(color='red', icon='cloud')
    ).add_to(m)

    # Menambahkan rute ke peta
    for leg in route['legs']:
        points = []
        for step in leg['steps']:
            points.append([step['end_location']['lat'], step['end_location']['lng']])

        folium.PolyLine(points, color="blue", weight=5, opacity=1).add_to(m)

    # Mengkonversi peta menjadi string HTML
    map_html = m._repr_html_()  # Menggunakan metode _repr_html_ untuk mendapatkan HTML peta
    return map_html



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find-path', methods=['POST'])
def find_path():
    start = request.form['start']
    end = request.form['end']
    
    route, distance = get_route(start, end)

    if route:
        map_html = create_map(route)
        return render_template('route_map.html', distance=distance, map_html=map_html)
    else:
        return "Error: Tidak dapat menemukan rute", 4

if __name__ == '__main__':
    app.run(debug=True)

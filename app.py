from flask import Flask, render_template, request
import requests
import folium

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
        return route
    else:
        return None

def create_map(route):
    # Membuat peta dengan Folium
    start_location = route['legs'][0]['start_location']
    m = folium.Map(location=[start_location['lat'], start_location['lng']], zoom_start=12)

    # Menambahkan rute ke peta
    for leg in route['legs']:
        points = []
        for step in leg['steps']:
            points.append([step['end_location']['lat'], step['end_location']['lng']])

        folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

    # Menyimpan peta ke file HTML
    m.save("templates/route_map.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find-path', methods=['POST'])
def find_path():
    start = request.form['start']
    end = request.form['end']
    
    route = get_route(start, end)

    if route:
        create_map(route)
        return render_template('route_map.html')
    else:
        return "Error: Tidak dapat menemukan rute", 400

if __name__ == '__main__':
    app.run(debug=True)

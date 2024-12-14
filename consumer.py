from googletrans import Translator
from kafka import KafkaConsumer
from flask import Flask
import json
import folium
import threading

translator = Translator()

app = Flask(__name__)

consumer = KafkaConsumer(
    'here_traffic', 'jawg_routing',  # Topic names
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
)

print("Listening to topics: here_traffic & jawg_routing...")

traffic_data = None
routing_data = None

def merge_data(traffic, routing):
    try:
        # Add more robust error checking
        if not traffic or not routing:
            print("Incomplete traffic or routing data")
            return None

        # Check for valid routing data
        routes = routing.get('routes', [])
        if not routes:
            print("No 'routes' found in routing data")
            return None
        
        route = routes[0].get('geometry', {}).get('coordinates', [])
        if len(route) < 2:
            print("Not enough coordinates in the route")
            return None

        origin = f"{route[0][1]},{route[0][0]}"  # Latitude, Longitude
        dest = f"{route[-1][1]},{route[-1][0]}"  # Latitude, Longitude

        merged_result = {
            "origin": origin,
            "dest": dest,
            "distance": routes[0].get("distance", "Unknown"),
            "duration": routes[0].get("duration", 0),
            "timestamp": traffic.get("sourceUpdated", "Unknown"),
            "traffic_flow": traffic.get("results", [])
        }
        return merged_result
    except Exception as e:
        print(f"Merge data error: {e}")
        return None



def translate(traffic):
    results = traffic.get("results", [])
    for flow in results:
        description = flow.get("location", {}).get("description", "")
        if description:
            flow['location']['description'] = translator.translate(description).text
    return traffic


@app.route('/')
def serve_map():
    global traffic_data, routing_data

    if not traffic_data or not routing_data:
        return "Waiting for data from Kafka..."

    merged = merge_data(traffic_data, routing_data)
    if not merged:
        return "Unable to merge data, check logs."

    # Create a Folium-based map
    route_map = folium.Map(location=[25.24424, 55.30553], zoom_start=12)

    # Add route markers
    try:
        origin_coords = list(map(float, merged["origin"].split(',')))
        dest_coords = list(map(float, merged["dest"].split(',')))
        folium.Marker(origin_coords, popup="Origin", icon=folium.Icon(color="green")).add_to(route_map)
        folium.Marker(dest_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(route_map)
    except (ValueError, KeyError) as coord_error:
        print(f"Error adding route markers: {coord_error}")

    # Add traffic flow markers
    for flow in merged['traffic_flow']:
        try:
            location = flow.get("location", {}).get("coordinates", [])[0]
            description = flow.get("location", {}).get("description", "No description")
            if location:
                folium.Marker(
                    [location['latitude'], location['longitude']], 
                    popup=description
                ).add_to(route_map)
        except (IndexError, KeyError) as marker_error:
            print(f"Error adding traffic flow marker: {marker_error}")

    return route_map._repr_html_()


# Start Kafka consumer in a separate thread
def consume():
    global traffic_data, routing_data

    try:
        for message in consumer:
            topic = message.topic
            data = message.value

            if topic == 'here_traffic':
                print("Received traffic data")
                traffic_data = data
            elif topic == 'jawg_routing':
                print("Received routing data")
                routing_data = data
    except KeyboardInterrupt:
        print("Stopped consuming.")
    except Exception as e:
        print(f"Error in consumer: {e}")


# Start consumer thread before running the app
consumer_thread = threading.Thread(target=consume, daemon=True)
consumer_thread.start()

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

print("Listening for traffic data...")
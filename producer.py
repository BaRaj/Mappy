from kafka import KafkaProducer
import requests
import json
import time

# Create KafkaProducer instance
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON format
)

# Function to fetch traffic data and send to Kafka
def fetch_traffic_data():
    
    # HERE API URL
    url = "https://data.traffic.hereapi.com/v7/flow?in=circle:25.24424,55.30553;r=200&locationReferencing=olr&lang=en-US&apiKey=xu5WvsfMxZtNOhscJ8WTZQA5HA9R8O3YkSc-gO_IcSY"
    head = {
    "Accept-Language": "en-US"
    }
    
    response = requests.get(url, headers=head)
    tim = time.localtime()
    tims = time.strftime("%H:%M:%S", tim)    

    if response.status_code == 200:
        data = response.json()
        producer.send('here_traffic', value=data)
        print("\n<",tims,">")
        print("Latest map data sent to Kafka ")  # Optional: For logging purposes
    else:
        
        print("Error:", response.status_code, response.text)
        exit()

def fetch_routing_data():
    api_key = "xcjNybQn15d9OZXlHn0efREvMzHuEDsWqeL8OmcB30OLEkSR9DzaQWrhtYf58KJv"
    destination = "55.316292,25.268180"
    origin = "55.30553,25.24424"
    
    url = f"https://api.jawg.io/routing/route/v1/driving/{origin};{destination}?overview=false&access-token={api_key}"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        producer.send('jawg_routing', value = data)
        print("Latest routing data sent to Kafka  ")
    else:

        print("Error: ", response.status_code, response.text)
        exit()



# Infinite loop to fetch and send traffic data every minute
try:
    while True:
        fetch_traffic_data()
        fetch_routing_data()
        time.sleep(60)  # Wait for 1 minute before the next request
except KeyboardInterrupt:
    print("Stopped producing. ")
    exit()
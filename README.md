# Real-Time Traffic Monitoring and Route Optimization System

This project is a real-time traffic monitoring and route optimization tool. It integrates Kafka for message streaming, Google Translate for text translation, and Folium for map-based visualization. The application is containerized using Docker for ease of deployment.

---

## Features

1. **Real-Time Data Streaming**:

   - Consumes traffic and routing data from Kafka topics (`here_traffic` and `jawg_routing`).

2. **Data Translation and Merging**:

   - Merges traffic flow information with routing data.
   - Translates traffic descriptions into the desired language using Google Translate.

3. **Interactive Map Visualization**:

   - Displays routes and traffic information on a map using Folium.
   - Marks origin, destination, and traffic flow data with interactive popups.

4. **Web-Based Interface**:

   - Flask provides a web interface to display the map.

5. **Containerized Deployment**:

   - The entire system (Kafka broker, consumer, producer, and Flask app) can be deployed using Docker and `docker-compose`.

---

## Prerequisites

1. **Dependencies**:

   - Python 3.x
   - Kafka
   - Flask
   - Folium
   - `googletrans` library
   - Install Python dependencies:
     ```bash
     pip install kafka-python flask folium googletrans==4.0.0-rc1
     ```

2. **Kafka Setup** (if not using Docker):

   - Install Kafka and Zookeeper.
   - Start Zookeeper and Kafka brokers.
   - Create the topics `here_traffic` and `jawg_routing`:
     ```bash
     kafka-topics.sh --create --topic here_traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     kafka-topics.sh --create --topic jawg_routing --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

3. **Docker Setup**:

   - Install Docker and Docker Compose.
   - Build the images and start the containers with `docker-compose`.

---

## Running the Application

1. **Start the Application**:

   - Build and run the application using Docker Compose:
     ```bash
     docker-compose up --build
     ```

2. **Access the Web Interface**:

   - Open your browser and navigate to `http://localhost:5000`.

---

## Project Structure

```
.
├── consumer.py           # Kafka consumer and Flask app
├── producer.py           # Kafka producer (data generator)
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for Flask app
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

---

## Known Issues

- Routing data may occasionally be missing or malformed. This is logged as: `No valid route data found in routing`.
- Translation delays may occur for large volumes of traffic data.

---

## Next Steps

1. Debug Kafka producer to ensure valid routing data is always published.
2. Implement automated tests for integration and edge cases.
3. Add monitoring/logging for Kafka messages.

---

## Contribution

Feel free to raise issues or contribute via pull requests.

---


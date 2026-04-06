import time
import json
import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Connection Settings
CLIENT_ID = "StreamLine_Edge_Node"
ENDPOINT = "al312bhfmjvjc-ats.iot.us-east-1.amazonaws.com" 
CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "certificate.pem.crt"
KEY_PATH = "private.pem.key"

# Initialize MQTT Client
myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

myMQTTClient.connect()
print("Edge Node Connected to AWS Cloud...")

while True:
    # Simulate High-Frequency Vital Signs
    data = {
        "heart_rate": random.randint(60, 160),
        "blood_pressure": f"{random.randint(110,140)}/{random.randint(70,90)}",
        "timestamp": time.time()
    }
    
    # Local Anomaly Detection (The Edge logic)
    if data["heart_rate"] > 150:
        print(f"!!! CRITICAL ALERT: High Heart Rate detected at Edge: {data['heart_rate']} !!!")
    
    # Publish to the Cloud
    myMQTTClient.publish("health/vitals", json.dumps(data), 1)
    time.sleep(1) # Send every second
# StreamLine - Cloud Brain Triage
# This script runs on an AWS EC2 instance and processes incoming medical telemetry.
# It simulates a high-level triage analysis (LLM-style) and broadcasts results.

import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Your unique AWS IoT Endpoint
ENDPOINT = "al312bhfmjvjc-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "StreamLine_Cloud_Brain"

# Topics
INPUT_TOPIC = "health/vitals"    # Incoming data from the Edge Node (Laptop)
TRIAGE_TOPIC = "health/triage"   # Outgoing data for the Clinician Dashboard

# Certificate File Paths (Must be in the same directory)
PATH_TO_ROOT_CA = "AmazonRootCA1.pem"
PATH_TO_CERT = "certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "private.pem.key"

# ==========================================
# 2. THE TRIAGE BRAIN (Simulated LLM Logic)
# ==========================================
def analyze_vitals(data):
    """
    Simulates high-level triage logic. In a production system, 
    this data would be processed by a medical-grade LLM or expert system.
    """
    hr = data.get("heart_rate", 0)
    
    if hr > 120:
        return {"level": 2, "status": "URGENT", "msg": "Potential Tachycardia detected. Assign to immediate triage."}
    elif hr > 100:
        return {"level": 3, "status": "STABLE-ELEVATED", "msg": "Elevated heart rate. Monitor trends for deterioration."}
    else:
        return {"level": 5, "status": "NORMAL", "msg": "Vitals within expected range. Routine monitoring."}

# ==========================================
# 3. MQTT SETUP & CALLBACK
# ==========================================
myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(PATH_TO_ROOT_CA, PATH_TO_PRIVATE_KEY, PATH_TO_CERT)

# Network stability: Wait up to 10 seconds for AWS handshake
myMQTTClient.configureMQTTOperationTimeout(10) 

def on_message_received(client, userdata, message):
    # Decode the incoming telemetry from the Edge
    payload = json.loads(message.payload)
    print(f"\n[INCOMING] Received vitals from Edge: {payload}")
    
    # Execute Triage Logic
    triage = analyze_vitals(payload)
    
    # Prepare the dashboard broadcast
    dashboard_report = {
        "patient_id": payload.get("patient_id", "Unknown"),
        "triage_level": triage["level"],
        "status": triage["status"],
        "recommendation": triage["msg"],
        "timestamp": time.time()
    }
    
    # PUBLISH to the triage topic (QoS 0 for fast, non-blocking delivery)
    myMQTTClient.publish(TRIAGE_TOPIC, json.dumps(dashboard_report), 0)
    print(f"[OUTGOING] Triage Decision Published to {TRIAGE_TOPIC}: Level {triage['level']}")

# ==========================================
# 4. EXECUTION
# ==========================================
print("Connecting StreamLine Cloud Brain to AWS IoT Core...")
try:
    myMQTTClient.connect()
    print(f"Connection Successful. Subscribing to {INPUT_TOPIC}...")
    myMQTTClient.subscribe(INPUT_TOPIC, 1, on_message_received)

    print("\n--- StreamLine Cloud Brain is LIVE ---")
    print("Listening for patient data and broadcasting triage levels.")
    print("Press Ctrl+C to shut down safely.")

    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down Cloud Brain. Goodbye!")
    myMQTTClient.disconnect()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
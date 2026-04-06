# StreamLine: Hybrid Edge-Cloud Medical Triage Framework

**StreamLine** is a medical IoT prototype designed to balance **real-time responsiveness** and **global intelligence**. It implements a hybrid architecture where life-critical alerts are handled at the "Edge" (local device), while complex triage and trend analysis are performed in the "Cloud" (AWS EC2).

## Key Features

  * **Local Anomaly Detection:** Real-time heart rate monitoring with instant alerts (Low Latency).

  * **Cloud-Native Triage:** Automated patient prioritization using simulated LLM logic.

  * **Secure Data Pipeline:** Mutual TLS (mTLS) encryption using X.509 certificates via MQTT over Port 8883.

  * **De-identified Privacy:** Patient data is anonymized before transmission to maintain high data privacy standards.

## Technical Architecture

1.  **Edge Node (Laptop):** Simulates a medical sensor. Detects immediate crises (e.g., HR \> 150) locally to ensure safety during network outages.

2.  **AWS IoT Core:** Acts as the secure message broker for encrypted telemetry.

3.  **Cloud Brain (EC2):** A Python-based intelligence hub that subscribes to telemetry, performs triage, and publishes results to a clinician dashboard.

## Prototype Evidence

### 1\. Edge Layer Responsiveness

The Edge node detects a heart rate spike and issues a local critical alert without waiting for a cloud response.

![Prototype Evidence #1 (Edge Layer)](https://raw.githubusercontent.com/ritzbizkit/StreamLine-Medical-IoT/main/Prototype%20Evidence%20%231%20(Edge%20Layer).png)


### 2\. Cloud Intelligence (Triage)

The EC2 server receives the raw data and "upgrades" it into an actionable Triage Level recommendation.

\<comment-tag id="2"\>\> *Evidence of Global Intelligence and LLM-style decision making.*\</comment-tag id="2" text="Since you have a great screenshot of the Cloud Brain's decision logs, you should embed the image directly here using Markdown syntax. This provides immediate technical validation for your claims about 'Global Intelligence'.


### 3\. AWS Infrastructure Verification

Verification of the running EC2 instance providing the centralized clinical decision support.

\<comment-tag id="3"\>\> *Proof of cloud-native deployment on AWS.*\</comment-tag id="3" text="Embedding the infrastructure summary screenshot here completes the proof of your deployment. It confirms the instance is running and shows the public IP used in your scripts.


## Implementation Details

  * **Protocol:** MQTT (WSS/mTLS)

  * **Cloud Provider:** AWS (IoT Core, EC2)

  * **Security:** X.509 Certificates (Root CA, Device Cert, Private Key)

  * **Language:** Python 3.9+

### How to Run

1. Ensure AWS IoT certificates are present in the project root.
2. Update the `ENDPOINT` in both scripts to match your AWS IoT Endpoint.
3. Run the Cloud Brain: `python3 cloud_triage.py`
4. Run the Edge Sensor: `python edge_sensor.py`

## Academic Project Statement

This project was developed as a technical prototype to demonstrate the efficacy of distributed medical systems. It showcases the integration of IoT security, edge computing, and cloud-based analytics.


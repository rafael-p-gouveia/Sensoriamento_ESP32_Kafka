
#include <WiFi.h>
#include <PubSubClient.h>
#include <random>
#include <Math.h>
#include "DHT.h"

// Specify data and clock connections and instantiate DHT object

#define DHTPIN 4
#define DHTTYPE DHT22   // DHT 22, or DHT 11
DHT dht(DHTPIN, DHTTYPE);

// Configuration of Wi-Fi
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Configuration of MQTT server
const char* mqtt_server = "mqtt.eclipseprojects.io";
const int mqtt_port = 1883;
const char* mqtt_user = "NOME_DE_USUARIO_MQTT";
const char* mqtt_password = "SENHA_MQTT";
const char* mqtt_topic = "climateInfo";

// Create an object of WiFi client
WiFiClient wifiClient;

// Create an object of MQTT Client
PubSubClient mqttClient(wifiClient);

// Function to connect to WiFi
void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
      Serial.print(".");
      delay(100);
  }
  Serial.println("");
  Serial.println("Conectado à rede Wi-Fi com sucesso");
}

// Function to connect to MQTT broker
void connectToMQTT() {
  mqttClient.setServer(mqtt_server, mqtt_port);

  Serial.print("Conectando ao broker MQTT");
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP32Client")) {
      Serial.println("");
      Serial.println("Conectado ao broker MQTT com sucesso");
    } else {
      Serial.print(".");
      delay(1000);
    }
  }
}

// Function to get the data of Sensor and send by MQTT
void sendData() {

  // Read values from the sensor
  float humi = dht.readHumidity();
  float temp = dht.readTemperature();

  // Format the data streaming
  String data = "T: " + String(temp, 3) + " U: " + String(humi, 3) + " E002";

  // Publish in MQTT broker
  mqttClient.publish(mqtt_topic, data.c_str());
  Serial.println("MQTT publicou: " + data);

  // Delay to send another data
  delay(3000);
}

// Setup of code
void setup() {
  dht.begin();
  Serial.begin(9600);
  connectToWiFi();
  mqttClient.setBufferSize(512);
  connectToMQTT();
}

// Loop of code
void loop() {

  // If the connection was closed, try connect again
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  sendData();
  mqttClient.loop();
}

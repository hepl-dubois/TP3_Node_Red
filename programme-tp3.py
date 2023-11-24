import network
import usocket as socket
import urequests
from machine import Pin
import time

# WiFi Configuration
# Replace the following values with your WiFi credentials
WIFI_SSID = 'VOO-H1D8M01_EXT'
WIFI_PASSWORD = 'L2ydCXk6HCGqqJC49s'

# Server Configuration
# Replace the following values with the IP address and port of your server
SERVER_IP = '192.168.0.41'
TCP_PORT = 5000
UDP_PORT = 5070

# LED Configuration
LED_PIN = 2
led = Pin(LED_PIN, Pin.OUT)

def connect_wifi(ssid, password):
    # Connect to the WiFi network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to Wi-Fi:', ssid)

def send_tcp_data(data):
    try:
        # Create a TCP socket and connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(SERVER_IP, TCP_PORT)[0][-1]
        print("Server address:", addr)

        print("Connecting to server...")
        s.connect(addr)
        print("Connected to server. Sending data:", data)
        s.sendall(str(data).encode())
        s.close()
        print("Data sent successfully.")
    except Exception as e:
        print("Error sending TCP data:", e)

def send_udp_data(data):
    try:
        # Create a UDP socket and send data to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.getaddrinfo(SERVER_IP, UDP_PORT)[0][-1]
        s.sendto(str(data).encode(), addr)
        s.close()
    except Exception as e:
        print("Error sending UDP data:", e)

def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)

    data_to_send = 0

    while True:
        led.value(1)  # Turn on the LED before sending data

        # Send data over the TCP socket
        send_tcp_data(data_to_send)

        # Send data over the UDP socket
        send_udp_data(data_to_send)

        led.value(0)  # Turn off the LED after sending data

        time.sleep(0)  # Add a delay based on your sending frequency
        data_to_send += 1

if __name__ == "__main__":
    main()

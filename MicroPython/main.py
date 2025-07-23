import network
import urequests
from time import sleep
from picozero import  pico_led
import hidden

def ConnectToWifi(ssid:str, password:str): # Checks if the data can connect
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    passedTime = 0
    while True:
        if passedTime > 10:
            print("Connection Took too long")
            
            return None
        
        if wlan.isconnected():
            print("Connected")
            
            pico_led.on()
            sleep(1)
            pico_led.off()
            
            ip = wlan.ifconfig()[0]
            return ip
        else:
            print('Waiting for connection...')
        
            pico_led.on()
            sleep(0.2)
            pico_led.off()
            sleep(0.2)
            passedTime += 0.4

def SendPostRequest(url, data, headers):
    try:
        response = urequests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("It is a success! All data has been sent")
        else:
            print("Status code:", response.status_code)
        
        response.close()
    except Exception as e:
        print("Failed to send POST request:", e)

def GetDataFromMessage(message:str) -> dict:
    return {"content": message}

def GetJSONHeader() -> dict:
    return {"Content-Type": "application/json"}

ip = ConnectToWifi(hidden.ssid, hidden.password)
for i in range(1):
    ip = ConnectToWifi(hidden.ssid, hidden.password)
    SendPostRequest(hidden.webpageURL, GetDataFromMessage("This is an automated message"), GetJSONHeader())
    sleep(1)






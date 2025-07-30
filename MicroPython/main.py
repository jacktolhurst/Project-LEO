import network
import urequests
from time import sleep
from picozero import pico_led
import json
from machine import Pin
import utime

led = Pin(15, Pin.OUT)

def ConnectToWifi(ssid:str, password:str, attemps:int=5) -> bool:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    connected = False
    for attempt in range(attemps):
        if wlan.isconnected():
            connected = True
            break
        sleep(0.1)
    
    return connected

def SendPostRequest(url:str, data:str, headers:str) -> bool:
    try:
        response = urequests.post(url, json=AddContentToData(data), headers=headers)
        if response.status_code == 200:
            return True
        else:
            print("Status code:", response.status_code)
            return False
        
    except Exception as e:
        print("Failed to send POST request:", e)
        return False

def GetCurrNetworks() -> list:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    foundNetworks = [currNetwork[0].decode('utf-8') for currNetwork in wlan.scan()]
    return foundNetworks

def CheckKnownNetworks(currentNetworks:list) -> str:
    try:
        with open("Data/KnownConnections.json", "r") as file:
            data = json.load(file)
    except:
        print("File could not be opened")
        return None

    for ssid in data.keys():
        if ssid in currentNetworks:
            return ssid
    return None

def GetPasswordFromName(name:str) -> str:
    try:
        with open("Data/KnownConnections.json", "r") as file:
            data = json.load(file)
    except:
        print("File could not be opened")
        return None
    
    return data[name]

def AddContentToData(message:str) -> dict:
    return {"content": message}

def GetJSONHeader() -> dict:
    return {"Content-Type": "application/json"}

led.value(1)

currentNetworks = GetCurrNetworks()
networkName = CheckKnownNetworks(currentNetworks)
if networkName:
    networkPassword = GetPasswordFromName(networkName)
    if ConnectToWifi(networkName, networkPassword, 10):
        with open("Data/WebsiteUrls.json", "r") as file:
            data = json.load(file)

        for url in data:
            print(SendPostRequest(url, "I love my wife", GetJSONHeader()))
else:
    print("No network could be accessed")

led.value(0)
sleep(2)





import network
import urequests
from time import sleep
from picozero import pico_led
import json
from machine import Pin
import utime
import time
import gc
import ntptime

button = Pin(15, Pin.IN, Pin.PULL_UP)
redLed = Pin(14, Pin.OUT)

UTC_OFFSET = 10 * 3600 # australia is UTC +10, change according to country

def SendCode(led, weight:int): # 2 means error occured, 3 means start of process
    for i in range(weight):
        led.value(0)
        sleep(0.1)
        led.value(1)
        sleep(0.1)
    led.value(0)

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

def SendPostRequest(url:str, data:str, headers:dict) -> bool:
    try:
        response = urequests.post(url, data=json.dumps(AddContentToData(data)), headers=headers)
        if str(response.status_code).startswith("2"):
            response.close()
            return True
        else:
            response.close()
            return False
        
    except Exception as e:
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
        return None
    
    return data.get(name)

def AddContentToData(message:str) -> dict:
    return {"content": message}

def GetJSONHeader() -> dict:
    return {"Content-Type": "application/json"}

def FormatNumber(number:int) -> str:
    return f"{number:02}" if number < 10 else str(number)

def ConnectToCurrentNetworks(attempts:int=15) -> bool:
    gc.collect()
    currentNetworks = GetCurrNetworks()
    print(currentNetworks)
    networkName = CheckKnownNetworks(currentNetworks)
    networkPassword = GetPasswordFromName(networkName)
    if networkName and networkPassword:
        return ConnectToWifi(networkName, networkPassword, attempts)
    else:
        return False

def SendData(text:str) -> bool:
    gc.collect()
    
    with open("Data/WebsiteUrls.json", "r") as file:
        data = json.load(file)

    success = False
    for url in data:
        if SendPostRequest(url, text, GetJSONHeader()):
            success = True
    return success


while True:
    print("--------------------")
    print("starting")
    redLed.value(1)
    sleep(1)
    connectedToWifi = ConnectToCurrentNetworks()
    if connectedToWifi:
        print("Connected To Wifi")
        sleep(1)
        ntptime.settime()
    while connectedToWifi:
        redLed.value(0)
        
        if button.value() == 0:
            print("button Pressed")
            redLed.value(1)
            
            
            localTime = time.localtime(time.time() + UTC_OFFSET)
            
            hour = localTime[3] % 12 or 12
            minute = FormatNumber(localTime[4])
            timeStamp = "am" if localTime[3] < 12 else "pm"

            SendData(f"CALL ME NOW: {hour}:{minute}{timeStamp}")
            redLed.value(0)
        
        connectedToWifi = network.WLAN(network.STA_IF).isconnected()
        utime.sleep(1)






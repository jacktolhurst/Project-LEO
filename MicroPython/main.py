import network
import urequests
from time import sleep
from picozero import  pico_led
import hidden

def ConnectToWifi(ssid:str, password:str, attempts:int=50): # Checks if the data can connect
    pico_led.on()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    for i in range(attempts):
        if wlan.isconnected():
            pico_led.off()
            
            print("Connected")
            
            hidden.lastUsedNetwork = (ssid, password)
            
            ip = wlan.ifconfig()[0]
            return ip
        else:
            print('Waiting for connection... ' + str(i+1))

            sleep(0.1)
    
    pico_led.off()
    print("Connection Took too long")
    return None

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

def ConnectToAllNetworks():
    currNetworks = GetCurrentNetworks()
    print(currNetworks)
    
    ip = None
    for networkName in currNetworks:
        for password in hidden.knownPasswords:
            sleep(0.1)
            ip = ConnectToWifi(networkName, password)
            
            if ip != None:
                break
    
    return ip

def GetCurrentNetworks() -> list[str]:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    foundNetworks = [currNetwork[0].decode('utf-8') for currNetwork in wlan.scan()]
    return foundNetworks

def GetDataFromMessage(message:str) -> dict:
    return {"content": message}

def GetJSONHeader() -> dict:
    return {"Content-Type": "application/json"}

ip = ConnectToWifi(hidden.lastUsedNetwork[0],hidden.lastUsedNetwork[1], 50)
if ip == None:
    ip = ConnectToAllNetworks()

if ip == None:
    print("A connection could not be made")
else:
    SendPostRequest(hidden.webpageURL, GetDataFromMessage("MEOWWW"), GetJSONHeader())






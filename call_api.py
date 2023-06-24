import requests

base_url = "http://192.168.1.178:5000"

def switch():
    url = base_url + "/lightswitch"
    data = {"light_name": "OwenColour"}
    requests.post(url, data=data)

def turn(is_on):
    url = base_url + "/turnlight"
    data = {"light_name": "OwenColour", "is_on": is_on}
    requests.post(url, data=data)

def color():
    url = base_url + "/lightcolor"
    data = {"light_name": "OwenColour", "red": 255, "green": 255, "blue": 255}
    requests.post(url, data=data)

def getlights():
    url = base_url + "/getlights"
    response = requests.post(url)
    print(response.json())
    for k, v in response.json().items():
        print(k)
        print(v)

def lightinfo():
    response_json = requests.post("http://192.168.1.178:5000/lightinfo", data={"light_name": "OwenBedroo"}).json()
    print(response_json)

if __name__ == "__main__":
    #switch()
    #turn(1)
    #color()
    #getlights()
    lightinfo()

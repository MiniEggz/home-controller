from flask import Flask, render_template, request, redirect, url_for

import os
import requests
import yaml


app = Flask(__name__)

with open(os.path.expanduser("~") + "/home-controller/config.yaml") as stream:
    config = yaml.safe_load(stream)

server_ip = config["api"]["server_ip"]
api_url = f"http://{server_ip}:5000"

light_colors = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
}

# all application routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lights")
def lights():
    lights_info = requests.post(api_url + "/getlights").json()
    return render_template("lights.html", api_route=f"{api_url}", lights=lights_info)

@app.route("/lights/<string:light_name>")
def light(light_name):
    light_info = requests.post(f"{api_url}/lightinfo", data={"light_name": light_name}).json()
    return render_template("light.html", light_colors=light_colors, light_name=light_name, **light_info)


# middleware api routes

@app.route("/lightswitch", methods=["POST"])
def lightswitch():
    requests.post(f"{api_url}/turnlight", data=request.form)
    referrer_url = request.referrer
    if referrer_url is None:
        return redirect(url_for("/lights"))
    else:
        return redirect(referrer_url)

@app.route("/lightcolor", methods=["POST"])
def lightcolor():
    light_name = request.form.get("light_name")
    requests.post(f"{api_url}/lightcolor", data=request.form)
    return redirect(f"lights/{light_name}")

@app.route("/changename", methods=["POST"])
def changename():
    new_name = request.form.get("new_name")
    requests.post(f"{api_url}/changename", data=request.form)
    return redirect(f"/lights/{new_name}")
        
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
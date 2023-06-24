import colorsys
import os

import yaml
from flask import Flask, jsonify, request
from phue import Bridge

with open(os.path.expanduser("~") + "/home-controller/config.yaml") as stream:
    config = yaml.safe_load(stream)

bridge_ip = config["api"]["bridge_ip"]

b = Bridge(bridge_ip)


def refresh_bridge():
    global b
    b = Bridge(bridge_ip)


app = Flask(__name__)


@app.route("/lightswitch", methods=["POST"])
def lightswitch():
    light_name = request.form.get("light_name")
    b.set_light(light_name, "on", not b.get_light(light_name, "on"))
    return ("", 204)


@app.route("/turnlight", methods=["POST"])
def turnlight():
    if None in request.form.values():
        return ("", 400)

    light_name = request.form.get("light_name")
    try:
        is_on = bool(int(request.form.get("is_on")))
    except:
        is_on = request.form.get("is_on").lower() == "true"

    b.set_light(light_name, "on", is_on)

    return ("", 204)


@app.route("/lightcolor", methods=["POST"])
def lightcolor():
    if None in request.form.values():
        return ("Incomplete request.", 400)

    light_name = request.form.get("light_name")
    rgb = (
        int(request.form.get("red")),
        int(request.form.get("green")),
        int(request.form.get("blue")),
    )

    if not all(0 <= val <= 255 for val in rgb):
        return ("Color values out of range.", 400)

    h, s, v = colorsys.rgb_to_hsv(*rgb)

    b.set_light(light_name, "hue", int(round(h * 65535)))
    b.set_light(light_name, "sat", int(round(s * 255)))
    b.set_light(light_name, "bri", int(round(v)))

    return ("", 204)


@app.route("/changename", methods=["POST"])
def changename():
    light_id = b.get_light_id_by_name(request.form.get("light_name"))
    b.set_light(light_id, "name", request.form.get("new_name"))
    return ("", 204)


@app.route("/getlights", methods=["POST"])
def getlights():
    lights = {light.name: light.on for light in b.lights}
    return (jsonify(lights), 200)


@app.route("/lightinfo", methods=["POST"])
def lightinfo():
    refresh_bridge()
    light_name = request.form.get("light_name")
    light = b.get_light_objects("name").get(light_name)

    if light is None:
        return (jsonify({"found": False}), 200)

    return (
        jsonify(
            {
                "found": True,
                "is_on": light.on,
                "color_capability": light.type == "Extended color light",
            },
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

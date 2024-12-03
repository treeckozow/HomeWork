from flask import Flask
import json

web = Flask(__name__)

@web.route("/")
def welcome():
    return "Welcome to my system, Please login"

@web.route("/login/<name>")
def login(name):
    try:
        with open(r"C:\Users\treec\Desktop\forward\Docker\config.json") as config:
            names_list = json.load(config)
    except:
        return "Error: Config file missing"
    if name in names_list:
        return "Access Granted"
    return "Access Denied"

if __name__ == "__main__":
    web.run(host="127.0.0.1", port=80)
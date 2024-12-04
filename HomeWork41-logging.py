from flask import Flask
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(funcName)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("web.log"),
        logging.StreamHandler()
        ]
    )

web = Flask(__name__)

@web.route("/")
def welcome():
    logging.info("User has accessed the path '/'")
    return "Welcome to my system, Please login"

@web.route("/login/<name>")
def login(name):
    try:
        with open("config.json") as config:
            names_list = set(json.load(config))
    except:
        logging.critical("Error: Config file missing")
        return "Error: Config file missing"
    if name in names_list:
        logging.info("User " + name + " has accessed the login page, permission granted")
        return "Access Granted"
    logging.warning("User " + name + " has accessed the login page, permission denied")
    return "Access Denied"

if __name__ == "__main__":
    web.run(host=os.environ.get("HOST_IP"), port=80)
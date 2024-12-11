from flask import Flask
import json
import os
import logging
import printColors

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
    return printColors.printBlack("Welcome to my system, Please login")

@web.route("/login/<name>")
def login(name):
    if name in names_set:
        logging.info("User " + name + " has accessed the login page, permission granted")
        return printColors.printGreen("Access Granted")
    logging.warning("User " + name + " has accessed the login page, permission denied")
    return printColors.printRed("Access Denied")

@web.route("/addname/<name>")
def addName(name):
    global names_set
    names_list.append(name)
    print(names_list)
    modifyJson(names_list)
    names_set = set(names_list)
    return printColors.printGreen('Name "' + name + '" added successfully')

def modifyJson(allowed_list):
    with open("config.json", "w") as config:
        json.dump(allowed_list, config, indent=4)

try:
    with open("config.json") as config:
        names_list = json.load(config)
        names_set = set(names_list)
    logging.info("Allowed names: " + str(names_list))
except:
    logging.critical("Error: Config file missing")

if __name__ == "__main__":
    web.run(host=os.environ.get("HOST_IP"), port=80)
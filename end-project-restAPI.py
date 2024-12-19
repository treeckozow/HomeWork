from flask import Flask, request, jsonify

app = Flask(__name__)

tasks={}
ID = 0

def isTaskValid(my_task):
    if not my_task or "title" not in my_task or "description" not in my_task:
        return False
    return True

def taskInvalidError():
    return jsonify({"error": "Bad Request, data must include 'title' and 'description'"}), 400

def notFoundError():
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["GET"])
def getTasks():
    return jsonify(tasks), 200

@app.route("/tasks", methods=["POST"])
def createTask():
    global ID
    task = request.get_json()
    if not isTaskValid(task):
        return taskInvalidError()
    ID += 1
    task["completed"] = False
    task["id"] = ID
    tasks[ID] = task
    return jsonify(task), 201 

@app.route("/tasks/<int:task_id>", methods=["GET"])
def getTaskById(task_id):
    if task_id in tasks:
        return jsonify(tasks[task_id]), 200
    return notFoundError()

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def modifyTask(task_id):
    if task_id in tasks:
        task = request.get_json()
        if not isTaskValid(task):
            return taskInvalidError()
        tasks[task_id]["title"] = task["title"]
        tasks[task_id]["description"] = task["description"]
        return jsonify(tasks[task_id]), 200
    return notFoundError()

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def deleteTask(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({"message":"Task deleted successfully"}), 200
    return notFoundError()

@app.route("/tasks/<int:task_id>/complete", methods=["GET"])
def markAsComplete(task_id):
    if task_id in tasks:
        if tasks[task_id]["completed"]:
            return jsonify({"message": "Task is already marked as completed", "task": tasks[task_id]}), 200
        tasks[task_id]["completed"] = True
        return jsonify({"message": "Task marked as completed", "task": tasks[task_id]}), 200
    return notFoundError()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
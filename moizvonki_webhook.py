from flask import Flask, request, jsonify

app = Flask(__name__)


def retrive_call_info(data):
    db_call_id = data.get("event").get("db_call_id")
    manager_id = data.get("webhoot").get("user_id")
    manager_login = data.get("webhoot").get("user_login")
    manager_name = data.get("event").get("user_name")
    client_number = data.get("event").get("client_number")
    client_name
    duration
    answered
    direction
    start_time
    answer_time
    end_time
    recording
    waiting_sec




@app.route("/call_finish", methods=["POST"])
def get_data():
    print(request.json)
    return jsonify({"status": "success"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4455)
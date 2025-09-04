from flask import Flask, request, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
from database import Database

database = Database()

app = Flask(__name__)



def retrieve_call_info(data):
    event = data.get("event", {})
    webhook = data.get("webhook", {})

    def datetime_format(value):
        dt = datetime.fromtimestamp(value, tz=ZoneInfo("Asia/Tashkent")) if value else None
        return dt
        

    start_time = datetime_format(event.get("start_time"))
    answer_time = datetime_format(event.get("answer_time"))
    end_time = datetime_format(event.get("end_time"))

    direction = event.get("direction")
    if direction == 0:
        direction = "incoming"
    else:
        direction = "outgoing"


    if event.get("answered") == 1:
        waiting_sec = int((answer_time - start_time).total_seconds())
    else:
        waiting_sec = int((end_time - start_time).total_seconds())
    if waiting_sec > 1:
        waiting_sec -= 2


    return {
        "db_call_id": event.get("db_call_id"),
        "manager_id": webhook.get("user_id"),
        "manager_login": webhook.get("user_login"),
        "manager_name": event.get("user_name"),
        "client_number": event.get("client_number"),
        "client_name": event.get("client_name"),
        "duration": event.get("duration"),
        "answered": event.get("answered", 0),
        "direction": direction,
        "start_time": start_time,
        "answer_time": answer_time,
        "end_time": end_time,
        "recording": event.get("recording"),
        "waiting_sec": waiting_sec,
    }


@app.route("/call_finish", methods=["POST"])
def get_data():
    data = request.json
    call_info = retrieve_call_info(data)
    print(call_info)
    database.insert_call(call_info)


    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4455)

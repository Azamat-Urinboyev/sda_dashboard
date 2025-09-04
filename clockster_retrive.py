import requests
from datetime import datetime, date
import mysql.connector


class Clockster:
    def __init__(self) -> None:
        self.token = "100|foGtHp6updGcwqe3DozNDo7jLkckac9EKRsNOGmg64c39db4" 
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://api.clockster.com/company/v2"

    def get_all_employees(self):
        url = f"{self.base_url}/users"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching employees: {response.text}")

        data = response.json()["data"]
        return {f"{u['first_name']} {u['last_name']}": u["id"] for u in data}


    def get_attendance_by_ids(self, employees, date_str):
        ids = ",".join(map(str, employees.values()))
        url = f"{self.base_url}/attendance"
        params = {
            "per_page": 1000,
            "date_start": date_str,
            "date_end": date_str,
            "users": ids,
        }

        response = requests.get(url=url, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching attendance: {response.text}")

        data = response.json()["data"]
        result = self._format_attendance(data=data, employees=employees)
        return result

    def _format_attendance(self, data: list, employees):
        users = {name: {"clock-in": None, "clock-out": None} for name in employees.keys()}

        for user in data:
            user_name = f"{user['user']['first_name']} {user['user']['last_name']}".strip()
            time_str = user["datetime"]
            datetime_obj = datetime.fromisoformat(time_str)
            time = datetime_obj.strftime("%H:%M")

            if users[user_name]["clock-in"] is None:
                users[user_name]["clock-in"] = time
                users[user_name]["clock-out"] = time
            else:
                if time < users[user_name]["clock-in"]:
                    users[user_name]["clock-in"] = time
                elif time > users[user_name]["clock-out"]:
                    users[user_name]["clock-out"] = time

        return users


def save_to_mysql(attendance_data, target_date):
    conn = mysql.connector.connect(
        host="localhost",       # change if remote
        user="root",            # your MySQL username
        password="yourpassword", # your MySQL password
        database="attendance_db" # your database name
    )
    cursor = conn.cursor()

    # CREATE TABLE attendance (
    #   id INT AUTO_INCREMENT PRIMARY KEY,
    #   employee_name VARCHAR(100),
    #   clock_in TIME NULL,
    #   clock_out TIME NULL,
    #   date DATE
    # );

    for name, times in attendance_data.items():
        clock_in = times["clock-in"]
        clock_out = times["clock-out"]

        sql = """
        INSERT INTO attendance (employee_name, clock_in, clock_out, date)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (name, clock_in, clock_out, target_date))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    c = Clockster()


    employees = c.get_all_employees()


    today = date.today().strftime("%Y-%m-%d")

    attendance = c.get_attendance_by_ids(employees, today)

    save_to_mysql(attendance, today)

    print(f"Attendance for {today} saved into MySQL!")

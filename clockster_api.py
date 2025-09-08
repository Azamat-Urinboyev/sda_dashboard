import requests
from datetime import datetime

from config import CLOCKSTER_TOKEN, CLOCKSTER_SALES_DEPARTMENT_ID



class Clockster:
    def __init__(self) -> None:
        self.token = CLOCKSTER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json',
        }
        self.base_url = "https://api.clockster.com/company/v2"


    def _get_sales_department_employees(self):
        url = f"{self.base_url}/users"
        params = {
            "per_page": 50,
            "departments": str(CLOCKSTER_SALES_DEPARTMENT_ID)
        }

        response = requests.get(url=url, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error: {response}")
        data = response.json()["data"]
        employees = {}
        for user in data:
            name = f"{user['first_name']} {user['last_name']}".strip()
            employees[name] = user["id"]
        return employees



    def get_attandance_by_date(self, date):
        employees = self._get_sales_department_employees()
        ids = [ids for name, ids in employees.items()]
        ids = ",".join(map(str, ids))

        url = f"{self.base_url}/attendance"
        params = {
            "per_page": 1000,
            "date_start": date,
            "date_end": date,
            "users": ids
        }

        response = requests.get(url=url, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error: {response}")
        data = response.json()["data"]
        result = self._format_attendance(data=data, employees=employees)
        return result
    


    def _format_attendance(self, data: list, employees):
        users = {}
        for name, id in employees.items():
            users[name] = {
                    "clock-in": None,
                    "clock-out": None
                }
        for user in data:
            user_name = f"{user['user']['first_name']} {user['user']['last_name']}".strip()
            time = user["datetime"]
            datetime_obj = datetime.fromisoformat(time)
            time = datetime_obj.strftime("%H:%M")
            if users[user_name]["clock-in"] == None:
                users[user_name] = {
                    "clock-in": time,
                    "clock-out": time
                }
            else:
                if time < users[user_name]["clock-in"]:
                    users[user_name]["clock-in"] = time
                elif time > users[user_name]["clock-out"]:
                    users[user_name]["clock-out"] = time

        return users

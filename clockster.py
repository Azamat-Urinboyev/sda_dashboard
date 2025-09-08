from apscheduler.schedulers.blocking import BlockingScheduler
from log_config import logger
from clockster_api import Clockster
from database import Database
from datetime import datetime, timedelta



def save_yesterday_attendance():
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    attendance = clockster.get_attandance_by_date(yesterday)
    attendance_list = []
    for name, times in attendance.items():
        attendance_list.append((
            name,
            yesterday,
            times["clock-in"],
            times["clock-out"]
        ))
    
    db.insert_attendance(attendance_list)



if __name__ == "__main__":
    clockster = Clockster()
    db = Database()

    scheduler = BlockingScheduler()


    scheduler.add_job(
        save_yesterday_attendance,
        trigger="cron",
        hour=1,
        day_of_week="mon-sat",
    )

    try:
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
        pass
import time
import threading
from datetime import datetime, timedelta

try:
    from plyer import notification
except ImportError:
    notification = None

# CONFIGURATION
BREAK_INTERVAL_MINUTES = 30
HYDRATION_INTERVAL_MINUTES = 20
CHECK_INTERVAL_SECONDS = 30
#placeholder for tasks function
tasks = []

# NOTIFICATION FUNCTION
def send_notification(title, message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {title}: {message}")

    if notification:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

# TASK CHECKER
def check_tasks():
    while True:
        now = datetime.now()

        for task in tasks:
            time_left = task["deadline"] - now

            # Notify if deadline is near (within 10 minutes)
            if timedelta(minutes=0) < time_left <= timedelta(minutes=10):
                send_notification(
                    "⚠️ Upcoming Deadline",
                    f"{task['name']} due in {int(time_left.total_seconds() // 60)} minutes"
                )

            # Notify if overdue
            elif time_left <= timedelta(seconds=0):
                send_notification(
                    "❌ Task Overdue",
                    f"{task['name']} is past deadline!"
                )

        time.sleep(CHECK_INTERVAL_SECONDS)

# BREAK REMINDER
def break_reminder():
    while True:
        time.sleep(BREAK_INTERVAL_MINUTES * 60)
        send_notification(
            "🧘 Take a Break",
            "You've been working for a while. Take a short break!"
        )

# HYDRATION REMINDER
def hydration_reminder():
    while True:
        time.sleep(HYDRATION_INTERVAL_MINUTES * 60)
        send_notification(
            "💧 Hydrate",
            "Time to drink some water!"
        )

# MAIN FUNCTION
def main():
    send_notification("System Started", "Task & Health Reminder is now running.")

    threading.Thread(target=check_tasks, daemon=True).start()
    threading.Thread(target=break_reminder, daemon=True).start()
    threading.Thread(target=hydration_reminder, daemon=True).start()

    # Timer (delays execution by 1second in real time) and keeps the program alive 
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

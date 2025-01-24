import os
import time
from datetime import datetime, timedelta
from instagrapi import Client

# Instagram credentials
USERNAME = "lapo_6090"
PASSWORD = "thitiyakorn2564"

# Constants
BASE_MINUTE_INTERVAL = 15
NOTE_CONTROL = 0.5

# Target birthday (update with the desired date)
BIRTHDAY = datetime(2025, 2, 1, 0, 0, 0)  # YYYY, MM, DD, HH, MM, SS

# Utility Functions
def generate_cookie(USERNAME, PASSWORD):
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(f"{USERNAME}.json")

def round_to_base(number, base, control):
    rounded = round(number / base) * base
    difference = number - rounded
    if abs(difference) > control * base:
        rounded += base if difference > 0 else -base
    return rounded

def calculate_time_difference(target_time):
    now = datetime.now()
    remaining = target_time - now
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds

def format_countdown(days, hours, minutes, seconds):
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = 'Next check on {:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1

def send_note(note_text):
    cl = Client()
    cl.load_settings(f"{USERNAME}.json")
    cl.login(USERNAME, PASSWORD)
    print(f"Posting: {note_text}")
    cl.create_note(note_text, 0)
    return f"Note posted: {note_text}"

# Main Script
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{USERNAME}.json")):
    print("Using existing cookies")
else:
    generate_cookie(USERNAME, PASSWORD)
    print("Cookies generated")

previous_note_text = None

while True:
    days, hours, minutes, seconds = calculate_time_difference(BIRTHDAY)

    if days < 0:
        print("The birthday has already passed!")
        break

    countdown_text = format_countdown(days, hours, minutes, seconds)
    note_text = f"Countdown to birthday: {countdown_text}! 🎉"

    if previous_note_text != note_text:
        print(send_note(note_text))
        previous_note_text = note_text
    else:
        countdown(900)  # Wait 15 minutes before the next update

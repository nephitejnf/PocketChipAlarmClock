import urllib
from tkinter import *
from tkinter.font import Font as tkFont
import time
from datetime import datetime
from pytz import timezone
from threading import Thread
import pygame
import os
from tzlocal import get_localzone

setHour = 0
setMinute = 0
setSeconds = 0
set_meridiem = ""
snowHour = 0
snowMinute = 0
snowMeridiem = "AM"
tz = get_localzone()
alarmLocation = "LukHash_-_ARCADE_JOURNEYS.mp3"

def stop_alarm(event = None):
  setHour = -1    #Prevents alarm from keep going off
  pygame.mixer.music.stop()
  pygame.mixer.quit()

def get_time():
  hour = datetime.now(timezone(str(tz))).hour
  minute = datetime.now(timezone(str(tz))).minute
  second = datetime.now(timezone(str(tz))).second

  global setHour
  global setMinute
  global setSeconds
  global set_meridiem
  global snowHour
  global snowMinute
  global snowMeridiem

  if hour > 12:
    hour = hour - 12
    meridiem = "PM"
  elif hour == 12:
    meridiem = "PM"
  elif hour == 0:
    hour = hour + 12
    meridiem = "AM"
  else:
    meridiem = "AM"

  if hour == setHour and minute == setMinute and second == setSeconds and set_meridiem == meridiem:
    setHour = -1
    thread = Thread(target = alarm)
    thread.start()

  return (str(hour) + ':' + (str(minute) if minute >= 10 else str("0" + "" + str(minute))) + ':' + (str(second) if second >= 10 else str("0" + "" + str(second))) + str(' ' + meridiem))

the_time = 0
meridiem = ""
master = Tk()
master.wm_title("Snow Alarm")
master.bind("<space>", stop_alarm)
frame = Frame(master)
helv46 = tkFont(size = 46)
time_label = Label(frame, text = get_time, font = helv46)
#Create file if it doesn't exist
openPrefs = open("pref.dat", "a")
openPrefs.close()
openPrefs = open("pref.dat", "r")
lines = openPrefs.readlines()
print(lines)
#Fill file if nothing is present
if len(lines) < 1:
  openPrefs.close()
  openPrefs = open("pref.dat", "w")
  openPrefs.write("NoSchoolName\nNoWebsite")
  openPrefs.close()
else:
  openPrefs.close()

#Now pull school and website from file
openPrefs = open("pref.dat", "r")
lines = openPrefs.readlines()
school = lines[0]
website = lines[1]

#GUI for Raspberry Pi alarm clock

def alarm():
  global setHour
  setHour = -1
  pygame.mixer.init()
  pygame.mixer.music.load(alarmLocation)
  pygame.mixer.music.play(-1)
  while pygame.mixer.music.get_busy() == True:
    continue

def show_dialog():
  global dialog
  dialog = Tk()
  hour_label = Label(dialog, text = "Hour: ")
  hour_label.pack(fill = Y, side = LEFT)
  global hour_input
  hour_input = Entry(dialog, width = 2)
  hour_input.pack(fill = Y, side = LEFT)
  minute_label = Label(dialog, text = "Minute: ")
  minute_label.pack(fill = Y, side = LEFT)
  global minute_input
  minute_input = Entry(dialog, width = 2)
  minute_input.pack(fill = Y, side = LEFT)
  second_label = Label(dialog, text = "Second: ")
  second_label.pack(fill = Y, side = LEFT)
  global second_input
  second_input = Entry(dialog, width = 2)
  second_input.pack(fill = Y, side = LEFT)
  global option
  option = StringVar(dialog)
  option.set("AM")
  w = OptionMenu(dialog, option, "AM", "PM")
  w.pack()
  done_button = Button(dialog, text = "Ok", command = click)
  done_button.pack()

def click():
  global setHour
  global setMinute
  global setSeconds
  global set_meridiem
  global snowHour
  global snowMinute
  global snowMeridiem
  setHour = int(hour_input.get())
  setMinute = int(minute_input.get())
  setSeconds = int(second_input.get())
  set_meridiem = option.get()
  dialog.destroy()
  print(str(setHour) + " " + str(setMinute) + " " + str(setSeconds) + set_meridiem)
  if setMinute < 2:
    snowMinute = setMinute + 58
    snowHour = setHour - 1
  else:
    snowMinute = setMinute - 2
    snowHour = setHour

  if setHour == 12 and setMinute == 0 or setMinute == 1:
    snowMeridiem = "AM" if set_meridiem == "PM" else "PM"
  else:
    snowMeridiem = set_meridiem

def update_time():
  time_label.configure(text=get_time())
  master.after(500, update_time)

frame.pack(fill = BOTH, expand = 1)
the_time = StringVar()
the_time.set(get_time())
time_label.pack(fill = BOTH, expand = 1)
button = Button(frame, text = "Set Alarm", command = show_dialog, font = helv46)
button.pack(fill = BOTH, expand = 1)
#Create option menu
menubar = Menu(master)    #Main menu
settings_menu = Menu(menubar, tearoff=0) #cascading options
#add file men to main menu
menubar.add_cascade(label="Settings", menu=settings_menu)
#display menu
master.config(menu=menubar)
update_time()
#Maximize window
w, h = master.winfo_screenwidth(), master.winfo_screenheight()
master.geometry("%dx%d+0+0" % (w, h))

master.mainloop()
master.destroy()

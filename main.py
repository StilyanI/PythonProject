import PySimpleGUI as sg
import time
import threading
import winsound


class Alarm:
    def __init__(self, time, enabled, repeat):
        self.time = time
        self.enabled = enabled
        self.repeat = repeat


alarms = []
timesList = []

alarms_list = [
    [sg.Text("Alarms")],
    [sg.Listbox(timesList, enable_events=True, size=(40, 20), key="LIST")]
]

hours = []
minutes = []
for i in range(24):
    if i < 10:
        hours.append('0' + str(i))
    else:
        hours.append(str(i))
for i in range(60):
    if i < 10:
        minutes.append('0' + str(i))
    else:
        minutes.append(str(i))

alarm_settings = [
    [sg.Combo(hours, size=(10, 10), enable_events=True, readonly=True, key="IN_H"), sg.Text(":"),
     sg.Combo(minutes, size=(10, 10), enable_events=True, readonly=True, key="IN_M")],
    [sg.Checkbox("Enabled", key='ENABLED', default=True), sg.Checkbox("Repeat", key='REPEAT', default=False)],
    [sg.Button("Add"), sg.Button("Delete")]
]

layout = [
    [
        sg.Column(alarms_list),
        sg.VSeparator(),
        sg.Column(alarm_settings),
        sg.Button("Exit")
    ]
]

sg.theme('DarkAmber')
window = sg.Window("Program", layout)


def check_time():
    currTime = time.strftime("%H:%M:%S")
    while not stopFlag:
        for i in alarms:
            if i.time + ":00" == currTime and i.enabled:
                winsound.PlaySound('alarm_sound.wav', 0)
                if not i.repeat:
                    i.enabled = False
                break
        currTime = time.strftime("%H:%M:%S")
        print(currTime)
        time.sleep(1)


def update():
    window["LIST"].update(timesList)
    window["IN_H"].update("")
    window["IN_M"].update("")
    window["ENABLED"].update(True)
    window["REPEAT"].update(False)


def addAlarm(h, m, e, r):
    tmpTime = h + ":" + m
    if tmpTime in timesList:
        sg.popup_error("Alarm already exists")
    elif h == "" or m == "":
        sg.popup_error("Enter valid values")
    else:
        alarms.append(Alarm(tmpTime, e, r))
        timesList.append(tmpTime)


f = open("alarms.txt",'r')
lines = f.readlines()
for i in lines:
    j = i.split('_')
    hm = j[0].split(":")
    addAlarm(hm[0], hm[1], j[1], j[2])
f.close()

thread = threading.Thread(target=check_time)
stopFlag = False
thread.start()

while True:
    event, values = window.read()
    if event == "Add":
        addAlarm(values["IN_H"], values["IN_M"], values["ENABLED"], values["REPEAT"])
        update()
    if event == "Delete":
        tmpTime = values["IN_H"] + ":" + values["IN_M"]
        for i in alarms:
            if i.time == tmpTime:
                alarms.remove(i)
                timesList.remove(tmpTime)
                update()
    if event == "LIST":
        selectedTime = values["LIST"][0]
        for i in alarms:
            if i.time == selectedTime:
                selsectedAlarm = i
                break

        window["IN_H"].update(selsectedAlarm.time[0] + selsectedAlarm.time[1])
        window["IN_M"].update(selsectedAlarm.time[3] + selsectedAlarm.time[4])
        window["ENABLED"].update(selsectedAlarm.enabled)
        window["REPEAT"].update(selsectedAlarm.repeat)
    if event == "Exit" or event == sg.WIN_CLOSED:
        f = open("alarms.txt",'w')
        for i in alarms:
            f.write(i.time + "_" + str(i.enabled) + "_" + str(i.repeat) + "\n")
        f.close()
        break

stopFlag = True
window.close()
thread.join()

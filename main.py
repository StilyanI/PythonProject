import PySimpleGUI as sg
import os
import time
import threading
import winsound


class Alarm:
    def __init__(self, time, enabled, repeat):
        self.time = time
        self.enabled = enabled
        self.repeat = repeat


alarms = []

alarms_list = [
    [sg.Text("Alarms")],
    [sg.Listbox(alarms, enable_events=True, size=(40, 20), key="LIST")]
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
    [sg.Checkbox("Enabled", key='ENABLED', default=True), sg.Checkbox("Repeat", key='REPEAT')],
    [sg.Button("Add"), sg.Button("Delete")]
]

layout = [
    [
        sg.Menubar([["Settings"]]),
        sg.Column(alarms_list),
        sg.VSeparator(),
        sg.Column(alarm_settings),
        sg.Button("Exit")
    ]
]

settings = sg.UserSettings(filename="settings.ini", path=os.getcwd(), use_config_file=True)
sg.theme(settings["GUI"]["theme"])
window = sg.Window("Program", layout)


def check_time():
    currTime = time.strftime("%H:%M:%S")
    while not stopFlag:
        for i in alarms:
            if i.time + ":00" == currTime and i.enabled:
                winsound.PlaySound('alarm_sound.wav', 0)
        currTime = time.strftime("%H:%M:%S")
        print(currTime)
        time.sleep(1)


timesList = []
thread = threading.Thread(target=check_time)
stopFlag = False
thread.start()

while True:
    event, values = window.read()
    if event == "Add":
        tmpTime = values["IN_H"] + ":" + values["IN_M"]
        alarms.append(Alarm(tmpTime, values["ENABLED"], values["REPEAT"]))
        timesList.append(tmpTime)
        window["LIST"].update(timesList)
        print("Added:" + tmpTime + ":00")
    if event == "Delete":
        tmpTime = values["IN_H"] + ":" + values["IN_M"]
        for i in alarms:
            if i.time == tmpTime:
                alarms.remove(i)
                timesList.remove(tmpTime)
                window["LIST"].update(timesList)
    if event == "LIST":
        selectedTime = values["IN_H"] + ":" + values["IN_M"]
        values["IN_H"] = values["LIST"][0][0] + values["LIST"][0][1]
        values["IN_M"] = values["LIST"][0][3] + values["LIST"][0][4]

        window["IN_H"].update(values["LIST"][0][0] + values["LIST"][0][1])
        window["IN_M"].update(values["LIST"][0][3] + values["LIST"][0][4])
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

stopFlag = True
window.close()
thread.join()

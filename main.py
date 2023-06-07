import PySimpleGUI as sg
import os
import time
import threading


class Alarm:
    def __init__(self, hour, minute, active, repeat):
        self.hour = hour
        self.minute = minute
        self.active = active
        self.repeat = repeat


alarms = []

alarms_list = [
    [sg.Text("Alarms")],
    [sg.Listbox(alarms, enable_events=True, size=(40, 20), key="LIST")]
]

alarm_settings = [
    [sg.In(size=(20, 10), key="IN_H"), sg.Text(":"), sg.In(size=(20, 10), key="IN_M")],
    [sg.Checkbox("Repeat", key='REPEAT')],
    [sg.Button("Add")]
]

layout = [
    [
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
    currTime = time.strftime("%H:%M")
    tmpTime = currTime
    while not stopFlag:
        if currTime != tmpTime:
            print(currTime)
            tmpTime = currTime
            for i in alarms:
                if i.hour + ":" + i.minute == tmpTime:
                    # smeni tva na funkciq za alrmata
                    print("Evala bratle")
        currTime = time.strftime("%H:%M")
        time.sleep(1)


thread = threading.Thread(target=check_time)
stopFlag = False
thread.start()

while True:
    event, values = window.read()
    if event == "Add":
        alarms.append(Alarm(values["IN_H"], values["IN_M"], True, values["REPEAT"]))
        list = []
        for i in alarms:
            list.append(i.hour + ":" + i.minute)
        window["LIST"].update(list)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

stopFlag = True
thread.join()
window.close()

import PySimpleGUI as sg


class Alarm:
    def __init__(self, time, active, repeat):
        self.time = time
        self.active = active
        self.repeat = repeat


number_of_alarms = 0
alarms = []

alarms_list = [
    [sg.Text("Alarms")],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20))]
]

alarm_settings = [
    [sg.In(size=(40, 1), key="INPUT")],
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

window = sg.Window("Program", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

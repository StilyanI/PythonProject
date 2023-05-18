import PySimpleGUI as sg

alarms_list = [
    [sg.Text("Alarms")],
    [sg.Listbox(values=[],enable_events=True, size=(40,20))]
]

layout = [
    [
        sg.Column(alarms_list),
        sg.VSeparator(),
        sg.Button("Exit")
    ]
]

window = sg.Window("Program",layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
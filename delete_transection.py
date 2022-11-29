import PySimpleGUI as sg

def create(client, updated_data):
    layout = [
        [sg.Text('Please insert row no.'), sg.Input(key='-INDEX-')],
        [sg.Button('Delete'), sg.Button('Cancel')]
    ]
    addWindow = sg.Window("Delete transection", layout, modal=True)
    while True:
        event, values = addWindow.read()
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Delete':
            database = client["application"]
            collection = database["ledger"]
            index = int(values['-INDEX-'])
            query = {
                "Type": updated_data[index][0],
                "Category": updated_data[index][1],
                "Value": updated_data[index][2],
                "Comment": updated_data[index][3],
                "Month": updated_data[index][5],
                "Year": updated_data[index][6]
            }
            collection.delete_one(query)
            break
    addWindow.close()
import PySimpleGUI as sg

def get_update_data(old_data):
    category = tuple(['Salary', 'Food', 'Transport', 'Groceries', 'Cure', 'Education', 'Entertainment', 'Family', 'Insurance', 'Hobby', 'Vehicle', 'Credit card'])
    layout = [
        [sg.Text('Category'), sg.Combo(values=category, default_value=category[category.index(old_data[0][1])], readonly=True, k='-CATEGORY-')],
        [sg.Text('Value'), sg.Input(key='-INPUT-', default_text=int(old_data[0][2]))],
        [sg.Text('Comment'), sg.Input(key='-COMMENT-', default_text=old_data[0][3])],
        [sg.Button('Update'), sg.Button('Cancel')]
    ]
    addWindow = sg.Window("Edit data", layout, modal=True)
    while True:
        event, values = addWindow.read()
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Update':
            newvalue = {
                "$set": {
                    "Category": values['-CATEGORY-'],
                    "Value": int(values['-INPUT-']),
                    "Comment": values['-COMMENT-']
                }
            }
            addWindow.close()
            return newvalue
    addWindow.close()


def create(client, updated_data):
    layout = [
        [sg.Text('Please insert row no.'), sg.Input(key='-INDEX-')],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]
    addWindow = sg.Window("Edit transection", layout, modal=True)
    while True:
        event, values = addWindow.read()
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'OK':
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
            result = collection.find(query)
            data = []
            lists = []
            for dict in result:
                for key in dict:
                    if key != '_id':
                        lists.append(dict[key])
                data.append(lists)
                lists = []
            newvalue = get_update_data(data)
            collection.update_one(query, newvalue)
            break
    addWindow.close()
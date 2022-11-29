import PySimpleGUI as sg
import datetime

def create(client):
    category = tuple(['Salary', 'Food', 'Transport', 'Groceries', 'Cure', 'Education', 'Entertainment', 'Family', 'Insurance', 'Hobby', 'Vehicle', 'Credit card'])
    layout = [
        [sg.Radio('Income', "Transection_type", default=True, size=(10,1), k='-INCOME-'), sg.Radio('Expense', "Transection_type", default=False, size=(10,1), k='-EXPENSE-')],
        [sg.Text('Category'), sg.Combo(values=category, default_value=category[0], readonly=True, k='-CATEGORY-')],
        [sg.Text('Select date'), sg.Input(key='-DATE-', size=(20, 1)), sg.CalendarButton("Date", close_when_date_chosen=True, target='-DATE-', no_titlebar=False)],
        [sg.Text('Value'), sg.Input(key='-INPUT-')],
        [sg.Text('Comment'), sg.Input(key='-COMMENT-')],
        [sg.Button('Add'), sg.Button('Cancel')]
    ]
    addWindow = sg.Window("Add new transection", layout, modal=True)
    while True:
        event, values = addWindow.read()
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Add':
            if values['-INCOME-']:
                type_trans = 'Income'
            elif values['-EXPENSE-']:
                type_trans = 'Expense'
            datetimes = values['-DATE-']
            date = datetimes.split(' ')[0]
            date_lst = date.split('-')
            add_data = {
                "Type": type_trans,
                "Category": values['-CATEGORY-'],
                "Value": int(values['-INPUT-']),
                "Comment": values['-COMMENT-'],
                "DateTime": datetime.datetime(int(date_lst[0]),int(date_lst[1]),int(date_lst[2])),
                "Month": int(date_lst[1]),
                "Year": int(date_lst[0])
            }
            database = client["application"]
            collection = database["ledger"]
            x = collection.insert_one(add_data)
            break
    addWindow.close()
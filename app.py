import PySimpleGUI as sg
import add_transection
import delete_transection
import show_graph
import edit_transection
import pymongo
import datetime

def get_data(client, year, month):
    data = []
    lists = []
    database = client["application"]
    collection = database["ledger"]
    datetimes = datetime.datetime.now()
    query = { "Month": month , "Year": year}
    resultObj = collection.find(query)
    for dict in resultObj:
        for key in dict:
            if key != '_id':
                lists.append(dict[key])
        data.append(lists)
        lists = []
    return data

headings = ['Type', 'Category', 'Value', 'Comment', 'Date']

client = pymongo.MongoClient("mongodb://root:password@localhost:27017/admin?authSource=admin&authMechanism=SCRAM-SHA-1")
datetimes = datetime.datetime.now()
data = get_data(client, datetimes.year, datetimes.month)
year_lst = tuple([year for year in range(datetimes.year, datetimes.year-10, -1)])
month_lst = tuple([month+1 for month in range(12)])
balance = 0
for i in data:
    if i[0] == 'Income':
        balance += int(i[2])
    else:
        balance -= int(i[2])
layout = [
    [sg.Button('New'), sg.Button('Edit'), sg.Button('Delete'),
        sg.Text('Year'), sg.OptionMenu(values=year_lst,  k='-YEAR-', default_value=year_lst[0]),
        sg.Text('Month'), sg.OptionMenu(values=month_lst,  k='-MONTH-', default_value=datetimes.month),
        sg.Button('Search')],
    [sg.Table(
        values=data,
        headings=headings,
        max_col_width=35,
        auto_size_columns=True,
        display_row_numbers=True,
        justification='center',
        num_rows=10,
        key='-TABLE-',
        row_height=35
    )],
    [sg.Text('Total balance:'), sg.Text(balance, key='-BALANCE-'),
    sg.Button('Report')]
]
sg.theme('BlueMono')
window = sg.Window("Expense-Income record", layout)
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    elif event == 'New':
        add_transection.create(client)
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        window['-TABLE-'].Update(values=updated_data)
        balance = 0
        for i in updated_data:
            if i[0] == 'Income':
                balance += int(i[2])
            else:
                balance -= int(i[2])
        window['-BALANCE-'].Update(value=balance)
    elif event == 'Delete':
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        delete_transection.create(client, updated_data)
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        window['-TABLE-'].Update(values=updated_data)
        balance = 0
        for i in updated_data:
            if i[0] == 'Income':
                balance += int(i[2])
            else:
                balance -= int(i[2])
        window['-BALANCE-'].Update(value=balance)
    elif event == 'Search':
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        window['-TABLE-'].Update(values=updated_data)
        balance = 0
        for i in updated_data:
            if i[0] == 'Income':
                balance += int(i[2])
            else:
                balance -= int(i[2])
        window['-BALANCE-'].Update(value=balance)
    elif event == 'Report':
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        show_graph.create_plot(updated_data)
    elif event == 'Edit':
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        edit_transection.create(client, updated_data)
        updated_data = get_data(client, int(values['-YEAR-']), int(values['-MONTH-']))
        window['-TABLE-'].Update(values=updated_data)
        balance = 0
        for i in updated_data:
            if i[0] == 'Income':
                balance += int(i[2])
            else:
                balance -= int(i[2])
        window['-BALANCE-'].Update(value=balance)
window.close()
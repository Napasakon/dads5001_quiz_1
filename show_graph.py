import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec

def create_plot(updated_data):
    income = 0
    expense = 0
    income_category_name = []
    for i in updated_data:
        if i[0] == 'Income':
            income_category_name.append(i[1])
    income_category_name = list(set(income_category_name))
    income_category_value = []
    for i in income_category_name:
        income_category_value.append(0)

    expense_category_name = []
    for i in updated_data:
        if i[0] == 'Expense':
            expense_category_name.append(i[1])
    expense_category_name = list(set(expense_category_name))
    expense_category_value = []
    for i in expense_category_name:
        expense_category_value.append(0)
    for i in updated_data:
        if i[0] == 'Income':
            income += int(i[2])
            income_category_value[0] += int(i[2])
        else:
            expense += int(i[2])
            expense_category_value[expense_category_name.index(i[1])] += int(i[2])
    if income_category_value == [] and expense_category_value == []:
        return 0
    colors = ['#8ceacd', '#d95c68']
    fig = plt.figure(constrained_layout=True)
    fig.suptitle("Monthly report")
    gs = GridSpec(2, 2, figure=fig)
    axs = fig.add_subplot(gs[:, 0])
    axs2 = fig.add_subplot(gs[0, 1])
    axs3 = fig.add_subplot(gs[1, 1])
    axs.pie([income, expense], colors=colors, labels=['Income', 'Expense'], autopct='%1.2f%%')
    axs2.pie(income_category_value, labels=income_category_name, autopct='%1.2f%%')
    axs3.pie(expense_category_value, labels=expense_category_name, autopct='%1.2f%%')

    layout = [
        [sg.Canvas(size=(1500, 1000), key='-CANVAS-')]
    ]
    window = sg.Window('Monthly summary', layout, finalize=True, element_justification='center')
    figure_canvas = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().pack(side='top', fill='none', expand=1)

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Cancel':
            break
    window.close()

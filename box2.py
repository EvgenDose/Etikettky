#-*- coding: utf-8 -*-
import PySimpleGUI as sg
import os
import platform
import time
import zpl
import socket
from pr import *
ZP = zpl.zpl
code_base = []
printers =''
Host = socket.gethostname()
p = os.path.abspath('box.zpl')
sg.theme("Reddit")

if platform.system() == 'Windows':
    import win32print
    printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
    print(printers)


def my_printer_function():
    if platform.system() == 'Linux' and values['-SYSTEML-'] == True:
        print(code_base)
        for codes in code_base:
            code_str = str(codes)
            box = ZP[0] + NAME + ZP[1] + DATA + ZP[2] + KOLVO + ZP[3] + SERIA + ZP[4] + GTIN + ZP[5] + code_str + ZP[6]
            file = open("box.zpl", "w", encoding="utf-8")
            file.write(box)
            file.close()
            comand = "cat box.zpl > /dev/usb/lp0"
            print(comand)
            os.system(comand)
            time.sleep(1)
        sg.Popup('Этикетки успешно напечатаны!', keep_on_top=True)
    elif platform.system() == 'Windows' and values['-SYSTEMW-'] == True:
        print(code_base)
        for codes in code_base:
            code_str = str(codes)
            box = ZP[0] + NAME + ZP[1] + DATA + ZP[2] + KOLVO + ZP[3] + SERIA + ZP[4] + GTIN + ZP[5] + code_str + ZP[6]
            file = open("box.zpl", "w", encoding="utf-8")
            file.write(box)
            file.close()
            comand = "print /d:\\\\" + Host + "\\" + values['-IN2-'] + " " + p + ""
            print(comand)
            os.system(comand)
            time.sleep(1)
        sg.Popup('Этикетки успешно напечатаны!', keep_on_top=True)
    else:
        sg.Popup('Неверно выбрана ОС!. Выход из программы....', title='ОШИБКА!',keep_on_top=True)
        exit(1)



Input_dan = [[sg.Text("Загрузите SSCC:"),sg.Push(), sg.Input(readonly=True, size =(25, 1),key='-INPUT1-',enable_events=True),sg.FileBrowse('Открыть',key='-IN-', file_types=(("TXT Files", "*.txt"),("ALL Files", "*.*")))],
          [sg.Text("Выберите препарат:"),sg.Push(),sg.Combo(m,readonly = True,size =(32, 1), key='-INPUT2-',enable_events=True)],
          [sg.Text("Введите дату:"),sg.Push(),sg.Input(size =(15, 1),key='-INPUT3-',enable_events=True)],
          [sg.Text("Введите серию:"),sg.Push(),sg.Input(size =(15, 1),key='-INPUT4-',enable_events=True)],
          [sg.Button('Справка'),sg.Push(),sg.pin(sg.Combo(printers, readonly = True,size =(22, 1), key='-IN2-', visible=False,enable_events=True)),sg.Push(),sg.Button('Печать')],
          [sg.Push(),sg.pin(sg.Text('Не выбран принтер!', key='-PRINTER-', text_color="red", visible=False)),sg.Push()],
          [sg.Radio('Linux',"RADIO1", default=True, key='-SYSTEML-', enable_events=True),sg.Radio('Windows',"RADIO1",key='-SYSTEMW-', default=False,enable_events=True)]
             ]

Output_dan =[[sg.Text('Название препарата',key='-NAME-',size=(40, 2), enable_events=True)],
             [sg.HSeparator()],
             [sg.Text('ДАТА ПРОИЗВОДСТВА'),sg.Push(),sg.Text('00.0000', key='-DATA-',enable_events=True)],
             [sg.Text('КОЛ-ВО ЕДЕНИЦ'),sg.Push(),sg.Text('00', key='-KOLVO-',enable_events=True)],
             [sg.Text('СЕРИЯ'),sg.Push(),sg.Text('000000',key='-SERIA-',enable_events=True)],
             [sg.Text('GTIN'),sg.Push(),sg.Text('00000000000000',key='-GTIN-',enable_events=True)],
             [sg.Push(), sg.Image('odnomer.png', size=(260, 120), background_color='white'), sg.Push()],
             [sg.Push(),sg.Text("00000000000000", key='-CODE-'), sg.Push()],

]

layout = [
    [sg.Column(Input_dan),
    sg.VSeparator(),
     sg.Column(Output_dan),
     sg.VSeparator(),]
]
window = sg.Window('Восстановление этикетки', layout)

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break

    if values['-SYSTEML-'] == False and values['-SYSTEMW-'] == True:
        window['-IN2-'].update(visible=True)
        window['-PRINTER-'].update(visible=True)
    else:
        window['-IN2-'].update(visible=False)
        window['-PRINTER-'].update(visible=False)

    code_base = []

    if values['-IN2-']:
        window['-PRINTER-'].update(values['-IN2-'], text_color='green')

    if values['-INPUT1-']:
        base = open(values['-INPUT1-'])
        while True:
            code = base.readline()
            print(code)
            if not code:
                break
            code_base.append(code)
            window['-CODE-'].update(code, text_color='green')

    if values['-INPUT2-']:
        for n_pr in pr_baze:
            n_pr = ','.join(n_pr)
            if n_pr == values['-INPUT2-']:
                print(n_pr)
                n_pr = n_pr.split(',')
                NAME = n_pr[1]
                KOLVO = n_pr[2]
                GTIN = n_pr[0]
                break
        window['-NAME-'].update(NAME, text_color='green')
        window['-KOLVO-'].update(KOLVO, text_color='green')
        window['-GTIN-'].update(GTIN, text_color='green')
    DATA = values['-INPUT3-']
    SERIA = values['-INPUT4-']

    if values['-INPUT3-']:
        window['-DATA-'].update(values['-INPUT3-'], text_color='green')
    if values['-INPUT4-']:
        window['-SERIA-'].update(values['-INPUT4-'], text_color='green')

    if event == 'Печать':
        if values['-INPUT1-'] and values['-INPUT2-'] and values['-INPUT3-'] and values['-INPUT4-']:
            my_printer_function()
        else:
            sg.Popup('Загрузите SSCC и введите данные!', keep_on_top=True)
    if event == 'Справка':
        sg.Popup('1.Загрузите файл с кодами в формате txt. Кол-во кодов в файле не ограничено' '\n' '2.Выберите необходимы препарат из списка, проверьте правильно ли отобразились данные''\n''3.Введите дату производства и серию, проверьте правильность ввода''\n''4.Нажмите кнопку "печать"', title='Справка',keep_on_top=True)

window.close()

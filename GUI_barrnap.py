import PySimpleGUI as sg
import os
import subprocess

ROW_SIZE = (15, 1)


def add_option(option, default=None, size=ROW_SIZE):
    return [sg.Text(option, size=size), sg.InputText(default, key=f'-{option.upper()}-')]


def add_input_file(file_path='file.fasta', size=ROW_SIZE):
    return [sg.Text('Input file path', size=size), sg.InputText(file_path, key='-INPUT_FILE-'), sg.FileBrowse()]


def remove_pref(string):
    if string.startswith('--'):
        return string[len('--'):]
    return string


def main():
    sg.theme('Dark Blue 3')

    options_dic = {'Kingdom': 'bac', 'Threads': '1', 'Lencutoff': '0.8', 'Reject': '0.25', 'Evalue': '1e-06'}

    layout = [[sg.Text('Welcome to barrnap')], add_input_file()]
    layout.extend([add_option(*option) for option in options_dic.items()])
    layout.extend([[sg.Text('Typed command', size=ROW_SIZE), sg.InputText(key='-OUTPUT-')], [sg.Submit(), sg.Cancel()]])

    window = sg.Window('GUI barrnap application', layout, finalize=True)

    while True:
        event, values = window.read()
        if event in {sg.WIN_CLOSED, 'Cancel'}:
            break
        if event == 'Submit':
            command = ['barrnap']
            command.append(f"{values['-INPUT_FILE-']}")
            for option in options_dic:
                command.append(f"--{option.lower()} {values[f'-{option.upper()}-']}")
            arg_list = command
            command = ' '.join(command)

            window['-OUTPUT-'].update(command)
            print(command)

    window.close()
    #del window
    
    
    comm = []
    for arg in arg_list:
        comm.append(remove_pref(arg))
    print(comm)

    stream = subprocess.Popen(comm, stdout=subprocess.PIPE, encoding='utf-8')
    out = stream.stdout.read()

    layout = [[(sg.Text('Barrnap output', size=[40, 1]))],
    [sg.Output(size=(80, 20))],
    [sg.Multiline(size=(70, 5), enter_submits=True),
    sg.Button('SEE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
    sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
    sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('GUI barrnap application', layout, default_element_size=(30, 2))


    while True:
        event, value = window.read()
        if event == 'SEE':
            print(out)
        #if event == ''
        else:
            break
    window.close()

    return command


if __name__ == "__main__":
    main()

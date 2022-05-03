import PySimpleGUI as sg

ROW_SIZE = (15, 1)


def add_option(option, default=None, size=ROW_SIZE):
    return [sg.Text(option, size=size), sg.InputText(default, key=f'-{option.upper()}-')]


def add_input_file(file_path='file.fasta', size=ROW_SIZE):
    return [sg.Text('Input file path', size=size), sg.InputText(file_path, key='-INPUT_FILE-'), sg.FileBrowse()]


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
            for option in options_dic:
                command.append(f"--{option.lower()} {values[f'-{option.upper()}-']}")
            command.append(f"{values['-INPUT_FILE-']}")
            command = ' '.join(command)

            window['-OUTPUT-'].update(command)
            print(command)

    window.close()
    del window
    return command


if __name__ == "__main__":
    main()

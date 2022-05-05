#import PySimpleGUI as sg
import subprocess
import os.path

ROW_SIZE = (15, 1)


def install(package):
    subprocess.call(['pip', 'install', package])
    print('Required packages are installed')


try:
    import PySimpleGUI as sg
except ImportError:
    install('pysimplegui')
finally:
    import PySimpleGUI as sg


def add_option(option, default=None, size=ROW_SIZE):
    return [sg.Text(option, size=size), sg.InputText(default, key=f'-{option.upper()}-')]


def add_file(text, file_path=None, key=None, size=ROW_SIZE):
    return [sg.Text(text, size=size), sg.InputText(file_path, key=key), sg.FileBrowse()]


def main():
    sg.theme('Dark Blue 3')

    options_dic = {'Kingdom': 'bac', 'Threads': '1', 'Lencutoff': '0.8', 'Reject': '0.25', 'Evalue': '1e-06'}

    layout_input = [[sg.Text('Welcome to barrnap')], add_file('Input file path', 'sequence.fasta', '-INPUT_FILE-')]
    layout_input.extend([add_option(*option) for option in options_dic.items()])
    layout_input.extend([[sg.Text('Typed command', size=ROW_SIZE), sg.InputText(key='-OUTPUT-')], [sg.Submit(), sg.Cancel()]])

    window_input = sg.Window('GUI barrnap application', layout_input, finalize=True)
    window_output_active = False

    while True:
        event_input, values_input = window_input.read(timeout=100)
        if event_input in {sg.WIN_CLOSED, 'Cancel'}:
            break

        if not window_output_active and event_input == 'Submit':
            if not os.path.exists(values_input['-INPUT_FILE-']):
                text = "This file does not exist!"
                window_input['-INPUT_FILE-'].update(text)
            else:
                window_output_active = True
                command = ['barrnap']
                command.append(f"{values_input['-INPUT_FILE-']}")
                for option in options_dic:
                    command.append(f"--{option.lower()}")
                    command.append(f"{values[f'-{option.upper()}-']}")
                arg_list = command
                command = ' '.join(command)

                window_input['-OUTPUT-'].update(command)

                comm = [arg.replace('--', '') for arg in arg_list]

                stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, encoding='utf-8')
                out = stream.stdout.read()

                layout_output = [[(sg.Text('Barrnap output', size=[40, 1]))],
                                [sg.Multiline(out, size=(80, 20))],
                                [sg.Text('Output file path', size=(20,1)), sg.InputText('result.gff', key='-OUTPUT_FILE-'), sg.FileBrowse(),
                                sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                                sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

                window_output = sg.Window('GUI barrnap application', layout_output, default_element_size=(30, 2))

                while window_output_active:
                    event_output, values_output  = window_output.read()
                    if event_output == 'SAVE':
                        with open(f"{values_output['-OUTPUT_FILE-']}", 'w') as outfile:
                            outfile.write(out)
                    elif event_output in {sg.WIN_CLOSED, 'EXIT'}:
                        window_output_active = False
                        break
                window_output.close()
                del window_output

    window_input.close()
    del window_input


if __name__ == "__main__":
    main()

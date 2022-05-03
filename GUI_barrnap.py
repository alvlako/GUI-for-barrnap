import PySimpleGUI as sg

sg.theme('Dark Blue 3')

SIZE = (15, 1)

layout = [
            [sg.Text('Welcome to barrnap')],
            [sg.Text('Input file path', size=SIZE), sg.InputText('file.fasta', key='-INPUT_FILE-'), sg.FileBrowse()],
            [sg.Text('Kingdom', size=SIZE), sg.InputText('bac', key='-KINGDOM-')],
            [sg.Text('Threads', size=SIZE), sg.InputText('1', key='-THREADS-')],
            [sg.Text('Lencutoff', size=SIZE), sg.InputText('0.8', key='-LENCUTOFF-')],
            [sg.Text('Reject', size=SIZE), sg.InputText('0.25', key='-REJECT-')],
            [sg.Text('Evalue', size=SIZE), sg.InputText('1e-06', key='-EVALUE-')],
            [sg.Text('Typed command:', size=SIZE), sg.InputText(key='-OUTPUT-')],
            [sg.Submit(), sg.Cancel()]
            ]

window = sg.Window('GUI barrnap application', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Submit':
        input_file = f"{values['-INPUT_FILE-']}"
        kingdom = f"--kingdom {values['-KINGDOM-']}"
        threads = f"--threads {values['-THREADS-']}"
        lencutoff = f"--lencutoff {values['-LENCUTOFF-']}"
        reject = f"--reject {values['-REJECT-']}"
        evalue = f"--evalue {values['-EVALUE-']}"
        command = f"barrnap {kingdom} {threads} {lencutoff} {reject} {evalue} {input_file}"
        window['-OUTPUT-'].update(command)

window.close()

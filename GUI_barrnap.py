import subprocess
import os.path
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import time


FONT_STYLE = 'Arial 20'
FONT_STYLE_HEADER = 'Arial 25 bold'



def install(package):
    subprocess.call(['pip', 'install', package])
    print('Required packages are installed')


def add_option(option, default=None, size=(30, 1)):
    # FONT_STYLE = 'Arial 20'
    return [sg.Text(option, size=size, font=FONT_STYLE), sg.InputText(default, key=f'-{option.upper()}-',
                                                                      font=FONT_STYLE)]


def add_file(text, file_path=None, key=None, size=(30, 1)):
    # FONT_STYLE = 'Arial 20'
    return [sg.Text(text, size=size, font=FONT_STYLE), sg.InputText(file_path, key=key, font=FONT_STYLE),
                                                       sg.FileBrowse()]


def make_command_for_barrnap(values_input, options_dic):
    command = ['barrnap', values_input['-INPUT_FILE-']]
    for option in options_dic:
        command.append(f"--{option.lower()}")
        command.append(f"{values_input[f'-{option.upper()}-']}")
        command.extend(['--outseq', values_input['-OUTPUT_FASTA_FILE-']])
    arg_list = command
    command = ' '.join(command)
    return command, arg_list


def run_barrnap(arg_list):
    start_time = time.time()
    stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    output_gff = stream.stdout.read()
    # we need err because it had barrnap log
    out, err = stream.communicate()
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_formatted = str(timedelta(seconds=elapsed_time))
    logger.info(f"{err}")
    logger.info(f"Elapsed time (h:mm:ss): {elapsed_time_formatted}")
    logger.info("Work finished")
    return output_gff


def show_help_page():
    help_message = '''
    BAsic Rapid Ribosomal RNA Predictor

    Barrnap predicts the location of ribosomal RNA genes in genomes.
    It supports bacteria (5S,23S,16S), archaea (5S,5.8S,23S,16S), metazoan mitochondria (12S,16S)
    and eukaryotes (5S,5.8S,28S,18S).
    It takes FASTA DNA sequence as input, and write GFF3 as output.
    It uses the new nhmmer tool that comes with HMMER 3.1 for HMM searching in RNA:DNA style.
    Multithreading is supported and one can expect roughly linear speed-ups with more CPUs.

    Search
    --kingdom is the database to use: Bacteria:bac, Archaea:arc, Eukaryota:euk, Metazoan Mitochondria:mito
    --threads is how many CPUs to assign to nhmmer search
    --evalue is the cut-off for nhmmer reporting, before further scrutiny
    --lencutoff is the proportion of the full length that qualifies as partial match
    --reject will not include hits below this proportion of the expected length

    If you use Barrnap in your work, please cite:

    Seemann T
    barrnap 0.9 : rapid ribosomal RNA prediction
    https://github.com/tseemann/barrnap

    Graphical user interface (GUI) for Barrnap was created as Bioinformatics Institute student project
    https://github.com/alvlako/GUI-for-barrnap

    Thank you and wellcome to Barrnap GUI!
    '''
    return help_message


def make_input_window():
    # FONT_STYLE = 'Arial 20'
    # FONT_STYLE_HEADER = 'Arial 25 bold'

    options_dic = {'Kingdom': 'bac', 'Threads': '1', 'Lencutoff': '0.8', 'Reject': '0.25', 'Evalue': '1e-06'}

    layout_input = [[sg.Text('Welcome to barrnap!', font=FONT_STYLE_HEADER)],
                    add_file('Input file path', 'sequence.fasta', '-INPUT_FILE-'),
                    add_file('Output FASTA file path', 'rRNA.fasta', '-OUTPUT_FASTA_FILE-')]
    layout_input.extend([add_option(*option) for option in options_dic.items()])
    layout_input.extend([[sg.Text('Typed command', size=(30, 1), font=FONT_STYLE), sg.InputText(key='-OUTPUT-',
                                                                                                font=FONT_STYLE)],
                         [sg.Submit(), sg.Cancel(),
                          sg.Button('HELP', button_color=(sg.YELLOWS[0], sg.BLUES[0]))]])

    window_input = sg.Window('GUI barrnap application', layout_input, finalize=True)
    window_output_active = False

    while True:
        event_input, values_input = window_input.read(timeout=100)
        if event_input in {sg.WIN_CLOSED, 'Cancel'}:
            break

        if event_input == 'HELP':
            make_help_window()

        if not window_output_active and event_input == 'Submit':
            if not os.path.exists(values_input['-INPUT_FILE-']):
                window_input['-INPUT_FILE-'].update("This file does not exist!")
            else:
                window_output_active = True
                command, arg_list = make_command_for_barrnap(values_input, options_dic)
                window_input['-OUTPUT-'].update(command)

                working_directory = os.getcwd()
                logger.info(f"Working directory: {working_directory}")
                logger.info(f"Input file that will be used: {values_input['-INPUT_FILE-']}")
                logger.info(f"Barrnap was called with the following arguments:\n {command}")

                output_gff = run_barrnap(arg_list)

                help = show_help_page()
                logger.info(help.split('If you use Barrnap in your work, please cite:')[1])

                make_output_window(logger, output_gff)

    window_input.close()
    del window_input


def make_help_window():
    # FONT_STYLE = 'Arial 20'
    # FONT_STYLE_HEADER = 'Arial 25 bold'
    help_page = show_help_page()
    layout_help = [[(sg.Text('Barrnap help page', size=[40, 1], font=FONT_STYLE_HEADER))],
                   [sg.Multiline(help_page, size=(80, 20), font=FONT_STYLE)],
                   [sg.Text('Output file path', size=(20, 1), font=FONT_STYLE),
                    sg.InputText('barrnap_help.txt', key='-HELP_PAGE-', font=FONT_STYLE), sg.FileBrowse(),
                    sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                    sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window_help = sg.Window('GUI barrnap application help page', layout_help, default_element_size=(30, 2))

    while True:
        event_help, values_help = window_help.read()
        if event_help == 'SAVE':
            with open(f"{values_help['-HELP_PAGE-']}", 'w') as help_file:
                help_file.write(help_page)
        elif event_help in {sg.WIN_CLOSED, 'EXIT'}:
            break
    window_help.close()
    del window_help


def make_output_window(log_file, output_gff):
    # FONT_STYLE = 'Arial 20'
    # FONT_STYLE_HEADER = 'Arial 25 bold'
    log_file_name = log_file._core.handlers[1]._sink._file.name
    with open(log_file_name) as output_log_file:
        output_log = output_log_file.read()
        layout_output = [[(sg.Text('Barrnap output', size=[40, 1], font=FONT_STYLE_HEADER))],
                         [sg.Multiline(output_log, size=(80, 20), font=FONT_STYLE)],
                         [sg.Text('Output GFF file', size=(20, 1), font=FONT_STYLE),
                          sg.InputText('result.gff', key='-OUTPUT_GFF_FILE-', font=FONT_STYLE), sg.FileBrowse(),
                          sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                          sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

        window_output = sg.Window('GUI barrnap application results', layout_output,
                                  default_element_size=(30, 2))

        while True:
            event_output, values_output = window_output.read()
            if event_output == 'SAVE':
                with open(f"{values_output['-OUTPUT_GFF_FILE-']}", 'w') as outfile:
                    outfile.write(output_gff)
            elif event_output in {sg.WIN_CLOSED, 'EXIT'}:
                break
        window_output.close()
        del window_output


def main():
    sg.theme('Dark Blue 3')

    now = datetime.now()
    barrnap_logs_dir_name = f"./barrnap_logs/{now.strftime('%Y-%m-%d')}/"
    Path(barrnap_logs_dir_name).mkdir(parents=True, exist_ok=True)
    logger.add(barrnap_logs_dir_name + "barrnap_log_file_{time:YYYY-MM-DD_HH-mm-ss}.log", format="{time:YYYY-MM-DD at HH:mm:ss} |"
                                                                             " {level} | {message}")
    logger.info("All the packages are installed")

    try:
        barrnap_app = subprocess.Popen(['barrnap', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       encoding='utf-8')
    except FileNotFoundError:
        # subprocess.call(['yes','|','conda', 'install', '-c', 'bioconda', '-c', 'conda-forge', 'phispy'])
        ps = subprocess.Popen('yes', stdout=subprocess.PIPE)
        output = subprocess.check_output(('conda', 'install', '-c', 'bioconda', '-c', 'conda-forge', 'barrnap'),
                                         stdin=ps.stdout)
        ps.wait()

    logger.info("Barrnap is checked")

    make_input_window()

    logger.info("Application has completed its work. Have a nice day!")


if __name__ == "__main__":
    try:
        import PySimpleGUI as sg
    except ImportError:
        install('pysimplegui')
    finally:
        import PySimpleGUI as sg

    try:
        from loguru import logger
    except ModuleNotFoundError:
        subprocess.call(['pip3', 'install', 'loguru'])
    finally:
        from loguru import logger

    main()

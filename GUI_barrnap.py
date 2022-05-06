import subprocess
import os.path
import time

ROW_SIZE = (60, 1)


def install(package):
    subprocess.call(['pip', 'install', package])
    print('Required packages are installed')


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

logger.add("file_barrnap_{time}.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
logger.info("All the packages are installed")

try:
    barrnap_app = subprocess.Popen(['barrnap', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
except FileNotFoundError:
    # subprocess.call(['yes','|','conda', 'install', '-c', 'bioconda', '-c', 'conda-forge', 'phispy'])
    ps = subprocess.Popen(('yes'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('conda', 'install', '-c', 'bioconda', '-c', 'conda-forge', 'barrnap'),
                                     stdin=ps.stdout)
    ps.wait()

logger.info("Barrnap is checked")


def add_option(option, default=None, size=ROW_SIZE):
    return [sg.Text(option, size=size), sg.InputText(default, key=f'-{option.upper()}-')]


def add_file(text, file_path=None, key=None, size=ROW_SIZE):
    return [sg.Text(text, size=size), sg.InputText(file_path, key=key), sg.FileBrowse()]


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

    Thank you and wellcome to Barrnap GUI!.
    '''
    return help_message


def main():
    sg.theme('Dark Blue 3')

    options_dic = {'Kingdom': 'bac', 'Threads': '1', 'Lencutoff': '0.8', 'Reject': '0.25', 'Evalue': '1e-06'}

    layout_input = [[sg.Text('Welcome to barrnap', font='Courier 400 italic bold underline overstrike')],
                    add_file('Input file path', 'sequence.fasta', '-INPUT_FILE-'),
                    add_file('Output FASTA file path', 'rRNA.fasta', '-OUTPUT_FASTA_FILE-')]
    layout_input.extend([add_option(*option) for option in options_dic.items()])
    layout_input.extend([[sg.Text('Typed command', size=ROW_SIZE), sg.InputText(key='-OUTPUT-')],
                         [sg.Submit(), sg.Cancel(),
                          sg.Button('HELP', button_color=(sg.YELLOWS[0], sg.BLUES[0]))]])

    window_input = sg.Window('GUI barrnap application', layout_input, finalize=True)
    window_output_active = False
    window_help_active = False

    while True:
        event_input, values_input = window_input.read(timeout=100)
        if event_input in {sg.WIN_CLOSED, 'Cancel'}:
            break

        if not window_help_active and event_input == 'HELP':
            window_help_active = True
            help_page = show_help_page()
            # print(help_page)
            layout_help = [[(sg.Text('Barrnap help page', size=[40, 1]))],
                           [sg.Multiline(help_page, size=(80, 20))],
                           [sg.Text('Output file path', size=(20, 1)),
                            sg.InputText('barrnap_help.txt', key='-HELP_PAGE-'), sg.FileBrowse(),
                            sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                            sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

            window_help = sg.Window('GUI barrnap application help page', layout_help, default_element_size=(30, 2))

            while window_help_active:
                event_help, values_help = window_help.read()
                if event_help == 'SAVE':
                    with open(f"{values_help['-HELP_PAGE-']}", 'w') as help_file:
                        help_file.write(help_page)
                elif event_help in {sg.WIN_CLOSED, 'EXIT'}:
                    window_help_active = False
                    break
            window_help.close()
            del window_help

        if not window_output_active and event_input == 'Submit':
            if not os.path.exists(values_input['-INPUT_FILE-']):
                text = "This file does not exist!"
                window_input['-INPUT_FILE-'].update(text)
            else:
                window_output_active = True
                command = ['barrnap']
                command.append(values_input['-INPUT_FILE-'])
                for option in options_dic:
                    command.append(f"--{option.lower()}")
                    command.append(f"{values_input[f'-{option.upper()}-']}")
                    command.extend(['--outseq', values_input['-OUTPUT_FASTA_FILE-']])
                arg_list = command
                command = ' '.join(command)

                window_input['-OUTPUT-'].update(command)

                logger.info(f"Input file that will be used: {values_input['-INPUT_FILE-']}")
                logger.info(f"Barrnap was called with the following arguments:\n {command}")

                start_time = time.time()
                stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, encoding='utf-8')
                output_gff = stream.stdout.read()
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info("Elapsed time: %s seconds" % elapsed_time)

                with open(values_input['-OUTPUT_FASTA_FILE-']) as output_fasta_file:
                    output_fasta = output_fasta_file.read()
                    layout_output = [[(sg.Text('Barrnap output', size=[40, 1]))],
                                     [sg.Multiline(output_fasta, size=(80, 20))],
                                     [sg.Text('Output file path', size=(20, 1)),
                                      sg.InputText('result.gff', key='-OUTPUT_GFF_FILE-'), sg.FileBrowse(),
                                      sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                                      sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

                    window_output = sg.Window('GUI barrnap application results', layout_output,
                                              default_element_size=(30, 2))

                    while window_output_active:
                        event_output, values_output = window_output.read()
                        if event_output == 'SAVE':
                            with open(f"{values_output['-OUTPUT_GFF_FILE-']}", 'w') as outfile:
                                outfile.write(output_gff)
                        elif event_output in {sg.WIN_CLOSED, 'EXIT'}:
                            window_output_active = False
                            break
                    window_output.close()
                    del window_output

    logger.info("Work finished")
    help = show_help_page()
    logger.info(help.split('If you use Barrnap in your work, please cite:')[1])
    window_input.close()
    del window_input


if __name__ == "__main__":
    main()

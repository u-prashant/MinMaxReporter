import sys
from tkinter import *
from tkinter import filedialog, ttk

from manager import Manager


class Constants:
    NO_FILES_SELECTED = 'No Files Selected'
    NO_DIR_SELECTED = 'No Directory Selected'


class GUI:
    APP_NAME = 'MinMax Reporter'
    DEFAULT_DIR = '/'

    def __init__(self, config):
        self.config = config
        self.launch()

    def launch(self):
        window = self.set_window()
        soh = ComponentGUI(window, self.config.source_dir, 'SOH Files')
        oit = ComponentGUI(window, self.config.source_dir, 'OIT Files')
        consumption = ComponentGUI(window, self.config.source_dir, 'Consumption Files')
        last_min_max = ComponentGUI(window, self.config.target_dir, 'Last Min Max File')
        target = TargetGUI(window, self.config.target_dir)
        generate = GenerateReportGUI(window, oit, soh, consumption, last_min_max, target, self.config)
        exit_btn = ExitGUI(window)

        soh.label_static.grid(column=1, row=1, padx=15, pady=13, sticky='W')
        soh.button_browse.grid(column=4, row=1, padx=15, pady=13, sticky='EW')
        soh.label_dynamic.grid(column=1, row=2, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=3, columnspan=4, sticky='ew')

        oit.label_static.grid(column=1, row=4, padx=15, pady=13, sticky='W')
        oit.button_browse.grid(column=4, row=4, padx=15, pady=13, sticky='EW')
        oit.label_dynamic.grid(column=1, row=5, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=6, columnspan=4, sticky='ew')

        consumption.label_static.grid(column=1, row=7, padx=15, pady=13, sticky='W')
        consumption.button_browse.grid(column=4, row=7, padx=15, pady=13, sticky='EW')
        consumption.label_dynamic.grid(column=1, row=8, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=9, columnspan=4, sticky='ew')

        last_min_max.label_static.grid(column=1, row=10, padx=15, pady=13, sticky='W')
        last_min_max.button_browse.grid(column=4, row=10, padx=15, pady=13, sticky='EW')
        last_min_max.label_dynamic.grid(column=1, row=11, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=12, columnspan=4, sticky='ew')

        target.label_static.grid(column=1, row=13, padx=15, pady=13, sticky='W')
        target.button_browse.grid(column=4, row=13, padx=15, pady=13, sticky='EW')
        target.label_dynamic.grid(column=1, row=14, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=15, columnspan=4, sticky='ew')

        generate.button.grid(column=2, row=16, columnspan=2, padx=15, pady=13, sticky='EW')
        exit_btn.button.grid(column=2, row=17, columnspan=2, padx=15, pady=13, sticky='EW')

        window.mainloop()

    @staticmethod
    def set_window():
        window = Tk()
        window.title(GUI.APP_NAME)
        window.config(background='azure3')
        return window


class TargetGUI:
    def __init__(self, window, destination_dir):
        self.window = window
        self.destination_dir = destination_dir
        self.label_static = self.get_label_static()
        self.label_dynamic = self.get_label_dynamic()
        self.button_browse = self.get_button_browse()

    def get_label_static(self):
        text = 'Target Directory'
        return Label(self.window, text=text, width=30, pady=7, bg='azure3')

    def get_label_dynamic(self):
        text = Constants.NO_DIR_SELECTED
        if self.destination_dir != '/':
            text = self.destination_dir
        return Label(self.window, text=text, width=70, height=4, fg='blue')

    def get_button_browse(self):
        return Button(self.window, text='Browse', width=20, command=self.browse_folder, bg='azure4', fg='white')

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.destination_dir, title='Select the target folder')
        if folder == '':
            folder = Constants.NO_DIR_SELECTED
        self.label_dynamic.configure(text=folder)


class ComponentGUI:
    def __init__(self, window, initial_dir, text):
        self.initial_dir = initial_dir
        self.text = text
        self.window = window
        self.label_static = self.get_label_static()
        self.label_dynamic = self.get_label_dynamic()
        self.button_browse = self.get_button_browse()

    def get_label_static(self):
        text = '{} Files Source Location'.format(self.text)
        return Label(self.window, text=text, width=30, pady=5, bg='azure3')

    def get_label_dynamic(self):
        return Label(self.window, text=Constants.NO_FILES_SELECTED, width=70, height=2, fg='blue')

    def get_button_browse(self):
        return Button(self.window, text='Browse', width=20, command=self.browse_files, bg='azure4', fg='white')

    def browse_files(self):
        file_types = [('Excel files', '.xlsx .xls .csv'), ('all files', '.*')]
        title = 'Select {} files'.format(self.text)
        files = filedialog.askopenfilenames(initialdir=self.initial_dir, title=title, filetypes=file_types)

        text = '\n'.join(list(files))
        if text == "":
            text = Constants.NO_FILES_SELECTED
        self.label_dynamic.configure(text=text)


class GenerateReportGUI:
    def __init__(self, window, oit_ui, soh_ui, consumption_ui, prev_minmax_ui, target_ui, config):
        self.config = config
        self.window = window
        self.oit_ui = oit_ui
        self.soh_ui = soh_ui
        self.consumption_ui = consumption_ui
        self.prev_minmax_ui = prev_minmax_ui
        self.target_ui = target_ui
        self.button = self.get_button()

    def get_button(self):
        return Button(self.window, text='Generate Report', bg='gray25', fg='white', width=30,
                      command=self.generate_report)

    def generate_report(self):
        oit_files = self.oit_ui.label_dynamic.cget('text')
        soh_files = self.soh_ui.label_dynamic.cget('text')
        consumption_files = self.consumption_ui.label_dynamic.cget('text')
        prev_min_max_files = self.prev_minmax_ui.label_dynamic.cget('text')
        target_dir = self.target_ui.label_dynamic.cget('text')
        self.config.set_source_dir(oit_files)
        self.config.set_target_dir(target_dir)
        self.config.write()

        oit_files_path = oit_files.split('\n')
        soh_files_path = soh_files.split('\n')
        consumption_files_path = consumption_files.split('\n')
        prev_min_max_file_path = prev_min_max_files.split('\n')[0]

        manager = Manager(consumption_files_path, soh_files_path, oit_files_path, prev_min_max_file_path, target_dir)
        manager.manage()


class ExitGUI:
    def __init__(self, window):
        self.window = window
        self.button = self.get_button()

    def get_button(self):
        return Button(self.window, text='EXIT', width=30, command=sys.exit)

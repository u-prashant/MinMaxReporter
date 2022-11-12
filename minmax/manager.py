import timeit

from constants import SkipRows
from reportwriter import ReportWriter
from minmaxreporter import MinMaxReporter
from preprocessors import SOHPreprocessor, ConsumptionPreprocessor, OITPreprocessor, MinMaxPreprocessor
from readers import Reader, ConfigurationReader, MinMaxReader


def print_df(df, title):
    print('-' * 30 + title + '-' * 30)
    print(df.columns)
    print(df.shape)
    print(df.head(10))
    print('-' * 100)


class Manager:

    def __init__(self, consumption_files, soh_files, oit_files, previous_min_max_file, output_dir):
        self.consumption_files = consumption_files
        self.soh_files = soh_files
        self.oit_files = oit_files
        self.previous_min_max_file = previous_min_max_file
        self.output_dir = output_dir

        print(self.consumption_files)
        print(self.soh_files)
        print(self.oit_files)
        print(self.previous_min_max_file)

    def manage(self):
        start = timeit.default_timer()

        # Read configuration file
        product_list_df, coefficient_df = ConfigurationReader.read()
        print_df(product_list_df, 'Product List DF')
        print_df(coefficient_df, 'Coefficient DF')

        # Reading input files
        soh_df = Reader.read_excel_files(self.soh_files, SkipRows.SOH_FILE)
        consumption_df = Reader.read_excel_files(self.consumption_files, SkipRows.CONSUMPTION_FILE)
        oit_df = Reader.read_excel_files(self.oit_files, SkipRows.OIT_FILE)
        prev_min_max_df = MinMaxReader.read(self.previous_min_max_file, SkipRows.MIN_MAX_FILE)

        # Preprocessing
        soh_df = SOHPreprocessor(product_list_df).preprocess(soh_df)
        print_df(soh_df, 'SOH DF')
        consumption_df = ConsumptionPreprocessor(product_list_df).preprocess(consumption_df)
        print_df(consumption_df, 'CONSUMPTION DF')
        oit_df = OITPreprocessor(product_list_df).preprocess(oit_df)
        print_df(oit_df, 'OIT DF')
        prev_min_max_df, current_date, last_12_months_date = MinMaxPreprocessor().preprocess(prev_min_max_df)
        print_df(prev_min_max_df, 'Prev MinMax Report')

        # Generate Report
        reporter = MinMaxReporter(product_list_df, soh_df, consumption_df, oit_df, prev_min_max_df, current_date)
        df = reporter.generate_report()
        print_df(df, 'Report')

        # Report Writer
        report_writer = ReportWriter(self.output_dir, coefficient_df)
        report_writer.compute_report(df, last_12_months_date, current_date)

        stop = timeit.default_timer()
        print('Time: ', stop - start)


if __name__ == '__main__':
    consumption_raw_files = [r'data/sample/consumption.xlsx']
    soh_raw_files = [r'data/sample/soh.xlsx']
    oit_raw_files = [r'data/sample/oit.xlsx']
    previous_min_max_ip_file = r'data/sample/prev_min_max_file.xlsx'
    output_dir = r'data/'
    Manager(consumption_raw_files, soh_raw_files, oit_raw_files, previous_min_max_ip_file, output_dir).manage()

import pandas as pd

from constants import Columns


class Reader:
    @staticmethod
    def convert_column_names_to_small(df):
        df.columns = df.columns.str.lower()
        return df

    @staticmethod
    def read_csv(file):
        return Reader.convert_column_names_to_small(pd.read_csv(file))

    @staticmethod
    def read_excel(file, header):
        df = pd.read_excel(file, header=header)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return Reader.convert_column_names_to_small(df)

    @staticmethod
    def read_excel_as_it_is(file, header):
        return pd.read_excel(file, header=header)

    @staticmethod
    def read_excel_sheet(file, sheet):
        return Reader.convert_column_names_to_small(pd.read_excel(file, sheet_name=sheet))

    @staticmethod
    def read_excel_files(raw_files, header):
        dfs = []
        for file in raw_files:
            print('Reading {} file...'.format(file))
            dfs.append(Reader.read_excel(file, header=header))
        return Reader.convert_column_names_to_small(pd.concat(dfs))


class ConfigurationReader:
    PRODUCT_LIST_SHEET = 'Product List'
    COEFFICIENT_SHEET = 'Coefficient'
    CONFIG_FILE_PATH = r'data/configuration_file.xlsx'

    @staticmethod
    def read():
        product_list_df = Reader.read_excel_sheet(ConfigurationReader.CONFIG_FILE_PATH,
                                                  ConfigurationReader.PRODUCT_LIST_SHEET)
        product_list_df = product_list_df.drop(columns=Columns.COLOR)

        coefficient_df = Reader.read_excel_sheet(ConfigurationReader.CONFIG_FILE_PATH,
                                                 ConfigurationReader.COEFFICIENT_SHEET)
        return product_list_df, coefficient_df


class MinMaxReader:
    @staticmethod
    def read(file, header):
        return Reader.read_excel_as_it_is(file, header)

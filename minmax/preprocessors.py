from constants import ProductListColumns, ConsumptionColumns, Columns, SOHColumns, OITColumns, MinMaxReportColumns
from datetime import datetime, timedelta


class Preprocessor:
    def __init__(self, name, product_list_df):
        self.name = name
        self.product_list_df = product_list_df

    @staticmethod
    def fill_na(df, columns_to_fill):
        default_columns = [Columns.COLOR, Columns.SIZE, Columns.CONFIGURATION]
        columns_to_fill.extend(default_columns)
        for column in columns_to_fill:
            df[column].fillna(0, inplace=True)
        return df

    def get_code_for_roq(self, df):
        df[ProductListColumns.ITEM_CODE] = df[Columns.ITEM_NUMBER]
        df = df.merge(self.product_list_df, on=ProductListColumns.ITEM_CODE, how='left')
        print('{} - found no ROQs for {} items'.format(self.name, df[Columns.CODE_FOR_ROQ].isnull().sum()))
        df = df[~df[Columns.CODE_FOR_ROQ].isnull()]
        return df

    def get_unique_code(self, df):
        df[Columns.UNIQUE_CODE] = df.apply(lambda x: self.__generate_unique_code(x), axis=1)
        return df

    @staticmethod
    def convert_int_quantity_to_positive(df, column_name):
        df[column_name] = df[column_name].astype(int)
        df[column_name] = df[column_name].abs()
        return df

    @staticmethod
    def filter_products_for_which_minmax_is_calculated(df):
        return df[df[ProductListColumns.CONSIDERED_IN_MINMAX] == 'Considered']

    @staticmethod
    def group_by(df, group_by_columns, columns_to_aggregate):
        df = df.groupby(group_by_columns)[columns_to_aggregate].sum().reset_index()
        return df

    @staticmethod
    def keep_only_required_columns(df, columns_to_keep):
        return df[columns_to_keep]

    def __generate_unique_code(self, row):
        roq = row[Columns.CODE_FOR_ROQ]
        color = row[Columns.COLOR]
        size = self.__convert_to_whole_number_if_not_decimal(row[Columns.SIZE])
        conf = self.__convert_to_whole_number_if_not_decimal(row[Columns.CONFIGURATION])
        return '{} BC{} ADD{} DIA{}'.format(roq, size, color, conf)

    @staticmethod
    def __convert_to_whole_number_if_not_decimal(value):
        try:
            value = float(value)
            if (value / int(value)) == 1:
                return int(value)
        except Exception:
            return value


class SOHPreprocessor(Preprocessor):
    def __init__(self, product_list_df):
        super().__init__('SOH Preprocessor', product_list_df)

    def preprocess(self, df):
        print('{} running ...'.format(self.name))
        df = self.fill_na(df, columns_to_fill=[SOHColumns.AVAILABLE_PHYSICAL])
        df = self.get_code_for_roq(df)
        df = self.get_unique_code(df)
        df = self.filter_products_for_which_minmax_is_calculated(df)
        df = self.group_by(df, group_by_columns=[Columns.UNIQUE_CODE], columns_to_aggregate=[SOHColumns.AVAILABLE_PHYSICAL])
        return df


class ConsumptionPreprocessor(Preprocessor):
    def __init__(self, product_list_df):
        super().__init__('Consumption Preprocessor', product_list_df)

    def preprocess(self, df):
        print('{} running ...'.format(self.name))
        df = self.__convert_column_names_to_generic_names(df)
        df = self.fill_na(df, columns_to_fill=[ConsumptionColumns.QUANTITY])
        df = self.convert_int_quantity_to_positive(df, ConsumptionColumns.QUANTITY)
        df = self.get_code_for_roq(df)
        df = self.get_unique_code(df)
        df = self.filter_products_for_which_minmax_is_calculated(df)
        df = self.group_by(df, group_by_columns=[Columns.UNIQUE_CODE], columns_to_aggregate=[ConsumptionColumns.QUANTITY])
        return df

    @staticmethod
    def __convert_column_names_to_generic_names(df):
        df[Columns.CONFIGURATION] = df[ConsumptionColumns.CONFIGURATION]
        df[Columns.SIZE] = df[ConsumptionColumns.SIZE]
        df[Columns.COLOR] = df[ConsumptionColumns.COLOR]
        df.drop([ConsumptionColumns.CONFIGURATION, ConsumptionColumns.SIZE, ConsumptionColumns.COLOR], axis=1, inplace=True)
        return df


class OITPreprocessor(Preprocessor):
    def __init__(self, product_list_df):
        super().__init__('OIT Preprocessor', product_list_df)

    def preprocess(self, df):
        print('{} running ...'.format(self.name))
        df = self.fill_na(df, columns_to_fill=[OITColumns.DELIVER_REMAINDER])
        df = self.get_code_for_roq(df)
        df = self.get_unique_code(df)
        df = self.filter_products_for_which_minmax_is_calculated(df)
        df = self.group_by(df, group_by_columns=[Columns.UNIQUE_CODE, OITColumns.MODE], columns_to_aggregate=[OITColumns.DELIVER_REMAINDER])
        df = self.__combine_different_modes_into_same_row(df)
        return df

    @staticmethod
    def __combine_different_modes_into_same_row(df):
        print(df[OITColumns.MODE].value_counts())
        sea_mode_df = df[df[OITColumns.MODE] == 'Sea']
        sea_mode_df[MinMaxReportColumns.OIT_1] = sea_mode_df[OITColumns.DELIVER_REMAINDER]
        sea_mode_df = sea_mode_df.drop([OITColumns.DELIVER_REMAINDER, OITColumns.MODE], axis=1)
        other_mode_df = df[df[OITColumns.MODE] != 'Sea']
        other_mode_df[MinMaxReportColumns.OIT_2] = other_mode_df[OITColumns.DELIVER_REMAINDER]
        other_mode_df = other_mode_df.drop([OITColumns.DELIVER_REMAINDER, OITColumns.MODE], axis=1)
        df = sea_mode_df.merge(other_mode_df, how='outer', on=Columns.UNIQUE_CODE)
        df[MinMaxReportColumns.OIT_1].fillna(0, inplace=True)
        df[MinMaxReportColumns.OIT_2].fillna(0, inplace=True)
        return df


class MinMaxPreprocessor:
    def __init__(self):
        self.name = 'Previous MinMax Preprocessor'

    def preprocess(self, df):
        df = df.dropna(how='all')
        last_12_months_consumption_columns = self.__get_last_12_month_columns(df)
        columns = [Columns.UNIQUE_CODE]
        columns.extend(last_12_months_consumption_columns)
        current_date = self.__compute_next_month_based_on_last_month(columns[-1])
        df = df[columns]
        df = self.__convert_datetime_columns_to_str_columns(df, last_12_months_consumption_columns)
        current_date = self.__convert_datetime_to_str(current_date)
        last_12_months_consumption_columns = [self.__convert_datetime_to_str(date) for date in last_12_months_consumption_columns]
        return df, current_date, last_12_months_consumption_columns

    @staticmethod
    def __get_last_12_month_columns(df):
        print(df.columns[7:19])
        return df.columns[7:19]

    @staticmethod
    def __compute_next_month_based_on_last_month(last_month):
        # move to first next month
        next_month = last_month.replace(day=28) + timedelta(days=4)
        # Now move to the second next month
        next_month = next_month.replace(day=28) + timedelta(days=4)
        # come back to the first next month's last day
        res = next_month - timedelta(days=next_month.day)
        print('Calculating min max report for date {}'.format(res.date()))
        return res.date()

    def __convert_datetime_columns_to_str_columns(self, df, columns):
        for column in columns:
            column_in_str = self.__convert_datetime_to_str(column)
            df[column_in_str] = df[column]
            df = df.drop(column, axis=1)
        return df

    @staticmethod
    def __convert_datetime_to_str(date):
        return datetime.strftime(date, '%b-%y')

import re

import numpy as np

from constants import Columns, ProductListColumns, SOHColumns, ConsumptionColumns, OITColumns, MinMaxReportColumns


class MinMaxReporter:
    def __init__(self, product_list_df, soh_df, consumption_df, oit_df, prev_minmax_df, current_date):
        self.product_list_df = product_list_df
        self.soh_df = soh_df
        self.consumption_df = consumption_df
        self.oit_df = oit_df
        self.prev_minmax_df = prev_minmax_df
        self.current_date = current_date
        self.regex_pattern = re.compile(r"(^.*?(?= BC)) BC(.*?(?= ADD)) ADD(.*?(?= DIA)) DIA(.*)")

    def generate_report(self):
        df = self.__combine_all_info_together()
        df = self.__fill_na(df)
        df = self.__drop_rows_with_null_unique_code(df)
        df = self.__get_item_properties_from_unique_code(df)
        df = self.__add_supplier(df)
        df = self.__add_lead_time(df)
        df = self.__add_minmax(df)
        df = self.__add_ramp_up(df)
        df = self.__add_min_qty(df)
        df = self.__add_max_month_min_time(df)
        df = self.__add_order_frequency(df)
        df = self.__add_moq_whs(df)
        df = self.__add_sku_price(df)
        df = self.__get_current_month_consumption(df)
        return df

    @staticmethod
    def __drop_rows_with_null_unique_code(df):
        return df.dropna(subset=[Columns.UNIQUE_CODE])

    def __combine_all_info_together(self):
        df = self.soh_df.merge(self.consumption_df, how='outer', on=Columns.UNIQUE_CODE)
        df = df.merge(self.oit_df, how='outer', on=Columns.UNIQUE_CODE)
        df = df.merge(self.prev_minmax_df, how='right', on=Columns.UNIQUE_CODE)
        return df

    @staticmethod
    def __fill_na(df):
        columns = [SOHColumns.AVAILABLE_PHYSICAL, ConsumptionColumns.QUANTITY, MinMaxReportColumns.OIT_1, MinMaxReportColumns.OIT_2]
        for column in columns:
            df[column].fillna(0, inplace=True)
        return df

    def __get_item_properties_from_unique_code(self, df):
        for index, row in df.iterrows():
            item, size, color, config = self.__extract_item_config_dia_color(row[Columns.UNIQUE_CODE])
            df.loc[index, Columns.ITEM_NUMBER] = item
            df.loc[index, Columns.SIZE] = size
            df.loc[index, Columns.COLOR] = color
            df.loc[index, Columns.CONFIGURATION] = config
        return df

    def __extract_item_config_dia_color(self, value):
        try:
            item, size, color, config = '', '', '', ''
            for match in self.regex_pattern.finditer(value):
                item = match.group(1).strip()
                size = match.group(2).strip()
                color = match.group(3).strip()
                config = match.group(4).strip()
                break
            return item, size, color, config
        except Exception as e:
            print("Invalid Unique Code: {}".format(value))
            raise e

    def __add_supplier(self, df):
        item_number_to_supplier_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, ProductListColumns.SUPPLIER)
        df[ProductListColumns.SUPPLIER] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_supplier_map.get(x, np.NAN)
        )
        return df

    def __add_lead_time(self, df):
        item_number_to_lead_time_whs_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE,
                                                           MinMaxReportColumns.LEAD_TIME_SUPP_WHS_IN_DAYS)
        item_number_to_lead_time_hub_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE,
                                                           MinMaxReportColumns.LEAD_TIME_FROM_HUB_BRANCH_DAYS)
        df[MinMaxReportColumns.LEAD_TIME_SUPP_WHS_IN_DAYS] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_lead_time_whs_map.get(x, 0)
        )
        df[MinMaxReportColumns.LEAD_TIME_FROM_HUB_BRANCH_DAYS] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_lead_time_hub_map.get(x, 0)
        )
        return df

    def __add_minmax(self, df):
        item_number_to_minmax_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, MinMaxReportColumns.MINMAX)
        df[MinMaxReportColumns.MINMAX] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_minmax_map.get(x, "NO")
        )
        return df

    def __add_ramp_up(self, df):
        item_number_to_ramp_up_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, MinMaxReportColumns.RAMP_UP)
        df[MinMaxReportColumns.RAMP_UP] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_ramp_up_map.get(x, '100%')
        )
        return df

    def __add_min_qty(self, df):
        item_number_to_min_qty_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE,
                                                     MinMaxReportColumns.MIN_QTY)
        df[MinMaxReportColumns.MIN_QTY] = df[Columns.ITEM_NUMBER].apply(
            lambda x: item_number_to_min_qty_map.get(x, 0)
        )
        return df

    def __add_max_month_min_time(self, df):
        product_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE,
                                      ProductListColumns.MAX_MONTH_MIN_TIME)
        df[ProductListColumns.MAX_MONTH_MIN_TIME] = df[Columns.ITEM_NUMBER].apply(lambda x: product_map.get(x, 0))
        return df

    def __add_order_frequency(self, df):
        product_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, MinMaxReportColumns.ORDER_FREQ)
        df[MinMaxReportColumns.ORDER_FREQ] = df[Columns.ITEM_NUMBER].apply(lambda x: product_map.get(x, 0))
        return df

    def __add_moq_whs(self, df):
        product_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, MinMaxReportColumns.MOQ_WHS)
        df[MinMaxReportColumns.MOQ_WHS] = df[Columns.ITEM_NUMBER].apply(lambda x: product_map.get(x, 1))
        return df

    def __add_sku_price(self, df):
        product_map = self.__form_map(self.product_list_df, ProductListColumns.ITEM_CODE, MinMaxReportColumns.SKU_PRICE)
        df[MinMaxReportColumns.SKU_PRICE] = df[Columns.ITEM_NUMBER].apply(lambda x: product_map.get(x, 100))
        return df

    @staticmethod
    def __form_map(df, key_column, value_column):
        return dict(zip(df[key_column], df[value_column]))

    def __get_current_month_consumption(self, df):
        df[self.current_date] = df[ConsumptionColumns.QUANTITY]
        df = df.drop(ConsumptionColumns.QUANTITY, axis=1)
        return df


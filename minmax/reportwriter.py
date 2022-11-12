import os
from datetime import datetime

import xlsxwriter

from constants import MinMaxReportColumns, Columns, ColumnNumber, SOHColumns, ProductListColumns, CoefficientColumns
from formula import Formula


class ReportWriter:
    def __init__(self, output_dir, coefficient_df):
        self.workbook = self.get_workbook(output_dir)
        self.minmax_sheet = self.get_minmax_worksheet(self.workbook)
        _ = self.get_coefficient_worksheet(self.workbook, coefficient_df)

    @staticmethod
    def get_output_file_path(output_dir):
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        return os.path.join(output_dir, 'minmax_report_{}.xlsx'.format(current_time))

    def get_workbook(self, output_dir):
        file = self.get_output_file_path(output_dir)
        return xlsxwriter.Workbook(file)

    @staticmethod
    def get_minmax_worksheet(workbook):
        return workbook.add_worksheet(name='MinMaxReport')

    @staticmethod
    def get_coefficient_worksheet(workbook, coefficient_df):
        worksheet = workbook.add_worksheet(name='Coefficient')
        # header
        worksheet.write(0, 0, CoefficientColumns.ALPHA)
        worksheet.write(0, 1, CoefficientColumns.COEFFICIENT)
        # data
        for row_idx, row in coefficient_df.iterrows():
            worksheet.write(row_idx+1, 0, row[CoefficientColumns.ALPHA])
            worksheet.write(row_idx+1, 1, row[CoefficientColumns.COEFFICIENT])
        return worksheet

    def compute_report(self, df, last_12_months_columns, current_date_column):
        self.write_minmax_header(last_12_months_columns, current_date_column)
        self.write_minmax_rows(df, last_12_months_columns, current_date_column)
        self.workbook.close()

    def write_minmax_header(self, last_12_months_date_columns, current_date_column):
        row, col = 0, 0
        self.minmax_sheet.write(row, col, MinMaxReportColumns.SUPPLIER)
        self.minmax_sheet.write(row, col+1, MinMaxReportColumns.UNIQUE_CODE)
        self.minmax_sheet.write(row, col+2, MinMaxReportColumns.ITEM_NUMBER)
        self.minmax_sheet.write(row, col+3, MinMaxReportColumns.CONFIGURATION)
        self.minmax_sheet.write(row, col+4, MinMaxReportColumns.SIZE)
        self.minmax_sheet.write(row, col+5, MinMaxReportColumns.ADD)

        col = ColumnNumber.DATE_COLUMN_STARTING
        for column in last_12_months_date_columns:
            self.minmax_sheet.write(row, col, column)
            col += 1
        self.minmax_sheet.write(row, col, current_date_column)

        col = ColumnNumber.TOTAL_COLUMN
        self.minmax_sheet.write(row, col, MinMaxReportColumns.TOTAL)
        self.minmax_sheet.write(row, col+1, MinMaxReportColumns.COUNT_MONTH)
        self.minmax_sheet.write(row, col+2, MinMaxReportColumns.AVG_CONSUMPTION)
        self.minmax_sheet.write(row, col+3, MinMaxReportColumns.ALLOCATED_STOCK)
        self.minmax_sheet.write(row, col+4, MinMaxReportColumns.STOCK_IN_HAND)
        self.minmax_sheet.write(row, col+5, MinMaxReportColumns.OIT_1)
        self.minmax_sheet.write(row, col+6, MinMaxReportColumns.OIT_2)
        self.minmax_sheet.write(row, col+7, MinMaxReportColumns.FUTURE_STOCK)
        self.minmax_sheet.write(row, col+8, MinMaxReportColumns.ORDER_1)
        self.minmax_sheet.write(row, col+9, MinMaxReportColumns.COVERAGE)
        self.minmax_sheet.write(row, col+10, MinMaxReportColumns.LEAD_TIME_SUPP_WHS_IN_DAYS)
        self.minmax_sheet.write(row, col+11, MinMaxReportColumns.LEAD_TIME_FROM_HUB_BRANCH_DAYS)
        self.minmax_sheet.write(row, col+12, MinMaxReportColumns.LEAD_TIME_SUPP_WHS_IN_MONTH)
        self.minmax_sheet.write(row, col+13, MinMaxReportColumns.MINMAX)
        self.minmax_sheet.write(row, col+14, MinMaxReportColumns.RAMP_UP)
        self.minmax_sheet.write(row, col+15, MinMaxReportColumns.MIN_QTY)
        self.minmax_sheet.write(row, col+16, MinMaxReportColumns.MAX_MONTH)
        self.minmax_sheet.write(row, col+17, MinMaxReportColumns.ORDER_FREQ)
        self.minmax_sheet.write(row, col+18, MinMaxReportColumns.MOQ_WHS)
        self.minmax_sheet.write(row, col+19, MinMaxReportColumns.AVG_MONTHLY_DEMAND)
        self.minmax_sheet.write(row, col+20, MinMaxReportColumns.CLASS)
        self.minmax_sheet.write(row, col+21, MinMaxReportColumns.DDL)
        self.minmax_sheet.write(row, col+22, MinMaxReportColumns.NEXT_SUPPLY_TIME_INVENTORY)
        self.minmax_sheet.write(row, col+23, MinMaxReportColumns.ALPHA)
        self.minmax_sheet.write(row, col+24, MinMaxReportColumns.COEFFICIENT_OF_SECURITY)
        self.minmax_sheet.write(row, col+25, MinMaxReportColumns.SS1)
        self.minmax_sheet.write(row, col+26, MinMaxReportColumns.SS2)
        self.minmax_sheet.write(row, col+27, MinMaxReportColumns.SS3)
        self.minmax_sheet.write(row, col+28, MinMaxReportColumns.SS_CONSTRAINT)
        self.minmax_sheet.write(row, col+29, MinMaxReportColumns.ROL)
        self.minmax_sheet.write(row, col+30, MinMaxReportColumns.LOT_SIZE)
        self.minmax_sheet.write(row, col+31, MinMaxReportColumns.MAX_LEVEL)
        self.minmax_sheet.write(row, col+32, MinMaxReportColumns.ROQ)
        self.minmax_sheet.write(row, col+33, MinMaxReportColumns.MONTH_COVERAGE_SS)
        self.minmax_sheet.write(row, col+34, MinMaxReportColumns.MONTH_COVERAGE_DDL)
        self.minmax_sheet.write(row, col+35, MinMaxReportColumns.MONTH_COVERAGE_DDL_SS)
        self.minmax_sheet.write(row, col+36, MinMaxReportColumns.MAX_MULTIPLIER_MONTH)
        self.minmax_sheet.write(row, col+37, MinMaxReportColumns.CRITICAL)
        self.minmax_sheet.write(row, col+38, MinMaxReportColumns.UNDER_SAFETY_STOCK)
        self.minmax_sheet.write(row, col+39, MinMaxReportColumns.OK)
        self.minmax_sheet.write(row, col+40, MinMaxReportColumns.EXCESS)
        self.minmax_sheet.write(row, col+41, MinMaxReportColumns.MISSING_QTY)
        self.minmax_sheet.write(row, col+42, MinMaxReportColumns.PROJECTED_EXCESS_QTY)
        self.minmax_sheet.write(row, col+43, MinMaxReportColumns.SKU_PRICE)
        self.minmax_sheet.write(row, col+44, MinMaxReportColumns.EXCESS_VALUE)

    def write_minmax_rows(self, df, last_12_months_date_columns, current_date_column):
        df.fillna(0, inplace=True)
        last_row = len(df.index) + 1

        for row_idx, row in df.iterrows():
            columns = []
            columns.append(row[MinMaxReportColumns.SUPPLIER])
            columns.append(row[MinMaxReportColumns.UNIQUE_CODE])
            columns.append(row[MinMaxReportColumns.ITEM_NUMBER])
            columns.append(row[MinMaxReportColumns.CONFIGURATION])
            columns.append(row[MinMaxReportColumns.SIZE])
            columns.append(row[Columns.COLOR])
            for column in last_12_months_date_columns:
                columns.append(row[column])
            columns.append(row[current_date_column])

            # write to worksheet
            row_idx += 1
            for col in range(len(columns)):
                self.minmax_sheet.write(row_idx, col, columns[col])

            col = ColumnNumber.TOTAL_COLUMN
            self.minmax_sheet.write(row_idx, col, Formula.total(row_idx+1))
            self.minmax_sheet.write(row_idx, col+1, Formula.count_month(row_idx+1))
            self.minmax_sheet.write(row_idx, col+2, Formula.avg_consumption(row_idx+1))
            self.minmax_sheet.write(row_idx, col+3, 0)
            self.minmax_sheet.write(row_idx, col+4, row[SOHColumns.AVAILABLE_PHYSICAL])
            self.minmax_sheet.write(row_idx, col+5, row[MinMaxReportColumns.OIT_1])
            self.minmax_sheet.write(row_idx, col+6, row[MinMaxReportColumns.OIT_2])
            self.minmax_sheet.write(row_idx, col+7, Formula.future_stock(row_idx+1))
            self.minmax_sheet.write(row_idx, col+8, Formula.order_1(row_idx+1))
            self.minmax_sheet.write(row_idx, col+9, Formula.coverage(row_idx+1))
            self.minmax_sheet.write(row_idx, col+10, row[MinMaxReportColumns.LEAD_TIME_SUPP_WHS_IN_DAYS])
            self.minmax_sheet.write(row_idx, col+11, row[MinMaxReportColumns.LEAD_TIME_FROM_HUB_BRANCH_DAYS])
            self.minmax_sheet.write(row_idx, col+12, Formula.lead_time(row_idx+1))
            self.minmax_sheet.write(row_idx, col+13, row[MinMaxReportColumns.MINMAX])
            self.minmax_sheet.write(row_idx, col+14, row[MinMaxReportColumns.RAMP_UP])
            self.minmax_sheet.write(row_idx, col+15, row[MinMaxReportColumns.MIN_QTY])
            self.minmax_sheet.write(row_idx, col+16, Formula.max_month(row_idx+1, row[ProductListColumns.MAX_MONTH_MIN_TIME]))
            self.minmax_sheet.write(row_idx, col+17, row[MinMaxReportColumns.ORDER_FREQ])
            self.minmax_sheet.write(row_idx, col+18, row[MinMaxReportColumns.MOQ_WHS])
            self.minmax_sheet.write(row_idx, col+19, Formula.avg_monthly_demand(row_idx+1))
            self.minmax_sheet.write(row_idx, col+20, Formula.class_(row_idx+1, last_row))
            self.minmax_sheet.write(row_idx, col+21, Formula.ddl(row_idx+1))
            self.minmax_sheet.write(row_idx, col+22, Formula.next_supply_time(row_idx+1))
            self.minmax_sheet.write(row_idx, col+23, Formula.alpha(row_idx+1))
            self.minmax_sheet.write(row_idx, col+24, Formula.coefficient_of_security(row_idx+1))
            self.minmax_sheet.write(row_idx, col+25, Formula.ss1(row_idx+1))
            self.minmax_sheet.write(row_idx, col+26, Formula.ss2(row_idx+1))
            self.minmax_sheet.write(row_idx, col+27, Formula.ss3(row_idx+1))
            self.minmax_sheet.write(row_idx, col+28, Formula.ss_constraint(row_idx+1))
            self.minmax_sheet.write(row_idx, col+29, Formula.rol(row_idx+1))
            self.minmax_sheet.write(row_idx, col+30, Formula.lot_size(row_idx+1))
            self.minmax_sheet.write(row_idx, col+31, Formula.max_level(row_idx+1))
            self.minmax_sheet.write(row_idx, col+32, Formula.roq(row_idx+1))
            self.minmax_sheet.write(row_idx, col+33, Formula.month_coverage_ss(row_idx+1))
            self.minmax_sheet.write(row_idx, col+34, Formula.month_coverage_ddl(row_idx+1))
            self.minmax_sheet.write(row_idx, col+35, Formula.month_coverage_ss_ddl(row_idx+1))
            self.minmax_sheet.write(row_idx, col+36, Formula.max_multiplier_month(row_idx+1))
            self.minmax_sheet.write(row_idx, col+37, Formula.critical(row_idx+1))
            self.minmax_sheet.write(row_idx, col+38, Formula.under_safety_stock(row_idx+1))
            self.minmax_sheet.write(row_idx, col+39, Formula.ok(row_idx+1))
            self.minmax_sheet.write(row_idx, col+40, Formula.excess(row_idx+1))
            self.minmax_sheet.write(row_idx, col+41, Formula.missing_quantity(row_idx+1))
            self.minmax_sheet.write(row_idx, col+42, Formula.projected_excess_quantity(row_idx+1))
            self.minmax_sheet.write(row_idx, col+43, row[MinMaxReportColumns.SKU_PRICE])
            self.minmax_sheet.write(row_idx, col+44, Formula.excess_value(row_idx+1))

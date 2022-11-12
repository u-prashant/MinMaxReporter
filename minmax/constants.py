class SkipRows:
    SOH_FILE = 5
    CONSUMPTION_FILE = 0
    OIT_FILE = 13
    MIN_MAX_FILE = 0


class ProductListColumns:
    ITEM_CODE = 'item code'
    SUPPLIER = 'supplier'
    CONSIDERED_IN_MINMAX = 'considered in min-max'
    MAX_MONTH_MIN_TIME = 'max. month (min. time)'


class CoefficientColumns:
    ALPHA = 'alpha'
    COEFFICIENT = 'coefficient of security'


class Columns:
    ITEM_NUMBER = 'item number'
    CONFIGURATION = 'configuration'
    SIZE = 'size'
    COLOR = 'color'
    CODE_FOR_ROQ = 'code for roq'
    UNIQUE_CODE = 'unique code'


class ConsumptionColumns:
    CONFIGURATION = 'dia'
    SIZE = 'sph/base'
    COLOR = 'cyl/add'
    QUANTITY = 'qty'


class SOHColumns:
    AVAILABLE_PHYSICAL = 'available physical'


class OITColumns:
    DELIVER_REMAINDER = 'deliver remainder'
    MODE = 'mode'


class MinMaxReportColumns:
    SUPPLIER = 'supplier'
    UNIQUE_CODE = 'unique code'
    ITEM_NUMBER = 'item number'
    CONFIGURATION = 'configuration'
    SIZE = 'size'
    ADD = 'add'
    TOTAL = 'total'
    COUNT_MONTH = 'Count Month'
    AVG_CONSUMPTION = 'Avg. Consumption'
    ALLOCATED_STOCK = 'Allocated Stock'
    STOCK_IN_HAND = 'Stock In Hand'
    OIT_1 = 'OIT-1 (Sea)'
    OIT_2 = 'OIT-2 (Surface/Air)'
    FUTURE_STOCK = 'Future Stock'
    ORDER_1 = 'Order-1'
    COVERAGE = 'Coverage'
    LEAD_TIME_SUPP_WHS_IN_DAYS = 'lead time supp-whs (in days)'
    LEAD_TIME_FROM_HUB_BRANCH_DAYS = 'lead time hub-brnanch (in days)'
    LEAD_TIME_SUPP_WHS_IN_MONTH = 'Lead Time Supp-WHS (In Months)'
    MINMAX = 'minmax (yes/no)'
    RAMP_UP = 'ramp up'
    MIN_QTY = 'min qty'
    MAX_MONTH = 'Max Month'
    ORDER_FREQ = 'order frequency (month)'
    MOQ_WHS = 'moq whs'
    AVG_MONTHLY_DEMAND = 'Avg. Monthly Demand'
    CLASS = 'Class'
    DDL = 'DDL'
    NEXT_SUPPLY_TIME_INVENTORY = 'Next Supply Time Inventory (Lead Time Days + 30 days inv)'
    ALPHA = 'Alpha'
    COEFFICIENT_OF_SECURITY = 'Coefficient of Security'
    SS1 = 'SS1'
    SS2 = 'SS2'
    SS3 = 'SS3 (SS1+SS2)'
    SS_CONSTRAINT = 'SS Constraint'
    ROL = 'ROL (SSC+DDL)'
    LOT_SIZE = 'Lot Size'
    MAX_LEVEL = 'Max Level (ROL+LOT)'
    ROQ = 'ROQ (Max level - STH - OIT'
    MONTH_COVERAGE_SS = 'Month Coverage-SS'
    MONTH_COVERAGE_DDL = 'Month Coverage-DDL'
    MONTH_COVERAGE_DDL_SS = 'Month Coverage (DDL+SS)'
    MAX_MULTIPLIER_MONTH = 'Max Multiplier Month'
    CRITICAL = 'Critical'
    UNDER_SAFETY_STOCK = 'Under Safety Stock'
    OK = 'OK'
    EXCESS = 'Excess'
    MISSING_QTY = 'Missing Qty'
    PROJECTED_EXCESS_QTY = 'Projected Excess Qty'
    SKU_PRICE = 'sku price'
    EXCESS_VALUE = 'Excess Value'
    OIT_VAL = 'OIT Val. (INR)'


class ColumnNumber:
    DATE_COLUMN_STARTING = 6
    TOTAL_COLUMN = 19

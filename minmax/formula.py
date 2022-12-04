class Formula:
    @staticmethod
    def total(row):
        return f'=SUM(H{row}:S{row})'

    @staticmethod
    def count_month(row):
        return f'=COUNTIF(H{row}:S{row}, ">0")'

    @staticmethod
    def avg_consumption(row):
        return f'=AVERAGE(S{row},(ROUND(AVERAGE(P{row}:S{row},(AVERAGE(G{row}:S{row}))),0)))'

    @staticmethod
    def future_stock(row):
        return f'=(X{row}-W{row})+Y{row}+Z{row}'

    @staticmethod
    def order_1(row):
        return f'=AA{row}-(V{row}*3)'

    @staticmethod
    def coverage(row):
        return f'=IF(V{row}=0,AA{row},AA{row}/V{row})'

    @staticmethod
    def lead_time(row):
        return f'=(AD{row}+AE{row})/30'

    @staticmethod
    def max_month(row, min_time):
        return f'={min_time}+AF{row}'

    @staticmethod
    def avg_monthly_demand(row):
        return f'=V{row}'

    @staticmethod
    def class_(row, last_row):
        return f'=IF(V{row}<1,"Low",IF(AND(U{row}>=9,V{row}>(SUMIF($C$2:$C${last_row},C{row},$V$2:$V${last_row})/COUNTIF($C$2:$C${last_row},C{row}))),"High","Medium"))'

    @staticmethod
    def ddl(row):
        return f'=IF(AG{row}="no",0,ROUNDUP(AF{row}*AM{row},0))'

    @staticmethod
    def next_supply_time(row):
        return f'=AO{row}+ROUND(AM{row}/2,0)'

    @staticmethod
    def alpha(row):
        return f'=IF(AM{row}=0,0,ROUND(STDEV(H{row}:S{row})/AM{row},1))'

    @staticmethod
    def coefficient_of_security(row):
        return f"=IF(AM{row}=0,0,IF(AQ{row}>3.7,2.4,IF(AQ{row}<0.1,1.5,VLOOKUP(AQ{row},'Coefficient'!$A$2:$B$38,2,0))))"

    @staticmethod
    def ss1(row):
        return f'=IF(AN{row}="Low",MIN(2*AM{row},IF(AG{row}="NO",0,STDEVA(H{row}:S{row})*AR{row}*SQRT(AF{row}+AK{row}))),IF(AN{row}="Medium",MIN(4*AM{row},IF(AG{row}="NO",0,STDEVA(H{row}:S{row})*AR{row}*SQRT(AF{row}+AK{row}))),MIN(6*AM{row},IF(AG{row}="NO",0,STDEVA(H{row}:S{row})*AR{row}*SQRT(AF{row}+AK{row})))))'

    @staticmethod
    def ss2(row):
        return f'=IF(AG{row}="NO",0,(AM{row}*0))'

    @staticmethod
    def ss3(row):
        return f'=AS{row}+AT{row}'

    @staticmethod
    def ss_constraint(row):
        return f'=IF(OR(AG{row}="no",AU{row}=0),0,IF(OR(AN{row}="low",AN{row}="medium"),(ROUND(MAX(AI{row},MIN(AU{row}*AH{row},AM{row}*BD{row})),0)),(ROUND(MAX(AI{row},MAX(AU{row}*AH{row},AM{row}*BD{row})),0))))'

    @staticmethod
    def rol(row):
        return f'=IF($AG{row}="no",0,IF($AN{row}="Low",MIN($AO{row}+AV{row},V{row}),SUM($AO{row},AV{row})))'

    @staticmethod
    def lot_size(row):
        return f'=IF(AG{row}="no",0,ROUNDUP(MAX(AL{row},(AM{row})*AK{row}),0))'

    @staticmethod
    def max_level(row):
        return f'=AW{row}+AX{row}'

    @staticmethod
    def roq(row):
        return f'=IF(OR($AG{row}="No",AND($AN{row}="Low",$AC{row}>2.5)),0,IF(OR($AA{row}<=$AW{row},$AP{row}-AA{row}>0),$AY{row}-$AA{row},0))'

    @staticmethod
    def month_coverage_ss(row):
        return f'=IF(AND(AU{row}=0,AM{row}=0),0,(AU{row}/AM{row}))'

    @staticmethod
    def month_coverage_ddl(row):
        return f'=IF(AND(AO{row}=0,AM{row}=0),0,IF(AND(AM{row}>0,AO{row}=0),0,(AO{row}/AM{row})))'

    @staticmethod
    def month_coverage_ss_ddl(row):
        return f'=BA{row}+BB{row}'

    @staticmethod
    def max_multiplier_month(row):
        return f'=AJ{row}-BC{row}'

    @staticmethod
    def critical(row):
        return f'=IF(AA{row}<0.5*AV{row},1,0)'

    @staticmethod
    def under_safety_stock(row):
        return f'=IF(AND(0.5*AV{row}<=AA{row},AA{row}<AV{row}),1,0)'

    @staticmethod
    def ok(row):
        return f'=IF(AND(AV{row}<=AA{row},AA{row}<=((1.5*AV{row})+AX{row})),1,0)'

    @staticmethod
    def excess(row):
        return f'=IF(AA{row}>((1.5*AV{row})+AX{row}),1,0)'

    @staticmethod
    def missing_quantity(row):
        return f'=IF(AA{row}<AV{row},AA{row}-AV{row},0)'

    @staticmethod
    def projected_excess_quantity(row):
        return f'=IF(BH{row}=1,ROUND(AA{row}-((1.5*AV{row})+AX{row}),0),0)'

    @staticmethod
    def excess_value(row):
        return f'=BK{row}*BJ{row}'

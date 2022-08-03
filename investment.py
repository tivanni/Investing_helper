from helpers import *
from settings import *


class Investment:

    FEE = FEE_INVESTMENT
    TAX = TAX_INVESTMENT
    CODE = "INVESTMENT"


    def __init__(self, starting_capital, starting_year, unit_value):
        self.starting_capital = starting_capital
        self.starting_year = starting_year
        self.current_year = starting_year
        self.current_capital = starting_capital
        self.tax_paid = 0
        self.id = f"{self.CODE}_{self.starting_year}"
        self.capital_gain_tax = 0
        self.exit_capital = 0
        self.exited = False
        self.unit_value = unit_value
        self.unit_starting_value = unit_value
        self.unit_numbers = starting_capital / unit_value


    def apply_interest(self):
        multiplier = 1 + INTEREST_RATE
        unit_value_new = self.unit_value * multiplier
        new_capital = unit_value_new * self.unit_numbers
        smart_print(f'INTEREST_APPLIED_EVENT: {self.id} unit-value pre-interest {round(self.unit_value,2)} becomes {round(unit_value_new,2)}.Capital {round(self.current_capital,2)} becomes {round(new_capital,2)}')
        self.current_capital = new_capital
        self.unit_value = unit_value_new


    def apply_fees(self):
        multiplier = 1 - self.FEE
        new_capital = self.current_capital * multiplier
        new_unit_numbers = new_capital / self.unit_value
        smart_print(f'FEE_APPLIED_EVENT: {self.id} unit-number pre-fee {round(self.unit_numbers,2)} becomes {round(new_unit_numbers,2)} capital pre-fee {round(self.current_capital,2)} becomes {round(new_capital,2)}')
        self.current_capital = new_capital
        self.unit_numbers = new_unit_numbers


    def get_capital_gain_per_unit(self):
        capital_gain_per_unit = self.unit_value - self.unit_starting_value
        return capital_gain_per_unit

    def get_capital_gain(self):
        capital_gain = self.get_capital_gain_per_unit() * self.unit_numbers
        smart_print(f'CAPITAL_GAIN_CALCULATED: {self.id} {capital_gain}')
        return capital_gain

    def exit_investment(self):
        self.exited = True
        self.capital_gain_tax = self.get_capital_gain() * self.TAX
        capital_after_taxes = self.current_capital - self.capital_gain_tax
        smart_print(f'CAPITAL_AFTER_TAXES: {self.id} {capital_after_taxes}')
        self.current_capital = capital_after_taxes
        self.exit_capital = capital_after_taxes
        self.tax_paid = self.capital_gain_tax


    def increase_current_year(self):
        self.current_year = self.current_year + 1

    def yearly_cycle(self):
        self.apply_fees()
        self.apply_interest()
        self.increase_current_year()
        smart_print(f"ETF REPORT. Name {self.id}, current capital {round(self.current_capital,3)}, unit value {round(self.unit_value,3)}, unit_numbers {round(self.unit_numbers,3)}, tax paid {round(self.tax_paid,3)}, percentage gain(bet) {round(self.get_gain_percentage(),3)}, absolute gain((bet) {round(self.get_gain_absolute(),3)}")

    def get_gain_percentage(self):
        capital = self.current_capital
        if self.exited:
            capital = self.exit_capital
        return int((capital/self.starting_capital)*100 - 100)

    def get_gain_absolute(self):
        capital = self.current_capital
        if self.exited:
            capital = self.exit_capital
        return int((capital - self.starting_capital))

    def __repr__(self):
        return f"ETF REPORT. Name {self.id}, starting capital {self.starting_capital}, current capital {int(self.current_capital)}, exit capital {int(self.exit_capital)}, tax paid {int(self.tax_paid)}, percentage gain {int(self.get_gain_percentage())}, absolute gain {int(self.get_gain_absolute())}"

class EtfItalia(Investment):
    TAX = TAX_ETF_ITALIA
    CODE = "ETF_ITALIA"


class EtfIrlanda(Investment):
    TAX = TAX_ETF_IRLANDA
    CODE = "ETF_IRLANDA"

    def __init__(self, starting_capital, starting_year, unit_value):
        self.tax_paid_per_unit = 0
        super().__init__(starting_capital,starting_year,unit_value)


    def pay_tax(self, tax_event_name, tax_name, deemed):
        tax_per_unit = self.get_capital_gain_per_unit() * self.TAX
        tax_per_unit_to_pay = tax_per_unit - self.tax_paid_per_unit
        tax_total_to_pay = tax_per_unit_to_pay * self.unit_numbers ###this seems to be wrong as unit number is lowered by fees
        new_capital = self.current_capital - tax_total_to_pay
        new_unit_numbers = new_capital / self.unit_value
        old_capital = self.current_capital
        old_unit_numbers = self.unit_numbers
        old_tax_paid_per_unit = self.tax_paid_per_unit
        self.tax_paid_per_unit += tax_per_unit_to_pay
        self.tax_paid += self.tax_paid_per_unit * self.unit_numbers
        self.current_capital = new_capital
        self.unit_numbers = new_unit_numbers
        if deemed:
            smart_print(f"{tax_event_name}: {self.id}. Unit value {round(self.unit_value,3)}, unit number see below,"
                        f" unit {tax_name} "
                        f"{round(tax_per_unit,3)}, unit_to_pay {tax_name} {round(tax_per_unit_to_pay,3)},"
                        f" all_units_to_pay"
                        f" {tax_name} {round(tax_total_to_pay,3)}\n "
                        f"capital pre {tax_name} {round(old_capital,3)}, capital post {tax_name} {round(self.current_capital,3)},\n"
                        f"unit numbers  pre {tax_name} {round(old_unit_numbers,3)}, unit numbers post {tax_name} {round(self.unit_numbers,3)}"
                        f"unit tax paid pre {tax_name} {round(old_tax_paid_per_unit,3)}, unit tax paid post {tax_name} "
                        f"{round(self.tax_paid_per_unit,3)}", False)
        else:
            smart_print(f"{tax_event_name}: {self.id}. Unit value {round(self.unit_value, 3)}, unit number see below,"
                        f"unit {tax_name} "
                        f"{round(tax_per_unit, 3)}, unit_to_pay {tax_name} {round(tax_per_unit_to_pay, 3)} ,"
                        f" all_units_to_pay"
                        f" {tax_name} {round(tax_total_to_pay, 3)}\n "
                        f"capital pre {tax_name} {round(old_capital, 3)}, capital post {tax_name} {round(self.current_capital, 3)},\n"
                        f"unit numbers  pre {tax_name} {round(old_unit_numbers,3)},"
                        f"unit tax paid pre {tax_name} {round(old_tax_paid_per_unit, 3)}, unit tax paid post {tax_name} "
                        f"{round(self.tax_paid_per_unit, 3)}", False)
            self.exit_capital = self.current_capital


    def deemed_disposal(self):
        if self.current_year - self.starting_year > 0:
            if ((self.current_year - self.starting_year) % 8) == 0:
                self.pay_tax("DEEMED_DISPOSAL_EVENT",'dd_tax', True)


    def yearly_cycle(self):
        self.deemed_disposal() #consertative, as first thing
        super().yearly_cycle()

    def exit_investment(self):
        self.pay_tax("EXIT_INVESTMENT_EVENT","ei_tax", False)
        smart_print(f"EXIT_REPORT. Name {self.id}, starting capital {round(self.starting_capital,3)}, current capital {round(self.current_capital,3)}, exit capital {round(self.exit_capital,3)}, unit value {round(self.unit_value,3)}, unit numbers {round(self.unit_numbers,3)}, tax paid {round(self.tax_paid,3)}, percentage gain(aet) {round(self.get_gain_percentage(),3)}, absolute gain((aet) {round(self.get_gain_absolute(),3)}")

class PensionInvestment(Investment):
    FEE = FEE_PENSION

    def exit_investment(self):
        #no capital gain taxes
        self.exit_capital = self.current_capital
        smart_print(f"PENSION_EXIT_INVESTMENT: {self.current_capital}")

class Portfolio():

    def __init__(self, name):
        self.etfs = []
        self.invested_capital = 0
        self.exit_capital = 0
        self.name = name

    def perform_pac(self, investment):
        if isinstance(investment, PensionInvestment):
            raise ValueError("PensionPortfolio: can't perform PAC as Investment is of wrong type")
        self.etfs.append(investment)

    def yearly_cycle(self):
        for etf in self.etfs:
            etf.yearly_cycle()

    def exit_investment(self):
        self.get_invested_capital()
        for etf in self.etfs:
            etf.exit_investment()
            self.exit_capital += int(etf.exit_capital)

    def get_invested_capital(self):
        for etf in self.etfs:
            self.invested_capital += etf.starting_capital

    def get_gain_percentage(self):
        return int((self.exit_capital / self.invested_capital) * 100 - 100)

    def get_gain_absolute(self):
        return int((self.exit_capital - self.invested_capital))

    def print_etfs(self):
        for etf in self.etfs:
            print(etf)

    def __repr__(self):
        return f"PORTFOLIO REPORT. Name {self.name}, invested capital {self.invested_capital}, exit capital {self.exit_capital}, percentage gain {self.get_gain_percentage()}, absolute gain {self.get_gain_absolute()},eft# {len(self.etfs)}"


class PensionPortfolio(Portfolio):

    def __init__(self, name):
        self.etfs = []
        self.invested_capital = 0
        self.exit_capital = 0
        self.name = name
        self.tax_paid = 0
        self.actual_invested_capital = 0 # when putting money into pension, no tax are applied. this represents money
                                         # was received in payroll instead of investing it

    def perform_pac(self, investment):
        if not isinstance(investment, PensionInvestment):
            raise ValueError("PensionPortfolio: can't perform PAC as Investment is of wrong type")
        self.etfs.append(investment)

    def get_invested_capital(self):
        for etf in self.etfs:
            self.invested_capital += etf.starting_capital
        self.actual_invested_capital = self.invested_capital * 0.6 # assuming 40% tax would be removed

    def exit_investment(self):
        self.get_invested_capital()
        exit_capital_before_tax= 0
        for etf in self.etfs:
            etf.exit_investment()
            exit_capital_before_tax += int(etf.exit_capital)
        if exit_capital_before_tax < 200000:
            self.exit_capital = exit_capital_before_tax
            self.tax_paid = 0
            smart_print(f"PENSION_EXIT_INVESTMENT: exit capital below 200000, no tax applied", True)
        elif exit_capital_before_tax > 200000 and exit_capital_before_tax < 500000:
            self.exit_capital = 200000 + (exit_capital_before_tax-200000)*0.8 # amount above 200.000 taxed at 20%
            self.tax_paid = exit_capital_before_tax - self.exit_capital
            smart_print(f"PENSION_EXIT_INVESTMENT: 200.000<exit capital<500000, exit_capital_before tax {exit_capital_before_tax}, exit_capital_after_taxes {self.exit_capital}, tax paid {self.tax_paid}", True)
        elif exit_capital_before_tax > 500000:
            self.exit_capital = 200000 + 300000*0.8 + (exit_capital_before_tax-500000)*0.52 #Considering Marginal Rate 41% income tax, 7% USC. Excluding 4% PRSI
            self.tax_paid = exit_capital_before_tax - self.exit_capital
            smart_print(f"PENSION_EXIT_INVESTMENT: exit capital>500000, exit_capital_before tax {exit_capital_before_tax}, exit_capital_after_taxes {self.exit_capital}, tax paid {self.tax_paid}", True)

        else:
            raise ValueError("PensionPortfolio:value outside range")

    def get_gain_percentage(self):
        return int((self.exit_capital / self.actual_invested_capital) * 100 - 100)

    def get_gain_absolute(self):
        return int((self.exit_capital - self.actual_invested_capital))

    def __repr__(self):
        return f"PENSION REPORT. Name {self.name}, invested capital {self.invested_capital}, actual invested capital {self.actual_invested_capital} exit capital {self.exit_capital}, percentage gain {self.get_gain_percentage()}, absolute gain {self.get_gain_absolute()},eft# {len(self.etfs)}"

















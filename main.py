from investment import *
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



'''Old code, reference only'''
def single_etf_simulation():

    etf_irlanda = EtfIrlanda(STARTING_CAPITAL,0)
    etf_italia = EtfItalia(STARTING_CAPITAL,0)
    year = 0

    print(f"Starting capital:{STARTING_CAPITAL}")
    while year < 20:
        etf_irlanda.yearly_cycle()
        etf_italia.yearly_cycle()
        etf_ratio = round((etf_italia.current_capital/etf_irlanda.current_capital)*100 - 100,2)
        capital_difference = int(etf_italia.current_capital - etf_irlanda.current_capital)
        print(f"Year {year}: etf_italia {int(etf_italia.current_capital)}, etf_irlanda {int(etf_irlanda.current_capital)}. Ratio {etf_ratio}, capital difference {capital_difference}")
        year = year + 1

    etf_italia.exit_investment()
    etf_irlanda.exit_investment()


    print(f"TAX_APPLICATION. etf_italia CGT {TAX_ETF_ITALIA}, pre-tax value {int(etf_italia.current_capital)}, after tax value: {int(etf_italia.exit_capital)}. Total tax payed:{round(etf_italia.capital_gain_tax,2)}")
    print(f"TAX_APPLICATION. etf_italia CGT {TAX_ETF_IRLANDA}, pre-tax value {int(etf_irlanda.current_capital)}, after tax value: {int(etf_irlanda.exit_capital)}. Total tax payed:{round(etf_irlanda.capital_gain_tax,2)}")


    print(f"END_OF_INVESTMENT. etf_italia percentage gain {etf_italia.get_gain_percentage()}%, etf_italia absolute gain {etf_italia.get_gain_absolute()} euro")
    print(f"END_OF_INVESTMENT. etf_irlanda percentage gain {etf_irlanda.get_gain_percentage()}%, etf_italia absolute gain {etf_irlanda.get_gain_absolute()} euro")
    print(f"END_OF_INVESTMENT. etf_italia/irlanda percentage gain difference {etf_italia.get_gain_percentage()-etf_irlanda.get_gain_percentage()}, etf_italia/irlanda absolute gain difference {etf_italia.get_gain_absolute() - etf_irlanda.get_gain_absolute()}")


'''Test ETF IRELAND BEHAVIOUR'''
def updated_etf_irlanda_per_unit(input_year=0, input_unit_value=1):
    year = input_year
    unit_value = input_unit_value
    etf_irlanda = EtfIrlanda(STARTING_CAPITAL, 0, unit_value)

    while year < YEARS:
        smart_print(year)
        etf_irlanda.yearly_cycle()
        year += 1

    smart_print(etf_irlanda, True)
    etf_irlanda.exit_investment()


'''Test ETF PENSION SINGLE INVESTMENT BEHAVIOUR'''
def single_pension_investment_simulation(input_year=0, input_unit_value=1):
    year = input_year
    unit_value = input_unit_value
    pension_investment = PensionInvestment(STARTING_CAPITAL, 0, unit_value)

    while year < YEARS:
        smart_print(year)
        pension_investment.yearly_cycle()
        year += 1

    pension_investment.exit_investment()
    print(pension_investment)

def portfolio_simulation():
    year = 0
    unit_value = 1
    unit_value_multiplier = 1 + INTEREST_RATE
    portfolio_ireland = Portfolio("portfolio_ireland")
    print(f"=====LEGEND=====\nbet == before exit taxes\naet == after exit taxes \n")

    while year < YEARS:
        smart_print(year)
        etf_ireland = EtfIrlanda(STARTING_CAPITAL,year,unit_value)
        if year == 0: #this is to remove pac, only initial capital. Remove this line and fix indent for line below to Add Pac
            portfolio_ireland.perform_pac(etf_ireland)
        portfolio_ireland.yearly_cycle()
        year += 1
        unit_value = unit_value * unit_value_multiplier
    portfolio_ireland.exit_investment()
    smart_print(portfolio_ireland,True)
    return portfolio_ireland



def pension_simulation():
    year = 0
    unit_value = 1
    unit_value_multiplier = 1 + INTEREST_RATE
    pension_ireland = PensionPortfolio("pension_ireland")
    gross_capital = STARTING_CAPITAL / 0.6 # getting gross value that goes into pension. x - 0.4x = y -> x = y / 0.6. Where x = gross value before taxes
    while year < YEARS:
        pension_investement = PensionInvestment(gross_capital,year,unit_value)
        pension_ireland.perform_pac(pension_investement)
        pension_ireland.yearly_cycle()
        year += 1
        unit_value = unit_value * unit_value_multiplier
    pension_ireland.exit_investment()
    smart_print(pension_ireland, True)
    return pension_ireland

'''Previous output
etf_portfolio = portfolio_simulation()
pension = pension_simulation()

print("\n\n===============FINAL REPORT===============")
print("Comparing Investment via etf with investment via pension over the same time range. Same capital investment, same market behaviour(different fees)")
print(f"ABSOLUTE CAPITAL: pension {pension.exit_capital}, etf investment {etf_portfolio.exit_capital}")
print(f"growth difference: {round((pension.exit_capital/etf_portfolio.exit_capital)*100,2) - 100}%")
'''
etf_portfolio = portfolio_simulation()
print(f"ABSOLUTE CAPITAL:  etf investment {etf_portfolio.exit_capital}")


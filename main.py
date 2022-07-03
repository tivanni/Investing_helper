from investment import *
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


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


def portfolio_simulation ():

    year = 0
    portfolio_irlanda = Portfolio("etf_irlanda")
    print(f"=====LEGEND=====\nbet == before exit taxes\naet == after exit taxes \n")

    while year < YEARS:
        print(year)
        if year == 0:
            etf_irlanda = EtfIrlanda(STARTING_CAPITAL, year)
            portfolio_irlanda.perform_pac(etf_irlanda)
        portfolio_irlanda.yearly_cycle()
        year += 1

    etf_irlanda.exit_investment()
    '''
    print("=====END OF INVESTMENT=====")
    portfolio_irlanda.exit_investment()
    print(portfolio_irlanda)
    print("\n")
    '''

def updated_etf_irlanda_per_unit():
    year = 0
    unit_value = 1
    etf_irlanda = EtfIrlanda(STARTING_CAPITAL, 0, unit_value)

    while year < YEARS:
        print(year)
        etf_irlanda.yearly_cycle()
        year += 1

    etf_irlanda.exit_investment()




updated_etf_irlanda_per_unit()
#### single etf completely reviewed, continue with 1)evaluate adding dividends 2) portfolio
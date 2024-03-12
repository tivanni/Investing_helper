from mortgage import Loan
from investment import Portfolio, EtfIrlanda
from settings import INTEREST_RATE
from helpers import smart_print
from prettytable import PrettyTable

'''
This script aim to help answering the question: "if every month I have a sum X available to invest between Mortgage and
a portolio of financial assets(e.g ETF), what is the combination that maximizes my total return?"
Paying the mortgage earlier result in lower cost of mortgage (and viceversa)
Investing more money and for longer term in financial assets (should) result in higher returns (and vice versa). 
The total return is calculated as return obtained from financial investment minus the cost of mortgage.
Taxation for the ETF portfolio is modeled as per Irish Laws, and includes deemed disposal payment.
The script does NOT model inflation nor the value of the house at the end of the simulation window, as these are
orthogonal to the goal. To better understand the concept, the question this script aim to help answer can be rephrased as
"what is the best way to pay my mortgage while investing in financial assets?"
The needs of mortgage and investment are in competition between each other, and the best prioritization depends on
mortgage details (principal, interest, term, partner contribution) and investment details (expected return)
The behaviour of the script is simple. For a given mortgage principal and interest, and a given amount of money available
to invest per month, the script simulates the total return obtained over a fixed time window (e.g 20 years) with
mortgages of different terms. While the mortgage is active, the amount of money invested in the financial asset 
portfolio equals to the total sum available per month minus the monthly mortgage payment. When the mortgage expires,
all the money available is invested in the financial assets.
The script allows to change all the relevant input values and print as output the expected total return for all the
different mortgage terms. hope it's helpful!
'''

#Define inputs
##Mortgage Inputs
MORTGAGE_TERMS_TO_SIMULATE = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6]
MORTGAGE_PRINCIPAL = 300000
MORTGAGE_INTEREST_RATE = .0475 # 3.75%
MORTGAGE_PARTNER_CONTRIBUTION = 500
##Investment Inputs
TOTAL_MONEY_TO_INVEST_MONTHLY = 4000
INVESTMENT_INTEREST_RATE = 0.22
##Time Inputs
TOTAL_YEARS_TO_SIMULATE = INTEREST_RATE # changing value on this file will not affect computation

#verify mortgage terms do not exceed total years of simulation
assert max(MORTGAGE_TERMS_TO_SIMULATE) <= TOTAL_YEARS_TO_SIMULATE, ("Mortgage terms can't be longer than total years of"
                                                                    "simulation")

#storing output results
results = {}

for mortgageTerm in MORTGAGE_TERMS_TO_SIMULATE:
    smart_print(f"mortgage term:{mortgageTerm}", False)

    #define loan variables
    loan = Loan(principal=MORTGAGE_PRINCIPAL, interest=MORTGAGE_INTEREST_RATE,term=mortgageTerm, currency='€')
    loan_monthly_contribution_personal = int(loan.monthly_payment) - MORTGAGE_PARTNER_CONTRIBUTION
    smart_print(f"Loan monthly payment:{int(loan.monthly_payment)}, share of monthly payment: "
                f"{loan_monthly_contribution_personal}", False)

    #setup variables required by Portfolio
    portfolio_unit_value = 1
    portfolio_unit_value_multiplier = 1 + INTEREST_RATE
    portfolio = Portfolio("portfolio")


    #begin modelling
    year = 0
    while year < TOTAL_YEARS_TO_SIMULATE:
        smart_print(year, False)

        #Money available for investment depends on mortgage payment
        money_to_invest_monthly = TOTAL_MONEY_TO_INVEST_MONTHLY
        if year < mortgageTerm:
            # loan.monthly_payment is a Decimal
            money_to_invest_monthly = TOTAL_MONEY_TO_INVEST_MONTHLY - loan_monthly_contribution_personal

            #store the monthly payment with mortgage for later
            if year == 0:
                money_to_invest_monthly_w_mortgage = money_to_invest_monthly

        #do not compute if can't afford the mortgage
        if money_to_invest_monthly < 0:
            print(f"Money to invest montlhy is negative, skipping computation for mortgage term {mortgageTerm}")
            break
        smart_print(f"Money to Invest monthly: {money_to_invest_monthly}", False)
        money_to_invest = money_to_invest_monthly * 12
        portfolio.perform_pac(EtfIrlanda(money_to_invest,year,portfolio_unit_value))
        portfolio.yearly_cycle()
        year += 1
        portfolio_unit_value = portfolio_unit_value * portfolio_unit_value_multiplier

    # do not compute if can't afford the mortgage
    if money_to_invest_monthly < 0:
        continue
    portfolio.exit_investment()
    total_return = portfolio.exit_capital - int(loan.total_interest)
    mortgageTermResult = {'total_return':total_return, 'portfolio_return': portfolio.exit_capital,
                         'investment_gain': portfolio.get_gain_absolute(), 'mortgage_cost': int(loan.total_interest),
                          'money_to_invest_monthly_w_mortgage': money_to_invest_monthly_w_mortgage,
                          'money_to_invest_without_mortgage': money_to_invest_monthly}
    results[mortgageTerm] = mortgageTermResult
    smart_print("\n\n", False)

#enrich results with comparison with best value
best_total_return = max([results[key]['total_return'] for key in results.keys()])

for result in results.values():
    result['difference_from_best_return'] = result['total_return'] - best_total_return


#Print a nice table for the user
table_header = ['Mortgage Term', 'Total Return', 'Difference from Best Return', 'Portfolio Return', 'Portfolio Gain',
                'Morgage Cost', 'Money To Invest Monthly w/ mortgage', 'Money To Invest Monthly without mortgage']
table = PrettyTable(table_header)
for key, value in results.items():
    table.add_row([key, f"{value['total_return']:,}", f"{value['difference_from_best_return']:,}",
                   f"{value['portfolio_return']:,}",f"{value['investment_gain']:,}", f"{value['mortgage_cost']:,}",
                   f"{value['money_to_invest_monthly_w_mortgage']:}",f"{value['money_to_invest_without_mortgage']:,}"
                   ])
print("\nINPUTS:")
print(f"[Mortgage inputs] Mortgage Principal: {MORTGAGE_PRINCIPAL:,}, Mortgage Interest: {MORTGAGE_INTEREST_RATE*100}%,",
      f"Mortgage Partner Contribution: {MORTGAGE_PARTNER_CONTRIBUTION:,}")
print(f"[Investment inputs] Total Money To Invest Monthly: {TOTAL_MONEY_TO_INVEST_MONTHLY:,}, Expected Yearly Return(avg)"
      f": {INVESTMENT_INTEREST_RATE*100:.2f}%")
print(f"[Time inputs] Length of Simulation(years): {TOTAL_YEARS_TO_SIMULATE}")
print(f"[Currency inputs] Currency:'€'")
print(f"[Note on Tax] Total Return and Portfolio Return are Irish Taxes included(w/ deemed disposal)")
print(f"\n")
print(table)



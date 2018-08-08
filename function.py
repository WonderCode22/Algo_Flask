import re
import numpy


# This function gets the text for the trigger, trade and security and a price series
# It returns two series, one represents the position on each day and the other one
# is the daily Pnl
def algo_result(condition, action, prices):
    comparisons = ['larger than', 'smaller than']

    for comparison in comparisons:
        search_res = re.findall(comparison, condition)

        if len(search_res) == 1:
            condition_parts = condition.split(comparison)
            break
        else:
            print('This condition is not supported yet')
            exit()

    avg_price = []

    # Here we calculate the moving averages for those two windows
    MA = []
    for condition_part in condition_parts:

        # find the MA window
        period = re.findall('\d+ \w+', condition_part)[0]
        period = period.split()

        if period[1] == 'days':
            num_days = int(period[0])
        else:
            if period[1] == 'weeks':
                num_days = int(period[0]) * 5  # a world without holidays!
            else:
                print('please use the time period in days or weeks')
                exit()

        # calculate MA
        MA.append([numpy.mean(prices[i - num_days:i]) for i in range(1, len(prices) + 1)])

    # Get buy/sell signal
    MA0 = numpy.array(MA[0])
    MA1 = numpy.array(MA[1])

    if comparison == 'larger than':
        buy_sell = MA0 > MA1
    else:
        buy_sell = MA0 < MA1

    # Create positions and PnL
    num_shares = re.findall('\d+', action)
    num_shares = int(num_shares[0])

    positions = [0]
    PnL = [0]
    for i in range(1, len(prices) - 1):
        if buy_sell[i]:
            positions.append(positions[i - 1] + num_shares)
        else:
            positions.append(0)

        PnL.append(positions[i - 1] * (prices[i] - prices[i - 1]))

    return positions, PnL


# def main():
#     prices = [1.2, 3, 2, 4.3, 3.3, 5.3, 1.2, 3, 3.7, 3.2, 4.4]
#
#     trigger = '2 days moving average larger than 5 days moving average'
#     trade = 'buy 50 shares'
#     # it assumes it should sell if the condition does not hold
#
#     [positions, PnL] = algo_result(trigger, trade, prices)
#
#     print(positions)
#     print('\n')
#     print(PnL)

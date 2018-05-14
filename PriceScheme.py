import numpy as np
from scipy.optimize import minimize

from app import *
from Bidders import *

def main():

    APP_COUNT = 10

    apps = []
    for i in range(APP_COUNT):
        apps.append(Application(i))

    IMPRESSIONS_WANTED = 50000

    opt_bidder = OptimizedBidder(apps, IMPRESSIONS_WANTED) #0
    rand_bidder = RandBidder(IMPRESSIONS_WANTED) #1
    fixed_bidder = FixedBidder(app.MEAN_BANNER, IMPRESSIONS_WANTED) #2

    # How many auctions to conduct?
    auction_count = 0
    for i in range(len(apps)):
        auction_count += apps[i].total_impressions

    print("Number of auctions to conduct: " + str(auction_count))

    auctioneer = Auctioneer(apps)

    wins = [0, 0, 0]
    cost = [0, 0, 0]

    while auction_count > 0:
        br = auctioneer.generate_bid_request()

        bid_prices = []

        bid_prices.append(opt_bidder.get_bid_price(br['app_id']))
        bid_prices.append(rand_bidder.get_bid_price(br['app_id']))
        bid_prices.append(fixed_bidder.get_bid_price(br['app_id']))

        dat = auctioneer.conduct_auction(br, bid_prices)

        winners = dat['winners']
        win_price = dat['win_price']

        for i in range(len(winners)):
            wins[winners[i]] += 1
            cost[winners[i]] += win_price

            if winners[i] == 0:
                opt_bidder.impressions_won += 1
            elif winners[i] == 1:
                rand_bidder.impressions_won += 1
            elif winners[i] == 2:
                fixed_bidder.impressions_won += 1

        auction_count -= 1

    print("Impressions won: ")
    print(wins)

    print("Total Cost: ")
    print(cost)

if __name__ == "__main__":
    main()


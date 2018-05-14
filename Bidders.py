import numpy as np
import app
from scipy.optimize import minimize

class RandBidder():

    def __init__(self, impressions_wanted):
        self.impressions_wanted = impressions_wanted
        self.impressions_won = 0

    def get_bid_price(self, app_id):
        if self.impressions_won >= self.impressions_wanted:
            return 0
        return np.random.rand()*15


class FixedBidder:

    def __init__(self, bid_price, impressions_wanted):
        self.impressions_wanted = impressions_wanted
        self.impressions_won = 0
        self.bid_price = bid_price

    def get_bid_price(self, app_id):
        if self.impressions_won >= self.impressions_wanted:
            return 0
        return self.bid_price

class OptimizedBidder:

    def __init__(self, apps, impressions_wanted):
        self.impressions_wanted = impressions_wanted
        self.impressions_won = 0
        APP_COUNT = len(apps)

        cons = []

        def num_impressions(x):

            imps = []

            for k in range(APP_COUNT):
                imp = np.interp(x[k], app.bins, apps[k].imp_curve)
                imps.append(imp)

            return sum(imps)

        def objective(x):
            costs = []

            for i in range(APP_COUNT):

                cost = apps[i].compute_area(x[i])
                costs.append(cost)
            return sum(costs)

        # Build the constraints
        for i in range(APP_COUNT):
            jac = np.zeros(APP_COUNT)
            jac[i] = 1.0

            cons.append({
                'type': 'ineq',
                'fun': lambda x: np.array([x[i]]),
                'jac': lambda x: jac
            })

        cons.append({
            'type': 'ineq',
            'fun': lambda x: np.array([num_impressions(x) - impressions_wanted])
        })

        cons = tuple(cons)
        x0 = [0.5] * APP_COUNT

        self.prices = minimize(objective, np.array(x0), method='COBYLA',
                       options={'disp': True}, constraints=cons).x

        for i in range(len(self.prices)):
            if self.prices[i] < 0:
                self.prices[i] =0

        print(self.prices)
        print(len(self.prices))

    def get_bid_price(self, app_id):
        if self.impressions_won >= self.impressions_wanted:
            return 0
        return self.prices[app_id]

    # Function performs an exhaustive search to find the optimal prices.
    # Obviously won't work for a large number of applications.
    #def exhaustive_search(self):

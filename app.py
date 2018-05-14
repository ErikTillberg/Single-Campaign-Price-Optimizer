import numpy as np

MEAN_POPULARITY = 10000
MEAN_BANNER = 1.50
MEAN_INTERSTITIAL = 5.50

bins = np.arange(0, 15, 0.01)

class Application():

    def __init__(self, id = None):
        if id is not None:
            self.id = id

        self.imp_curve = self._generate_curve()

    def _generate_curve(self):
        """
        Generates an impression curve for this application.
        :return:
        """
        popularity = int(np.random.normal(MEAN_POPULARITY, MEAN_POPULARITY/2))
        while popularity < 0:
            popularity = int(np.random.normal(MEAN_POPULARITY, MEAN_POPULARITY / 2))

        dist_banner = np.random.normal(MEAN_BANNER, 1.5, popularity)
        dist_interstitial = np.random.normal(MEAN_INTERSTITIAL, 5.5, int(popularity/1.5))

        dist_banner = _bound_distribution(dist_banner)
        dist_interstitial = _bound_distribution(dist_interstitial)

        self.dist_total = np.array(list(dist_banner) + list(dist_interstitial))

        self.total_impressions = len(self.dist_total)

        # Histogram bins
        hist = np.histogram(self.dist_total, bins)

        c = np.cumsum(hist[0])

        c = list(c) + list([c[len(c)-1]])

        return c

    # Computes the area above the impression curve, and below the number
    # of impressions gained at 'price'.
    def compute_area(self, price):

        area = 0
        for i, p in enumerate(bins):
            if p > price or (i+1)>len(self.imp_curve)-1:
                break
            temp = (self.imp_curve[i+1]-self.imp_curve[i])*p
            area += temp

        return area

def _bound_distribution(dist):

    for i in range(len(dist)):
        if dist[i] < 0:
            dist[i] = 0

    return dist

class Auctioneer():

    def __init__(self, apps):
        self.apps = apps

        num_apps = len(apps)
        temp = []

        # Generate the distribution of which app to come from
        for i in range(num_apps):
            temp.append(float(sum(self.apps[i].imp_curve)))

        temp = np.array(temp)/sum(temp)

        self.dist = []
        for i in range(len(temp)):
            self.dist.append(sum(temp[:i])+temp[i])



    def generate_bid_request(self):

        # Generate an app to come from
        chosen_app = self._get_app()


        return {
            'app_id': chosen_app.id,
            'app': chosen_app
        }

    def conduct_auction(self, bid_request, bid_prices):

        chosen_app = bid_request['app']

        win_price = chosen_app.dist_total[np.random.randint(0, len(chosen_app.dist_total))]

        winners = []

        for i in range(len(bid_prices)):
            if bid_prices[i] > win_price:
                winners.append(i)

        return {
            'winners': winners,
            'win_price': win_price
        }

    def _get_app(self):
        rand = np.random.rand()
        for i in range(len(self.apps)):
            if rand < self.dist[i]:
                return self.apps[i]
import market
import pathfinding
import numpy as np

test_buyer_0 = market.Buyer(100, 30, 5)
test_buyer_1 = market.Buyer(50, 50)
test_buyer_2 = market.Buyer(20, 100)
market = market.Market()
market.add_buyer(test_buyer_0)
market.add_buyer(test_buyer_1)
market.add_buyer(test_buyer_2)
#market.run_bid()
market.run_market()
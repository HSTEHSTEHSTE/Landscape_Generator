import path
import numpy as np
import market

def run_path_test():
    map = np.loadtxt('map_saves/main.csv', delimiter = ',')
    map_landmass = np.loadtxt('map_saves/landmass.csv', delimiter = ',')
    pathFinder = path.PathFinder(map)
    pathFinder.find_path([238, 40], [239, 74])#([238, 75], [239, 74])
    print('manhattan distance: ', pathFinder.get_manhattan_distance())
    pathFinder.print_path()
    
def run_sea_path_test():
    map = np.loadtxt('map_saves/main.csv', delimiter = ',')
    map_landmass = np.loadtxt('map_saves/landmass.csv', delimiter = ',')
    pathFinder = path.PathFinder(map)
    pathFinder.map_values(0, 2)
    pathFinder.map_values(-10, 5)
    pathFinder.map_values(-20, 9)
    pathFinder.find_path([201, 0], [191, 8])#([238, 75], [239, 74])
    print('manhattan distance: ', pathFinder.get_manhattan_distance())
    pathFinder.print_path()
    
def run_market_test():
    test_buyer_0 = market.Buyer(100, 30, 5)
    test_buyer_1 = market.Buyer(50, 50)
    test_buyer_2 = market.Buyer(20, 100)
    marketplace = market.Market()
    marketplace.add_buyer(test_buyer_0)
    marketplace.add_buyer(test_buyer_1)
    marketplace.add_buyer(test_buyer_2)
    #marketplace.run_bid()
    marketplace.run_market()
    
run_sea_path_test()
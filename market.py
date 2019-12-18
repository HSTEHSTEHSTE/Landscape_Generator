import math

class Buyer():
    def __init__(self, amount_0, value_max, surcharge = 0):
        self.amount_0 = float(amount_0)
        self.value_max = float(value_max)
        self.amount_held = 0
        self.amount_0_original = self.amount_0
        self.value_max_original = self.value_max
        self.surcharge = surcharge
        self.value_paid = 0

    def get_amount_by_value(self, value):
        value += self.surcharge
        if value > self.value_max:
            return 0
        elif self.value_max > 0:
            return math.floor(self.amount_0 / self.value_max * (self.value_max - value))
        else:
            return 0

    def get_value_by_amount(self, amount):
        return self.value_max / self.amount_0 * (self.amount_0 - amount)

    def add_amount_held(self, amount, value):
        self.amount_held += amount
        self.amount_0 -= amount
        self.value_max = self.value_max / (self.amount_0 + amount) * self.amount_0
        self.value_paid += (value + self.surcharge) * amount
        
    def reset(self):
        self.amount_held = 0
        self.value_max = self.value_max_original
        self.amount_0 = self.amount_0_original
        self.value_paid = 0

class Market():
    def __init__(self, price_0 = 0, marginal_production = 20, total_production = 1000, initial_price = 100, buyer_list = []):
        self.total_production = total_production
        self.initial_price = initial_price
        self.buyer_list = buyer_list
        self.price_0 = price_0
        self.marginal_production = marginal_production
    
    def add_buyer(self, buyer):
        self.buyer_list.append(buyer)
    
    def set_buyer_list(self, buyer_list):
        self.buyer_list = buyer_list
    
    def run_bid(self):
        price = self.initial_price
        price_step = 1
        production = self.total_production
        while production > 0 and price >= 0:
            print("Bidding at", price, "Production", production)
            interest = 1
            while interest == 1:
                amount_list = []
                for buyer in self.buyer_list:
                    amount_list.append(buyer.get_amount_by_value(price))
                max_amount = max(amount_list)
                if max_amount > 0:
                    buyer_index = amount_list.index(max_amount)
                    buyer = self.buyer_list[buyer_index]
                    if max_amount > production:
                        buyer.add_amount_held(production, price)
                        print("Amount", production, "sold to", buyer_index)
                        production = 0
                        interest = 0
                        print("End bidding")
                    else:
                        buyer.add_amount_held(max_amount, price)
                        production -= max_amount
                        print("Amount", max_amount, "sold to", buyer_index)
                else:
                    interest = 0
            price -= price_step
        for buyer in self.buyer_list:
            print("Amount: ", buyer.amount_held, "Value: ", buyer.value_paid)
            
    def reset_buyers(self):
        for buyer in self.buyer_list:
            buyer.reset()
    
    def get_production_by_price(self, price):
        return min((price - self.price_0) * self.marginal_production, self.total_production)
    
    def run_market(self):
        price = self.price_0
        price_step = 1
        found = 0
        maxed_out_production = 0
        while found == 0:
            demand = 0
            for buyer in self.buyer_list:
                demand += buyer.get_amount_by_value(price)
            supply = self.get_production_by_price(price)
            if supply == self.total_production:
                maxed_out_production = 1
            print("Bidding at", price, "Supply", supply, "Demand", demand)
            if supply > demand:
                found = 1
            else:
                price += price_step
        for buyer in self.buyer_list:
            amount = buyer.get_amount_by_value(price)
            buyer.add_amount_held(amount, price)
            buyer_index = self.buyer_list.index(buyer)
            print("Amount", amount, "sold to", buyer_index)
        print("End bidding")
        for buyer in self.buyer_list:
            print("Amount: ", buyer.amount_held, "Value: ", buyer.value_paid)
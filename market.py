import math

production = 20;

class buyer():
    def __init__(self, amount_0, value_max):
        self.amount_0 = float(amount_0)
        self.value_max = float(value_max)
        self.amount_held = 0
        self.amount_0_original = self.amount_0
        self.value_max_original = self.value_max
        
    def get_amount_by_value(self, value):
        if value > self.value_max:
            return 0
        elif self.value_max > 0:
            return math.floor(self.amount_0 / self.value_max * (self.value_max - value))
        else:
            return 0
            
    def get_value_by_amount(self, amount):
        return self.value_max / self.amount_0 * (self.amount_0 - amount)
        
    def add_amount_held(self, amount):
        self.amount_held += amount
        self.amount_0 -= amount
        self.value_max = self.value_max / (self.amount_0 + amount) * self.amount_0

buyer_list = []
test_buyer_0 = buyer(10, 3)
buyer_list.append(test_buyer_0)
test_buyer_1 = buyer(5, 5)
buyer_list.append(test_buyer_1)
price = 100
price_step = 1
while production > 0 and price >= 0:
    print("Bidding at", price, "Production", production)
    interest = 1
    while interest == 1:
        amount_list = []
        for buyer in buyer_list:
            amount_list.append(buyer.get_amount_by_value(price))
        max_amount = max(amount_list)
        if max_amount > 0:
            buyer_index = amount_list.index(max_amount)
            buyer = buyer_list[buyer_index]
            if max_amount > production:
                buyer.add_amount_held(production)
                print("Amount", production, "sold to", buyer_index)
                production = 0
                interest = 0
                print("End bidding")
            else:
                buyer.add_amount_held(max_amount)
                production -= max_amount
                print("Amount", max_amount, "sold to", buyer_index)
        else:
            interest = 0
    price -= price_step
    
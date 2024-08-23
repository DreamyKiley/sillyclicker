class Upgrade:
    def __init__(self, cost, increment, max_level):
        self.cost = cost
        self.increment = increment
        self.level = 0
        self.max_level = max_level

    def can_buy(self, money):
        return money >= self.cost and self.level < self.max_level

    def buy(self, money):
        if self.can_buy(money):
            money -= self.cost
            self.level += 1
            return money, self.increment
        return money, 0

    def get_button_text(self):
        if self.level >= self.max_level:
            return "Max"
        return f"Upgrade (Cost: ${self.cost})"


class Autoclicker:
    def __init__(self, cost):
        self.cost = cost
        self.active = False

    def can_buy(self, money):
        return money >= self.cost and not self.active

    def buy(self, money):
        if self.can_buy(money):
            money -= self.cost
            self.active = True
        return money

    def get_button_text(self):
        if self.active:
            return "Autoclicker Active"
        return f"Buy Autoclicker (Cost: ${self.cost})"

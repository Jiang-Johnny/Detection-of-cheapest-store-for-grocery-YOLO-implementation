class Aggregator:

    def __init__(self):

        self.data = {}

    def add(self, store, item, price):

        if store not in self.data:

            self.data[store] = {}

        self.data[store][item] = price

    def get(self):

        return self.data

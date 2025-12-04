class Comparer:

    def find_cheapest(self, data, shopping_list):

        best_store = None
        best_total = float("inf")

        for store, items in data.items():

            total = 0
            valid = True

            for item, qty in shopping_list.items():

                if item not in items:

                    valid = False

                    break

                total += items[item] * qty

            if valid and total < best_total:

                best_store = store
                best_total = total

        return best_store, best_total

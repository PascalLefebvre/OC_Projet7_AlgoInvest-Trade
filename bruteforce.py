"""Brute force algorithm."""


import csv

ACTIONS_LIST_FILE = "ActionsList.csv"
MAX_INVESTMENT = 500

actions, all_actions, all_combinations = [], [], []
best_combination = { 'actions': [], 'profit': 0 }


class Action:
    """Classe des actions"""

    def __init__(self, name, price, profit) -> None:
        self.name = name
        self.price = price
        self.profit = price*(profit/100) # Convert percent profit in euros        


"""Fill the "actions" array with action objects from the CSV file."""
def fill_actions_array():
    with open(ACTIONS_LIST_FILE) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for line in reader:
            actions.append(Action(line['name'], int(line['price']), int(line['profit'])))


"""Initialize combinations array with the simplest combinations (one combination = one action)
   and the full combination (the combination with all the actions)."""
def initialize_combinations_array():
    for action in actions:
        all_combinations.append([action])
        all_actions.append(action)
    all_combinations.append(all_actions)

"""Find all combinations and save them in "all_combinations" array."""
def find_all_combinations():
    # "prefix_length" corresponds to the number of actions grouped together to be added to each of the other actions.
    for prefix_length in range(1,len(actions)-1):
        # "combinations_indexes" array contains the indexes corresponding
        # to the positon of the action in the "actions" array.
        combinations_indexes = []
        combination_length = prefix_length + 1
        # Initialize the "combinations_indexes" array
        for i in range(combination_length):
            combinations_indexes.append(i)
        while combinations_indexes[0] <= len(actions)-1-prefix_length:
            last_index = combinations_indexes[-1]
            while combinations_indexes[-1] <= len(actions)-1:
                combination = []
                for i in range(combination_length):
                    combination.append(actions[combinations_indexes[i]])
                all_combinations.append(combination)
                combinations_indexes[-1] += 1
            for i in range(combination_length-1):
                combinations_indexes[i] += 1
            combinations_indexes[-1] = last_index +1

"""Calculate the total profit of the combination of actions."""
def calculate_combination_profit(combination):
        investment, profit = 0, 0
        for action in combination:
            investment += action.price
            if (investment > MAX_INVESTMENT):
                return None
            profit += action.profit
        return profit

def keep_best_combination():
    for combination in all_combinations:
        combination_profit = calculate_combination_profit(combination)
        if combination_profit is not None:
            if combination_profit > best_combination['profit']:
                best_combination['actions'] = combination
                best_combination['profit'] = combination_profit

def display_result():
    print(f"\nLe nombre de combinaisons trouvées est de {len(all_combinations)}.")
    print(f"\nLa meilleure combinaison d'actions est : \n")
    investment, profit = 0, 0
    for action in best_combination['actions']:
        print(action.name)
        investment += action.price
        profit += action.profit
    print(f"\npour un profit maximum  de {profit} et un investissement de {investment}.")

def main():
    fill_actions_array()
    initialize_combinations_array()
    find_all_combinations()
    keep_best_combination()
    display_result()

if __name__ == "__main__":
    main()

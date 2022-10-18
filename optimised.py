"""Optimised algorithm."""


import csv

ACTIONS_LIST_FILE = "ActionsList.csv"
MAX_INVESTMENT = 500

actions, actions_states = [], []
right_leaf_nodes = [] # Nodes Upper Bound Values


class Action:
    """Actions class"""

    def __init__(self, name, price, percentage_profit) -> None:
        self.name = name
        self.price = price
        self.percentage_profit = percentage_profit
        self.profit_amount = price*(percentage_profit/100)
    
    def __str__(self):
        return f"{self.name} / {self.percentage_profit} % / {self.price} € / {round(self.profit_amount,2)} €"


class Node:
    """Nodes class"""

    def __init__(self, ubv, sum_profits, sum_prices, depth, state, parent_node) -> None:
        self.ubv = ubv # Upper Bound Value
        self.sum_profits = sum_profits
        self.sum_prices = sum_prices
        self.depth = depth
        self.state = state
        self.parent = parent_node
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,new_node):
        self.leftChild = new_node
    
    def insertRight(self,new_node):
        self.rightChild = new_node


"""Fill the "actions" list with action objects from the CSV file."""
def fill_actions_list():
    with open(ACTIONS_LIST_FILE) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for line in reader:
            actions.append(Action(line['name'], float(line['price']), float(line['profit'])))

def merge_sort(list):
    if len(list) > 1:
        mid = len(list)//2
        lefthalf = list[:mid]
        righthalf = list[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)

        i, j, k = 0, 0, 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i].percentage_profit <= righthalf[j].percentage_profit:
                list[k]=lefthalf[i]
                i += 1
            else:
                list[k]=righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            list[k]=lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            list[k]=righthalf[j]
            j += 1
            k += 1
    return list

def calculate_ubv_value():
    sum_profits = 0
    investment = 0
    for i in range(len(actions)-1, -1, -1):
        if actions_states[i] == 1:
            investment += actions[i].price
            sum_profits += actions[i].profit_amount
            if investment > MAX_INVESTMENT:
                investment -= actions[i].price
                sum_profits -= actions[i].profit_amount
                # Split up the amount profit of the last reviewed action to achieve the exact MAX_INVESTMENT amount
                sum_profits += (actions[i].profit_amount/actions[i].price)*(MAX_INVESTMENT-investment)
                return sum_profits
    return sum_profits

def update_actions_states(node):
    while node.parent != None:
        actions_states[len(actions)-node.depth] = node.state
        node = node.parent
    return actions_states

def expand_tree(parent_node):
    global actions_states, right_leaf_nodes
    if parent_node.depth == len(actions):
        actions_states = update_actions_states(parent_node)
        return None
    index = len(actions)-parent_node.depth-1
    actions_states[index] = 0
    right_node = Node(calculate_ubv_value(), parent_node.sum_profits, parent_node.sum_prices,
                      parent_node.depth+1, 0, parent_node)
    actions_states[index] = 1
    parent_node.insertRight(right_node)
    actions_states = update_actions_states(parent_node)
    if parent_node.sum_prices+actions[index].price <= MAX_INVESTMENT:
        left_node = Node(parent_node.ubv, parent_node.sum_profits+actions[index].profit_amount,
                            parent_node.sum_prices+actions[index].price, parent_node.depth+1, 1, parent_node)
        parent_node.insertLeft(left_node)
        right_leaf_nodes.append((right_node))
        if len(right_leaf_nodes) >= 2:
            if right_node.ubv < right_leaf_nodes[-2].ubv:
                right_leaf_nodes = sorted(right_leaf_nodes, key=lambda node: node.ubv)
        expand_tree(left_node)
    else:
        right_leaf_nodes.append((right_node))
        if len(right_leaf_nodes) >= 2:
            if right_node.ubv < right_leaf_nodes[-2].ubv:
                right_leaf_nodes = sorted(right_leaf_nodes, key=lambda node: node.ubv)
        expand_tree(right_leaf_nodes.pop())

def display_result():
    print(f"\nLa meilleure combinaison d'actions est : \n")
    sum_profits = 0
    investment = 0
    i = 0
    for i in range(len(actions)-1, -1, -1):
        if actions_states[i] == 1:
            print(f"{actions[i].name}")
            investment += actions[i].price
            sum_profits += actions[i].profit_amount
        i -= 1
    print(f"\npour un profit maximum  de {round(sum_profits,2)} et un investissement de {round(investment,2)}.\n")

def main():
    global actions, actions_states
    fill_actions_list()
    actions = merge_sort(actions)
    actions_states = [ 1 for i in range(1,len(actions)+1) if i]

    root_node = Node(calculate_ubv_value(), 0, 0, 0, 0, None)
    expand_tree(root_node)

    display_result()


if __name__ == "__main__":
    main()

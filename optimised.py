"""Optimised algorithm."""


import csv

ACTIONS_LIST_FILE = "ActionsList.csv"
MAX_INVESTMENT = 500

actions, combination = [], []


class Action:
    """Actions class"""

    def __init__(self, name, price, percentage_profit) -> None:
        self.name = name
        self.price = price
        self.percentage_profit = percentage_profit
        self.profit_amount = round(price*(percentage_profit/100),2)
    
    def __str__(self):
        return f"{self.name} / {self.percentage_profit} % / {self.price} € / {round(self.profit_amount,2)} €"


class Node:
    """Nodes class"""

    def __init__(self, current_profit, current_investment, current_upper_bound) -> None:
        self.current_profit = current_profit
        self.current_investment = current_investment
        self.current_upper_bound = current_upper_bound
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,new_node):
        self.leftChild = new_node
    
    def insertRight(self,new_node):
        self.rightChild = new_node
    
    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    """def setRootVal(self,obj):
        self = obj

    def getRootVal(self):
        return self"""


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

def calculate_upper_bound_value(actions_states):
    cumulative_profit = 0
    cumulative_investment = 0
    print(f"\nEtat des actions : {actions_states}")
    i = 0
    for i in range(len(actions)-1, -1, -1):
        if actions_states[i] == 1:
            if cumulative_investment > MAX_INVESTMENT:
                cumulative_investment -= actions[i+1].price
                # Split up the amount profit of the last reviewed action to achieve the exact MAX_INVESTMENT amount
                cumulative_profit += (actions[i+1].profit_amount/actions[i+1].price)*(MAX_INVESTMENT-cumulative_investment)
                print(f"Dernière action : {actions[i+1].name}")
                print(f"Cunulative investment / profit : {round(cumulative_investment,2)} / {round(cumulative_profit,2)}")
                return round(cumulative_profit,2)
            else:
                cumulative_investment += actions[i].price
                cumulative_profit += actions[i].profit_amount
        i -= 1
    print(f"Dernière action : {actions[0].name}")
    print(f"Cunulative investment / profit : {round(cumulative_investment,2)} / {round(cumulative_profit,2)}")
    return round(cumulative_profit,2)

def expand_tree(parent_node, bis_actions, actions_states):
    global combination
    if len(bis_actions) == 0:
        return None
    right_node = Node(parent_node.current_profit,
                      parent_node.current_investment,
                      calculate_upper_bound_value(actions_states))
    parent_node.insertRight(right_node)
    expand_left_tree = False
    if parent_node.current_investment+bis_actions[-1].price <= MAX_INVESTMENT:
        left_node = Node(parent_node.current_profit+bis_actions[-1].profit_amount,
                        parent_node.current_investment+bis_actions[-1].price,
                        parent_node.current_upper_bound)
        parent_node.insertLeft(left_node)
        if left_node.current_upper_bound >= right_node.current_upper_bound:
            expand_left_tree = True
            combination.append(bis_actions.pop())
            expand_tree(left_node, bis_actions, actions_states)
    if not expand_left_tree:
        bis_actions.pop()
        actions_states[len(bis_actions)-len(actions)] = 0
        expand_tree(right_node, bis_actions, actions_states)

def display_result():
    for action in actions:
        print(action)
    print(f"\nLa meilleure combinaison d'actions est : \n")
    investment, profit = 0, 0
    for action in combination:
        print(action.name)
        investment += action.price
        profit += action.profit_amount
    print(f"\npour un profit maximum  de {round(profit,2)} et un investissement de {round(investment,2)}.\n")

def main():
    global actions
    fill_actions_list()
    actions = merge_sort(actions)
    bis_actions = actions.copy()
    actions_states = [ 1 for i in range(1,len(actions)+1) if i]

    root_node = Node(0, 0, calculate_upper_bound_value(actions_states))
    expand_tree(root_node, bis_actions, actions_states)

    display_result()


if __name__ == "__main__":
    main()

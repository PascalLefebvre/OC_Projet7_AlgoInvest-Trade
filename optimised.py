"""Optimised algorithm, based on the resolution of the known "Knapsack problem", using a backtracking process in an
   ordered binary tree. The binary tree is built by treating the most profitable shares first. The research of the
   optimal solution is based on the calculation of an upper bound value (UBV) for each tree node. In our case, it
   corresponds to a cumulative profit value of a given combination of shares for a theoretical limit equal to the
   maximum investment. Thus, an share can be split up (in theory but not in reality ! ) to achieve the exact
   investment capacity ("knapsack capacity"). Therefore, the binary tree is built to expand itself from the node
   with the max UBV within the constraint (maximum investment allowed). Each level of the tree corresponds to the
   processing of a new share and the depth tree is equal to the total number of shares."""


import csv, sys

DEFAULT_PATH = "data/"
DEFAULT_SHARES_FILE = "shares_list.csv"
shares, shares_states = [], []
right_leaf_nodes = []
max_investment = 0


class Share:
    """shares class"""

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
        self.ubv = ubv # Calculated Upper Bound Value
        self.sum_profits = sum_profits
        self.sum_prices = sum_prices
        self.depth = depth # The depth (or level) of the tree node
        self.state = state # 1 if the share is retained (put in the knapsack), 0 otherwise
        self.parent = parent_node # Link to the parent node
        self.leftChild = None # Link to the left child (the share is retained)
        self.rightChild = None # Link to the right child (the share is not retained)

    def insertLeft(self,new_node):
        self.leftChild = new_node
    
    def insertRight(self,new_node):
        self.rightChild = new_node


def fill_shares_list():
    """Load the "shares" list, from the CSV file, after checking data."""

    shares_file = DEFAULT_PATH +\
                  str(input(f"\nEntrez le nom du fichier contenant les actions (\"{DEFAULT_SHARES_FILE}\" par défaut): ")
                  or DEFAULT_SHARES_FILE)
    with open(shares_file) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        i = 0
        j = 0
        for line in reader:
            share_name = line['name']
            share_price = line['price']
            share_profit = line['profit']
            if share_name and share_price and share_profit:
                try:
                    share_price = float(share_price)
                    share_profit = float(share_profit)
                    if share_price > 0 and share_profit > 0:
                        shares.append(Share(share_name, share_price, share_profit))
                        i += 1
                except ValueError:
                    continue
            j += 1
    print(f"\nNombre d'actions valides : {i} sur {j}")

def merge_sort(list):
    """Sort list by increasing order (from DigitalOcean web site)."""

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
    """Calculate the upper bound value of a set of shares."""

    sum_profits = 0
    investment = 0
    # The most profitable share, located at the end of the list, are treated first.
    for i in range(len(shares)-1, -1, -1):
        if shares_states[i] == 1:
            investment += shares[i].price
            sum_profits += shares[i].profit_amount
            if investment > max_investment:
                # Substract and split up the amount profit of the last retained share to achieve the max investment.
                investment -= shares[i].price
                sum_profits -= shares[i].profit_amount
                # A rule ot three is performed to calculate the UBV corresponding to the exact max_investment amount.
                sum_profits += (shares[i].profit_amount/shares[i].price)*(max_investment-investment)
                return sum_profits
    return sum_profits

def update_shares_states(node):
    """Update the "shares_states" list by following the path from the current node to the root node."""

    while node.parent != None:
        shares_states[len(shares)-node.depth] = node.state
        node = node.parent
    return shares_states

def expand_tree(parent_node):
    """Expand the binary tree by creating a maximum of two child nodes."""

    global shares_states, right_leaf_nodes 
    # The base case
    if parent_node.depth == len(shares):
        shares_states = update_shares_states(parent_node)
        return None
    # "index" targets the position of the next share processed in the "shares_states" list.
    index = len(shares)-parent_node.depth-1
    # The right node corresponds to the choice not to retain the share. 
    shares_states[index] = 0
    # A new UBV must be calculated because, by default, the share is retained.
    right_node = Node(calculate_ubv_value(), parent_node.sum_profits, parent_node.sum_prices,
                      parent_node.depth+1, 0, parent_node)
    # After the calculation of the UBV, the "shares_states" list must be restored to its previous values.
    shares_states[index] = 1
    parent_node.insertRight(right_node)
    shares_states = update_shares_states(parent_node)
    if parent_node.sum_prices+shares[index].price <= max_investment:
        # The share is retained thus the left node is created.
        left_node = Node(parent_node.ubv, parent_node.sum_profits+shares[index].profit_amount,
                            parent_node.sum_prices+shares[index].price, parent_node.depth+1, 1, parent_node)
        parent_node.insertLeft(left_node)
        # Save the case where the share is not retained for possible later processing.
        right_leaf_nodes.append((right_node))
        # Sort the right nodes list in order of increasing UBV.
        if len(right_leaf_nodes) >= 2:
            if right_node.ubv < right_leaf_nodes[-2].ubv:
                right_leaf_nodes = sorted(right_leaf_nodes, key=lambda node: node.ubv)
        expand_tree(left_node)
    else:
        right_leaf_nodes.append((right_node))
        # Sort the right nodes list in order of increasing UBV.
        if len(right_leaf_nodes) >= 2:
            if right_node.ubv < right_leaf_nodes[-2].ubv:
                right_leaf_nodes = sorted(right_leaf_nodes, key=lambda node: node.ubv)
        # Expand the tree from the right leaf node with the best UBV.
        expand_tree(right_leaf_nodes.pop())

def display_result():
    """Display the optimal solution."""

    print(f"\nLa meilleure combinaison d'actions est : \n")
    sum_profits = 0
    investment = 0
    i = 0
    for i in range(len(shares)-1, -1, -1):
        if shares_states[i] == 1:
            print(shares[i])
            investment += shares[i].price
            sum_profits += shares[i].profit_amount
        i -= 1
    print(f"\npour un profit maximum  de {round(sum_profits,2)} et un investissement de {round(investment,2)}.\n")

def main():
    global shares, shares_states, max_investment

    # The default limit of 1000 recursions must be extended to process Sienna's data.
    sys.setrecursionlimit(3750)
    print(f"\nMax recursion : {sys.getrecursionlimit()}")

    max_investment = float(input("\nEntrer l'investissement maximum autorisé (500 € par défaut): ") or "500")

    fill_shares_list()
    shares = merge_sort(shares)
    # By default, shares are retained.
    shares_states = [ 1 for i in range(1,len(shares)+1) if i]

    root_node = Node(calculate_ubv_value(), 0, 0, 0, 0, None)
    expand_tree(root_node)

    # 1 = retained, 0 = not retained
    print(f"\nEtat des actions : \n{shares_states}\n")

    display_result()


if __name__ == "__main__":
    main()

from tree import *

def height(t , i):
    i += 1 
    if is_leaf(t):
        return i
    else:
        store = [height(x,i) for x in branches(t)]
    return max(store)

def max_path_sum(t , i):
    i += label(t)
    if is_leaf(t):
        return i
    else:
        store = [max_path_sum(x , i) for x in branches(t)]
    return max(store)

def square_tree(t):
    if is_leaf(t):
        return tree(label(t)**2)
    elif is_tree(t):
        store = [square_tree(x) for x in branches(t)]
        return tree(label(t)**2 , store)

def find_path(tree , x):
    if is_leaf(tree):
        return [label(tree)]
    else:
        for y in branches(tree):
            paths = [[label(tree)] + find_path(y , x)]
        



t = tree(2, [tree(7, [tree(3), tree(6, [tree(5), tree(11)])] ), tree(15)])

print(find_path(t , 5))

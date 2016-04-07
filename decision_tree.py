#!/usr/bin/python
# Vuong V. Bui (C) April 7th 2016

from collections import defaultdict
from math import log

def entropy(probabilities):
    return sum([- p * log(p) for p in probabilities])

def id3(instances, attrs, goal_attr):
    classes = [instance[goal_attr] for instance in instances]
        
    if (not attrs) or (classes.count(classes[0]) == len(classes)):
        return max(set(classes), key=classes.count)

    entropies = {}
    for attr in attrs:
        count = defaultdict(lambda: defaultdict(int))
        total = defaultdict(int)
        
        for instance in instances:
            count[instance[attr]][instance[goal_attr]] += 1
            total[instance[attr]] += 1
        entropies[attr] = sum([total[value] * entropy([float(c) / total[value]
                                                              for c in count[value].values()])
                                      for value in count.keys()])

    best_attr = min(entropies.keys(), key=entropies.get)
    partition = defaultdict(list)
    for instance in instances:
        partition[instance[best_attr]].append(instance)

    subtrees = {}
    attrs.remove(best_attr)
    for value in partition.keys():
        subtrees[value] = id3(partition[value], attrs, goal_attr)
    return best_attr, subtrees

def pretty_print(tree, level=0):
    margin = "  " * level
    if (isinstance(tree, tuple)):
        print margin + "[" + tree[0] + "]"
        for value, subtree in tree[1].items():
            print margin + "+, " + value
            pretty_print(subtree, level+1)
    else:
        print margin + "--->" + tree
            
if __name__ == "__main__":
    attributes = "outlook temperature humidity wind play.tennis?".split()
    goal_attribute = "play.tennis?"

    data = [d.split() for d in 
            ["sunny hot high weak no",
             "sunny hot high strong no",
             "overcast hot high weak yes",
             "rain mild high weak yes",
             "rain cool normal weak yes",
             "rain cool normal strong no",
             "overcast cool normal strong yes",
             "sunny mild high weak no",
             "sunny cool normal weak yes",
             "rain mild normal weak yes",
             "sunny mild normal strong yes",
             "overcast mild high strong yes",
             "overcast hot normal weak yes",
             "rain mild high strong no"]]

    training_data = []
    for d in data:
        instance = {}
        for attr, val in zip(attributes, d):
            instance[attr] = val
        training_data.append(instance)
        print instance

    features = set(attributes)
    features.remove(goal_attribute)
    tree = id3(training_data, features, goal_attribute)
    pretty_print(tree)

from typing import NamedTuple
from collections import defaultdict, Counter
import math

# Code print(Counter('abracadabra').most_common(3))
# Output [('a', 5), ('b', 2), ('r', 2)]

def data_entropy(labels):
    # Compute the class probabilities
    # Counter(labels).values() stores the value (False/Negative) as dict key and the count as dict value
    total_count = len(labels)
    class_probabilities = []
    for count in Counter(labels).values():
        class_probabilities.append(count / total_count)
    
    # Given a list of class probabilities, compute the entropy
    entropy = sum(-p * math.log(p, 2) for p in class_probabilities if p > 0)
    return entropy

def partition_entropy(subsets):
    # Returns the entropy from this partition of data into subsets
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count for subset in subsets)


def partition_by(inputs, attribute):
    # Partitions the inputs into two dictionary lists,
    # one set containing the individuals with the attribute as False
    # and one containing the individuals with the attribute as True
    partitions = defaultdict(list)
    # For each Individual in out inputs list
    for input in inputs:
        # get the value of the attribute for this Individual
        attribute_value = getattr(input, attribute)
        # Append the input to the partitions list based on the attribute value
        partitions[attribute_value].append(input)

    # The key of this partitions dict is True or False,
    # i.e. the True set contains all individuals whose attribute is True
    return partitions

def partition_entropy_by(inputs, attribute, label_attribute):
    # Calculates the entropy of a given partition
    # First, partition the inputs by the attribute we want to calculate entropy for
    partitions = partition_by(inputs, attribute)
    labels = []
    # partitions.values() gets the set of individuals corresponding to the True/False dict keys
    # For each partition in the partitions dict,
    for i, partition in enumerate(partitions.values()):
        labels.append([])
        # For each Individual in this partition,
        for input in partition:
            # append the value of label_attribute for this Individual to the labels list at the same partition index
            labels[i].append(getattr(input, label_attribute))
    # Return the entropy value for the partition
    return partition_entropy(labels)

class Leaf(NamedTuple):
    # A Leaf is a prediction, i.e. Did Run or Didn’t Run
    value: None

class Split(NamedTuple):
    # A Split contains an attribute to split on,
    # the subtrees for specific values of that attribute,
    # and a default value if we see and unknown value
    attribute: str
    subtrees: dict
    default_value: None

def classify(tree, input):
    # Classify the input using the given decision tree
    # If this is a leaf node, return its value loop is done
    if isinstance(tree, Leaf):
        return tree.value
    
    # Otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and whose values are subtrees to consider next
    subtree_key = getattr(input, tree.attribute)
    if subtree_key not in tree.subtrees: # If no subtree for key,
        return tree.default_value # return the default value.
    subtree = tree.subtrees[subtree_key] # Choose the appropriate subtree
    return classify(subtree, input) # and use it to classify the input.

def build_tree(inputs, split_attributes, target_attribute):
    # Count target labels, these are stores in label_counts under the value key
    # (i.e. True or False)
    label_counts = Counter(getattr(input, target_attribute)
                    for input in inputs)
    # Find most common label
    # most_common(number of values to return; i.e. most common 1 or 3 etc.)

    most_common_label = label_counts.most_common(1)[0][0]
    # If there is only one label in label_counts,
    # this ends the loop and we return the prediction
    if len(label_counts) == 1:
        return Leaf(most_common_label)
    
    # If there are no more splits available in our decision tree,
    # We return the prediction for the majority label
    if not split_attributes:
        return Leaf(most_common_label)
    
    # Otherwise we split by the best attribute

    def split_entropy(attribute):
        # Helper function for finding the best attribute
        return partition_entropy_by(inputs, attribute, target_attribute)
    
    # Find the best_attribute to split by; i.e. the attribute with the lowest entropy
    # This "min" function will return the minimum attribute in the split_attributes list
    # based on the return value of split_entropy for each attribute.
    best_attribute = min(split_attributes, key=split_entropy)
    # Partition based on the best_attribute
    partitions = partition_by(inputs, best_attribute)
    
    # Create a new list of attributes to pass through in the recursive call
    # (removing the best_attribute we just split on)
    new_attributes = [a for a in split_attributes if a != best_attribute]
    
    # Create the subtrees for this split
    # Subtrees are stored using the attribute_value as the key in the subtrees dict
    # The subtree stored under each key is created by recursively calling this same function,
    # passing the subset of input values stored in each partition of our partitions set from above.
    subtrees = {attribute_value: build_tree(subset, new_attributes,
    target_attribute)
        for attribute_value, subset in partitions.items()}

    # For each recursive call of this function, we continue down the tree until we hit a leaf node
    # at which point one of the previous return conditions are met and a leaf prediction is returned.
    # Once the recursive call to populate subtrees above is completed, we return the parent split of these subtrees.
    return Split(best_attribute, subtrees, default_value=most_common_label)

if __name__ == "__main__":
    # Named tuples assign a name to each position in a tuple.
    # They allow the ability to access fields by this name instead of positionindex.
    class Individual(NamedTuple):
        outlook: str
        temp: str
        humidity: str
        wind: str
        did_run: bool = None
        # We allow "None" here, for when we are predicting this based on the other inputs.
    
    # Inputs using the Individual class for easy referencing
    #                   outlook      temp   humidity    wind    did_run
    inputs = [Individual('Sunny',    'Hot',  'High',   'Weak',   False),
              Individual('Sunny',    'Hot',  'High',   'Strong', False),
              Individual('Overcast', 'Hot',  'High',   'Weak',   True),
              Individual('Rain',     'Mild', 'High',   'Weak',   True),
              Individual('Rain',     'Cool', 'Normal', 'Weak',   True),
              Individual('Rain',     'Cool', 'Normal', 'Strong', False),
              Individual('Overcast', 'Cool', 'Normal', 'Strong', True),
              Individual('Sunny',    'Mild', 'High',   'Weak',   False),
              Individual('Sunny',    'Cool', 'Normal', 'Weak',   True),
              Individual('Rain',     'Mild', 'Normal', 'Weak',   True),
              Individual('Sunny',    'Mild', 'Normal', 'Strong', True),
              Individual('Overcast', 'Mild', 'High',   'Strong', True),        
              Individual('Overcast', 'Hot',  'Normal', 'Weak',   True),
              Individual('Rain',     'Mild', 'High',   'Strong', False)
    ]
    # Generate the decision tree based on our inputs data.
    # We pass did_run as our target, this is what we want to predict.
    target_attribute = 'did_run'
    attributes = ['outlook', 'temp', 'humidity', 'wind']
    tree = build_tree(inputs, attributes, target_attribute)
    
    # Test the tree on new data.
    # This should predict True,
    print(classify(tree, Individual("Sunny", "Mild", "Normal", "Weak")))
    # and this should predict False.
    print(classify(tree, Individual("Rain", "Cold", "High", "Strong")))

    print(classify(tree, Individual("Sunny", "Cold", "Normal", "Strong")))


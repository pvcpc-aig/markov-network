"""
Using the generated Markov table from `gengraph.py`, this script will
load in the table and generate phrases with some given conditions.
"""
import os
import sys
import random


# The path to the generated markov table.
MARKOV_TABLE = "data/allthenews/markov"

# An 8MB read buffer size.
READ_BUFFER = 2 ** 23


def load_table(path):
    """
    Loads in a Markov table from the specified path. The specification
    for the table can be found in `gengraph.py`.

    The table returned contains a list of tuples in the form:

        (<Token>, <Links>, <Weights>)
    
    where <Token> is the actual textual token or value for the markov
    chain node. The <Links> is a list of indices demonstrating forward
    connections to other nodes in the table. The <Weights> is a list of
    probabilities corresponding with the links.
    """
    table = []
    with open(path, mode="r", buffering=READ_BUFFER) as fin:
        for entry in fin:
            info = entry.split()
            token = info[0]
            links = []
            weights = []
            for i in range(1, len(info) - 1, 2):
                links.append(int(info[i]))
                weights.append(float(info[i + 1]))
            table.append((token, links, weights))
    return table


def weighted_choice(sequence, weights):
    if len(sequence) != len(weights):
        raise ValueError("len(sequence) must equal len(weights)")
    if len(sequence) == 0:
        return None
    target = random.random()
    cumulative = 0
    for i, pair in enumerate(zip(sequence, weights)):
        item, weight = pair
        cumulative += weight
        if cumulative > target:
            return item
    return sequence[-1]


def generate_phrase(table, delim='.', maxtokens=256):
    phrase = []
    # Pick an initial token that is not the delimiter.
    token = None
    while token is None or token[0] == delim:
        token = random.choice(table)
    count = 0
    while count < maxtokens:
        phrase.append(token[0])
        _, links, weights = token
        if token[0].endswith(delim) or len(links) == 0:
            break
        token = table[weighted_choice(token[1], token[2])]
        count += 1
    return ' '.join(phrase)


if __name__ == "__main__":
    print("Loading Markov table...")
    table = load_table(MARKOV_TABLE)

    print("Generating phrases...")
    for i in range(100):
        print(f"{i}. {generate_phrase(table)}")
#!/usr/bin/env python
# coding: utf-8
"""
Author: Ameet Khedkar
Email: amtkhdkr@gmail.com
This code was written as part of the take home assignment for
the position of DevOps Engineer (TEC0788) at Kindred plc, Stockholm
"""
from argparse import ArgumentParser
import re
import os
import pprint
from collections import deque

class WhereAreMyKeys(object):

    def __init__(self):
        """
            Initialize commonly required data for all functions
        """
        # If there are no weights defined, assign a default
        # constant value to each
        self.CONSTANT_EFFORT = 1
        # Defines the smallest effort value for accessing
        # a node. For example, this is used here to map the node
        # and the item which is contained in that node.
        self.SMALLEST_EFFORT = 0
        # The graph's keys contain every node for the key
        # Every neighbour of the node is added to a
        # dictionary of the desintation: effort/cost
        # This makes for translating: A-> B=10 to self.graph[A][B] = 10
        self.graph = dict()
        # Initialize the weights to a None object, later we will
        # assign it to a dictionary where the A->B=10 goes in self.weights[A][B]=10
        self.weights = None
        # From the given input.config, we need to parse out the edges using RE
        # An edge can be of multiple items separated by colons
        # and an item at the end. The current implementation stores all parts
        # and the item itself in respectively new nodes.
        self.edge_expr = re.compile('(\w+)')
        # Optionally, there may be a weight assigned for every edge
        # This should be of the format House->Bathroom=10 with optional whitespaces
        # The expression below can capture each of them
        self.weights_expr = re.compile(r'\s*(\w+)\s*->\s*(\w+)\s*=\s*(\d+)')
        # call the function which captures weights from the given weights.config
        self.construct_weights()
        # using the above weights, capture the edges and create the graph
        self.construct_graph()

    def construct_weights(self):
        """
            Initialize the weights configuration if provided
        """
        if os.path.exists('weights.config'):
            with open('weights.config') as f:
                self.weights = dict()
                for line in f:
                    results = self.weights_expr.findall(line)
                    # the expression should match and the results should all be of length 3 (src, des, wt)
                    if not results or not all(len(items) == 3 for items in results):
                        raise ValueError(f'Invalid weight config line: {line.strip()}'
                                         '. Expected format source -> destination = weight')
                    source, destination, value = results[0]
                    # add an entry from source to destination with the weight value
                    try:
                        self.weights[source].update({destination: int(value)})
                    except KeyError:
                        self.weights[source] = {destination: int(value)}

    def lookup_weight(self, source, destination):
        """
            Lookup the cost of moving from source to destination.
            Returns the default value if there were no costs defined
        """
        if self.weights is None:
            # In case of no weights defined, return an equal weight for all
            value = self.CONSTANT_EFFORT
        else:
            # Some weights were defined! Let us try to lookup and return them
            try:
                value = self.weights[source][destination]
            except KeyError:
                raise ValueError(f'There was no weight defined for the path {source} -> {destination}')
        return value


    def construct_graph(self):
        """
            Construct nested dictionaries for each destination along with weights
        """
        with open('input.config') as f:
            for line in f:
                results = self.edge_expr.findall(line)
                if len(results) < 1:
                    raise ValueError(f'Invalid input config line: {line.strip()}'
                                    '. Expected format [\w:]')
                for i in range(len(results)):
                    if i < len(results) - 2 :
                        source, destination = results[i], results[i+1]
                        weight = self.lookup_weight(source, destination)
                        if source in self.graph:
                            self.graph[source].update({destination: weight})
                        else:
                            self.graph[source] = {destination: weight}
                    elif i == len(results) - 2:
                        self.graph[results[i]] = {results[i+1]: self.SMALLEST_EFFORT}

    def shortest_path_from(self, source, destination):
        """
            Implement Edgar Djikstra's shortest path algorithm.
            https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        # start with initial source
        current = source
        shortest_paths = {source: (None, 0)}
        visited = set()

        while current != destination:
            visited.add(current)
            destinations = list(self.graph[current].keys()) if current in self.graph else []
            effort_to_current = shortest_paths[current][-1]

            for destination in destinations:
                effort = self.graph[current][destination] + effort_to_current
                if destination not in shortest_paths:
                    shortest_paths[destination] = (current, effort)
                else:
                    if shortest_paths[destination][-1] > effort:
                        shortest_paths[destination] = (current, effort)
            next_destinations = {
                node: shortest_paths[node]
                for node in shortest_paths if node not in visited
            }
            if not next_destinations:
                # there is nothing to go further, route impossible
                return False
            current = min(
                next_destinations,
                key= lambda some_k: next_destinations[some_k][-1]
            )
        path = []
        while current is not None:
            path.insert(0, current)
            next_node = shortest_paths[current][0]
            current = next_node
        return path

if __name__=='__main__':
    parser = ArgumentParser(usage="A script which, given a current location and "
    "one object, will tell you the shortest path from the"
    " start location to the object.")
    parser.add_argument('source', help='Any location (eg Estate, Hall, etc) from input.config')
    parser.add_argument('item', help='Any item (eg keys, knife) from input.config')
    assignment = WhereAreMyKeys()
    args = parser.parse_args()
    source = args.source
    item = args.item
    try:
        current_location, *intermediate, item = assignment.shortest_path_from(source, item)
    except:
        print(f'There is no path possible from {source} to {item}')
        # Exit with failure
        exit(1)
    else:
        result = f'You are in the {current_location}. '
        if intermediate:
            result += 'Go to the ' + ". Go to the ".join(intermediate) + ". "
        result += f'Collect your {item}.'
        print(result)
        # Exit with success
        exit(0)

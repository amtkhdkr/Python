#!/usr/bin/env python
# coding: utf-8

# In[134]:


import re
import os
import pprint
from collections import deque

class WhereAreMyKeys(object):
    
    def __init__(self):
        """
            Initialize commonly required data for all functions
        """
        self.CONSTANT_EFFORT = 1
        self.SMALLEST_EFFORT = 0
        self.graph = dict()
        self.weights = None
        self.edge_expr = re.compile('(\w+)')
        self.weights_expr = re.compile(r'\s*(\w+)\s*->\s*(\w+)\s*=\s*(\d+)')
        self.construct_weights()
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
            Implement Djikstra's shortest path algorithm.
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
                
assignment = WhereAreMyKeys()
source = 'Stairs'
item = 'pillow'
try:
    current_location, *intermediate, item = assignment.shortest_path_from(source, item)
except:
    print(f'There is no path possible from {source} to {item}')
else:
    result = f'You are in the {current_location}. '
    if intermediate:
        result += 'Go to the ' + ". Go to the ".join(intermediate) + ". "
    result += f'Collect {item}. Done'
    print(result)


# In[ ]:





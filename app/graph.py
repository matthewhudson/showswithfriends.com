
import app

from flask import url_for

def make_mapping():
    filepath = 'app/static/map.csv'
    mapping = {}
    with open(filepath, 'r') as f:
        for line in f:
            compressed, sg = line.split(',')
            if sg is None:
                sg = 0
            try:
                mapping[int(compressed)] = int(sg)
            except:
                pass
    return mapping

def make_graph(mapping=None):
    filepath = 'app/static/graph.net'
    graph = []
    if mapping is None:
        mapping = make_mapping()
    with open(filepath, 'r') as f:
        for line in f:
            if line[0] == '*':
                continue
            try:
                source, target, weight = line.split(' ')
            except:
                break
            graph.append((int(source), int(target), float(weight)))
    return graph
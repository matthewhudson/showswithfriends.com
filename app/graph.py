
import app

from flask import url_for
from sglib.common import tryInt, tryFloat

def make_mapping():
    filepath = 'app/static/map.csv'
    mapping = {}
    with open(filepath, 'r') as f:
        for line in f:
            compressed, sg, recon = line.split(',')
            mapping[compressed] = tryInt(sg)
    return mapping

def make_graph():
    filepath = 'app/static/graph.net'
    graph = []
    mapping = make_mapping()
    with open(filepath, 'r') as f:
        for line in f:
            if line[0] == '*':
                continue
            try:
                source, target, weight = line.split(' ')
            except:
                break
            graph.append((tryInt(source), tryInt(target), tryFloat(weight)))
    return graph


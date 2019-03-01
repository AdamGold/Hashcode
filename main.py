import sys
import itertools
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt


def getTags(item):
    if isinstance(item, tuple):
        return set(allPhotos[item[0]] + allPhotos[item[1]])
    return set(allPhotos[item])


visited = []


def move_to_node(node):
    if node in visited:
        return
    print(f"{node} ->")
    edges = list(G.edges(node, data=True))
    visited.append(node)
    move_to_node(edges[0][1])


if __name__ == "__main__":
    G = nx.Graph()
    allPhotos = {}
    horizontal = []
    verticals = []
    with open(sys.argv[1], "r") as f:
        for index, line in enumerate(f):
            direction = line[0]
            line = line[:-1]
            allPhotos[index - 1] = line[line.find(" ", 2) + 1 :].split(" ")
            if direction == "H":
                horizontal.append(index - 1)
            elif direction == "V":
                verticals.append(index - 1)

    verticalCombinations = list(itertools.combinations(verticals, r=2))

    connections = horizontal + verticalCombinations
    for item in connections:
        tags = getTags(item)
        G.add_node(item)
        for other_item in connections:
            if item == other_item:
                continue
            other_tags = getTags(other_item)
            inters = tags.intersection(other_tags)
            math = min(
                len(inters),
                min((len(other_tags) - len(inters)), len(tags) - len(inters)),
            )
            G.add_edge(item, other_item, weight=math)

    for node in G.nodes():
        move_to_node(node)
    # print(nx.max_weight_matching(G))
    # print(nx.algorithms.shortest_paths.weighted.dijkstra_path(G, 0, (1, 2)))
    # nx.draw(G, with_labels=True, font_weight="bold")
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_edge_labels(G, pos=pos)
    # plt.show()

    # final[item] = math


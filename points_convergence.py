import networkx as nx 
import random 
import numpy as np
from pprint import pprint 

def add_edges(G,p):
    for i in G.nodes():
        for j in G.nodes():
            if i!=j and G.has_edge(i,j)==0:
                r = random.random()
                if r<=p:
                    G.add_edge(i,j)
    return G

def initialize_points(G):
    points = [100 for i in range(G.number_of_nodes())]
    return points

def distribute_point(G, points):
    prev_points = points
    new_points = [0 for i in range(G.number_of_nodes())]

    for i in G.nodes():
        out = G.out_edges(i)
        if len(out)==0:
            new_points[i] += prev_points[i]
        else:
            share = (float)(prev_points[i])/len(out)
            for each in out:
                new_points[each[1]] += share

    return G, new_points

def handle_points_sink(G,points):
    n = G.number_of_nodes()
    extra = 20 # 20% of total node to be divided and shared to all nodes uniformly
    for i in range(len(points)):
        points[i] = (float)(points[i])*0.8
        points[i] += 20
    return points

def keep_distributing_points(G,points):
    prev_points = points
    for i in range(1000):
        G , new_points = distribute_point(G,prev_points)
        new_points = handle_points_sink(G,new_points)
        prev_points = new_points

    print(new_points)
    return G, new_points

def get_nodes_sorted_by_points(points):
    points_array = np.array(points)
    nodes_sorted_by_points=np.argsort(-points_array)
    return nodes_sorted_by_points

def main():
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(10)])
    G = add_edges(G,0.3)

    # Assign 100 points to each node
    points = initialize_points(G)
    G, points = keep_distributing_points(G,points)
    nodes_sorted_by_points = get_nodes_sorted_by_points(points)
    pprint(nodes_sorted_by_points)
    pr = nx.pagerank(G)
    pr_sorted = sorted(pr.items(), key = lambda x:x[1] , reverse=True)
    for i in pr_sorted:
        print(i[0], end=" ")
main()
print()
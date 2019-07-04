import networkx as nx 
import random
import numpy as np 

def add_edges(G,p):
    for i in G.nodes():
        for j in G.nodes():
            if i!=j and G.has_edge(i,j)==0:
                r = random.random()
                if r<=p:
                    G.add_edge(i,j)
    return G

def get_nodes_sorted_by_RW(points):
    points_array = np.array(points)
    nodes_sorted_by_RW=np.argsort(-points_array)
    return nodes_sorted_by_RW

def random_walk(G):
    nodes= list(G.nodes())
    RW_points = [0 for i in range(G.number_of_nodes())]
    r = random.choice(nodes)
    RW_points[r] += 1
    out = list(G.out_edges(r))

    c = 0
    while(c!= 10000):
        if len(out)==0:
            focus = random.choice(nodes)
        else:
            r1 = random.choice(out)
            focus = r1[1]
        RW_points[focus] += 1
        out = list(G.out_edges(focus))
        c += 1
    return RW_points

def main():
    # Create a directed graph
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(10)])
    G = add_edges(G,0.3)
    
    RW_points = random_walk(G)
    
    nodes_sorted_by_RW = get_nodes_sorted_by_RW(RW_points)
    print("Page rank by the local function:        ",nodes_sorted_by_RW)

    pr = nx.pagerank(G)
    pr_sorted = sorted(pr.items(), key = lambda x:x[1] , reverse=True)
    print("Page rank by networkx.pagerank function: [", end= "")
    for i in pr_sorted:
        print(i[0], end=" ")
main()
print("]")
    


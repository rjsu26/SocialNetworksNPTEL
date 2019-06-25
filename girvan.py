import networkx as nx 
import matplotlib.pyplot as plt 
import intro2

def edge_to_remove(G):
    dict1 = nx.edge_betweenness_centrality(G) #gives the betweenness of all edgess
    # Betweenness is the value showing for each edge, how many shortest paths between any 2 nodes, does it lies.
    list_of_tuples = list(dict1.items())
    list_of_tuples.sort(key = lambda x:x[1] , reverse =True) #Method to sort a dictionary on the basis of 2nd value of the tuple in decreasing order.
    return  list_of_tuples[0][0] #(a,b)
    
def girvan(G):
    c = nx.connected_component_subgraphs(G) #Gives a graph object(generator object in new networkx version)
    l = len(list(c))
    print("The number of connected components are:",l)
    while(l==1):
        edge_removed =edge_to_remove(G) 
        print("The edge removed is:",edge_removed)
        G.remove_edge(*edge_removed)  #((a,b)) -> (a,b)
        c = nx.connected_component_subgraphs(G)
        l = len(c)
        print("The number of connected components are:",l)
    return c

# G = intro2.create_network((15))
# c = girvan(G)
# # print(c)
# # nx.draw(c)
# # plt.show()

# for i in c:
#     print(i.nodes())
#     print ("-----------------------------")
# for item in girvan(G):
#     print(item)

G = nx.karate_club_graph()
c = girvan(G)
for i in c:
    print(i.nodes())
    print ("-----------------------------")


import networkx as nx 
import matplotlib.pyplot as plt
import random

def create_network(num_edges):
    if num_edges>36:
        print("Please enter number of edges less than 70")
    else:
        city_set=['Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai' ,'Kolkata', 'Surat', 'Pune', 'Jaipur']
        costs=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]    
        
        G=nx.Graph()
        for each in city_set:
            G.add_node(each)
        
        while (G.number_of_edges()<num_edges):
            print("Adding edge number:", G.number_of_edges())
            c1=random.choice(list(G.nodes()))
            c2=random.choice(list(G.nodes()))
            if c1!=c2 and G.has_edge(c1,c2)==0 :
                w= random.choice(costs)
                G.add_edge(c1, c2, weight = w)
        
        return G
        # pos = nx.circular_layout(G)
        # nx.draw(G, pos,with_labels=1)
        # plt.show()
        

if __name__ == "__main__":
    G = create_network(20)
    pos = nx.circular_layout(G)
    nx.draw(G, pos,with_labels=1)
    plt.show()
    


# # nx.draw_networkx_edge_labels(G,pos)

# print (nx.is_connected(G))
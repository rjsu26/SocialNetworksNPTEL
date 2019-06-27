import networkx as nx 
import matplotlib.pyplot as plt

def plot_density():
    x = []
    y = []
    for i in range(0,11):
        G=nx.read_gml('evolution_' + str(i) + '.gml') # filename was like : evolution_2.gml
        x.append(i) # x-axis denotes time
        y.append(nx.density(G)) # y-axis denotes density of graph G at that at a time t
    
    plt.xlabel('TIme')
    plt.ylabel("Density")
    plt.title("Change in Density")
    plt.plot(x,y)
    plt.show()

if __name__== '__main__':
    plot_density()
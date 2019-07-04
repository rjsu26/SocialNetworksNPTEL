import networkx as nx   
import matplotlib.pyplot as plt
import random
import itertools
import time 

def get_signs_of_tris(tris_list, G):
    """Function to return the signs(+/-) of each edge of every traingle in list of list form
    Sample output:  [ [+,-,-] , [+,+,+] , [-,+,-] ]"""
    all_signs = []
    for i in range(len(tris_list)):
        tmp = []
        tmp.append(G[tris_list[i][0]][tris_list[i][1]]['sign'])
        tmp.append(G[tris_list[i][2]][tris_list[i][1]]['sign'])
        tmp.append(G[tris_list[i][0]][tris_list[i][2]]['sign'])
        all_signs.append(tmp)
    return all_signs #Output:  [ [+,-,-] , [+,+,+] , [-,+,-] , ...... ]

def count_unstable(all_signs):
    """Takes input of a list of list with sign of each edge and returns total
    number of unstable traingles in the network."""
    stable , unstable = 0 , 0
    for i in range(len(all_signs)):
        if all_signs[i].count('+')==3 or all_signs[i].count('+')==1:
            stable += 1 # "+++" and "-+-" are stable
        elif all_signs[i].count('+')==2 or all_signs[i].count('+')==0:
            unstable += 1 # "+-+" and "+--" are unstable
    # print("Number of unstable nodes out of ", stable+unstable," nodes is ", unstable)
    # print("Number of stable nodes out of ", stable+unstable," nodes is ", stable)

    return unstable

def see_coalitions(G):
    first_coalition=[] 
    second_coalition =  []
    nodes = G.nodes()
    r = random.choice(list(nodes))
    first_coalition.append(r)

    processed_nodes , to_be_processed = [], [r]
    
    for each in to_be_processed:
        if each not in processed_nodes:
            neigh = G.neighbors(each)
            # print(dir(neigh))
            for key in neigh.__iter__():
                if G[each][key]['sign']=='+':
                    if key not in first_coalition:
                        first_coalition.append(key)
                    if key not in to_be_processed:
                        to_be_processed.append(key)
                elif G[each][key]['sign']=='-':
                    if key not in second_coalition:
                        second_coalition.append(key)
                        processed_nodes.append(key)
            
            processed_nodes.append(each)
    return first_coalition, second_coalition

def revert_sign(G,i,j,index):
    """To change the sign of an edge"""
    if G[tris_list[index][i]][tris_list[index][j]]['sign']=='+':
        G[tris_list[index][i]][tris_list[index][j]]['sign']='-'
    elif G[tris_list[index][i]][tris_list[index][j]]['sign']=='-':
        G[tris_list[index][i]][tris_list[index][j]]['sign']='+'

def move_a_tri_to_stable(G, tris_list, all_signs):
    """To make a randomly selected as stable by reverting edge sign"""
    found_unstable = False
    while found_unstable==False:
        index = random.randint(0,len(tris_list)-1)
        if all_signs[index].count('+')==2 or all_signs[index].count('+')==0:
            found_unstable=True
    # To make the unstable triangle a stable one
    r = random.randint(1,3) #Choosing which one sign of the 3 edges to convert
    # In all cases of unstability, reverting sign of any single edge makes it stable
    if all_signs[index].count('+')==2:
        if r==1:
            revert_sign(G,0,1,index)
        elif r==2:
            revert_sign(G,1,2,index)
        elif r==3:
            revert_sign(G,0,2,index)
    elif all_signs[index].count('+')==0:
        if r==1:
            G[tris_list[index][0]][tris_list[index][1]]['sign']='+'
        if r==2:
            G[tris_list[index][2]][tris_list[index][1]]['sign']='+'
        if r==3:
            G[tris_list[index][0]][tris_list[index][2]]['sign']='+'

    return G

def draw_graph(G):
    edge_labels = nx.get_edge_attributes(G, 'sign') # To avoid label as "sign=+" in graph
    pos= nx.circular_layout(G)
    nx.draw(G, pos, node_size=5000, with_labels=True, node_color="red")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels , font_size=20, font_color="red")
    # To make node border as black
    ax= plt.gca()
    ax.collections[0].set_edgecolor("#000000")    
    plt.show()

G = nx.Graph()
n = 8
G.add_nodes_from([i for i in range(1,n+1)])
mapping =  {1:'Alexandria', 2:'Anterim', 3:'Bercy', 4:'Bearland', 5:'Eplex', 6:'Gripa',
                    7:'Ikly', 8:'Jemra', 9:'Lema', 10:'Umesi', 11:'Mexim', 12:'SocialCity', 13:'Tersi',
                    14:'Xopia', 15:'Tamara' }
G = nx.relabel_nodes(G, mapping)

signs = ['+', '-']
for i in G.nodes():
    for j in G.nodes():
        if i!=j and G.has_edge(i,j)==0:
            G.add_edge(i,j,sign=random.choice(signs))

# draw_graph(G) 

nodes = G.nodes()
tris_list= [list(x) for x in itertools.combinations(nodes,3)] # nC3 (combination) gives all possible traingles in the graph
all_signs = get_signs_of_tris(tris_list,G)
unstable = count_unstable(all_signs)
unstable_track = [unstable]
while unstable!=0:
    G = move_a_tri_to_stable(G, tris_list, all_signs)
    all_signs = get_signs_of_tris(tris_list,G)
    unstable = count_unstable(all_signs)
    unstable_track.append(unstable)

first , second = see_coalitions(G)
print(first,second)
# Visualising both the coalitions
pos = nx.circular_layout(G)
edge_labels = nx.get_edge_attributes(G, 'sign') # To avoid label as "sign=+" in graph
nx.draw_networkx_nodes(G,pos,nodelist=first,node_color='red', node_size=5000, alpha=0.8)
nx.draw_networkx_nodes(G,pos,nodelist=second,node_color='yellow', node_size=5000 )
nx.draw_networkx_labels(G,pos, font_size=15)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels, font_color='magenta', font_size=15, font_weight=2)
plt.show()
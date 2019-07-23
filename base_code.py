import networkx as nx 
import matplotlib.pyplot as plt

def set_all_B(G):
    for each in G.nodes():
        G.node[each]['action']='B'

def set_A(G, list1):
    for each in list1:
        G.node[each]['action']= 'A'

def get_colors(G):
    list1=[]
    for each in G.nodes():
        if G.node[each]['action']=='B':
            list1.append('red')
        else:
            list1.append('green')
    return list1

def find_neighbours(node, c, G):
        num = 0
        for each in G.neighbors(node):
                if G.node[each]['action']==c:
                        num += 1
        return num

def recalculate_options(G):
        dict1 = {}
        # Payoff(A)=a=4
        # Payoff(B)=b=3
        a = 6
        b = 4
        for each in G.nodes():
                num_A = find_neighbours(each, 'A', G)
                num_B = find_neighbours(each, 'B', G)
                payoff_A = a*num_A
                payoff_B = b*num_B
                if payoff_A>= payoff_B:
                        dict1[each]='A'
                else:
                        dict1[each]='B'
        return dict1

def reset_node_attributes(G,action_dictionary):
        for each in action_dictionary:
                G.node[each]['action']=action_dictionary[each]

def terminate_1(c,G):
        f=1
        for each in G.nodes():
                if G.node[each]['action']!=c:
                        f = 0
                        break
        return f

def terminate(G, count):
        flag1 = terminate_1('A', G)
        flag2 = terminate_1('B', G)
        if flag1==1 or flag2==1 or count>=100:
                return 1
        else:
                return 0

# G = nx.read_gml('random_graph.gml')
G = nx.erdos_renyi_graph(10,0.5)
set_all_B(G)
list1=[3,7]
set_A(G, list1)
colors = get_colors(G)
nx.draw(G, node_color=colors , node_size=800, with_labels=True)
plt.show()

count = 0
flag = 0
while(1):
        flag = terminate(G, count)
        if flag==1:
                break
        count += 1
        action_dictionary = recalculate_options(G)
        reset_node_attributes(G,action_dictionary)
        colors = get_colors(G)
        nx.draw(G, node_color=colors , node_size=800, with_labels=True)
        plt.show()

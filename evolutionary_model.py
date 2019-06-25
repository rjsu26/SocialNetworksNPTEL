import math
import random
import time
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create a graph of 100 nodes
def create_Graph():
    G = nx.Graph()
    G.add_nodes_from(range(1,101))
    return G

def visualize(G):# visualise G with label dictionary and node size as given 
    time.sleep(2)
    # nx.draw(G, with_labels=1 , node_size=nodesize)
    labeldict = get_labels(G)
    nodesize = get_size(G)
    color_array=get_colors(G)
    nx.draw_networkx(G, labels=labeldict, node_size=nodesize, node_color=color_array, pos=nx.spring_layout(G))
    
    # To add node borders as black
    ax= plt.gca()
    ax.collections[0].set_edgecolor("#000000")
    plt.axis('off')
    # plt.show()
    plt.savefig(BASE_DIR+ '/evolution.jpg')  #To show a stimulation of the changes in the graph formed at each call of visualise, on a jpg file named 'evolution' saved on the present directory
    plt.clf()
    plt.cla()

def assign_bmi(G): # assign a randmo bmi to each node ranging from 15 to 40 and set each node type as 'person'  
    for each in G.nodes():
        G.node[each]['name']=random.randint(15,40)
        G.node[each]['type']= 'person'

def get_labels(G):# create a dictionary with each node as key and its bmi as the value

    dict1={}
    for each in G.nodes():
        dict1[each]= G.node[each]['name']
    return dict1

def get_size(G):# return an array for node size, scaled 20 times the original bmi.

    array1=[]
    for each in G.nodes():
        if G.node[each]['type']=='person':
            array1.append(G.node[each]['name']*20)
        else:
            array1.append(1000)
            
    return array1

def add_foci_nodes(G):
    n = G.number_of_nodes()
    i = n+1
    foci_nodes=['gym', 'eatout', 'movie_club', 'karate_club', 'yoga_club']
    for j in range(0,5):
        G.add_node(i)
        G.node[i]['name']=foci_nodes[j]
        G.node[i]['type']='foci'
        i = i+1

def get_colors(G):
    c=[]
    for each in G.nodes():
        if G.node[each]['type']=='person':
            if G.node[each]['name']==15:
                c.append('green')
            elif G.node[each]['name']>=38:
                c.append('yellow')
            else:
                c.append('blue')
        else:
            c.append('red')
    return c

def get_foci_nodes():
    f=[]
    for each in G.nodes():
        if G.node[each]['type']=='foci':
            f.append(each)
    return f

def get_persons_nodes():
    p=[]
    for each in G.nodes():
        if G.node[each]['type']=='person':
            p.append(each)
    return p

def add_foci_edges():
    foci_nodes=get_foci_nodes()
    person_nodes=get_persons_nodes()
    for each in person_nodes:
        r=random.choice(foci_nodes)
        G.add_edge(each,r)

def homophily(G): #Making triadic closure
    pnodes = get_persons_nodes()
    for u in pnodes:
        for v in pnodes:
            if u!=v:
                diff = abs(G.node[u]['name'] - G.node[v]['name'])
                p = float(1)/(diff+1000)
                r = random.uniform(0,1)
                if r<p:
                    G.add_edge(u,v)

def cmn(u,v,G): #To return number of common friends of the nodes u and v in G
    nu = set(G.neighbors(u))
    nv = set(G.neighbors(v))
    return len(nu & nv)

def closure(G): #Making membership closure and foci closure
    array1= []
    for u in G.nodes():
        for v in G.nodes():
            if u!=v and (G.node[u]['type']=='person' or G.node[v]['type']=='person'):
                k = cmn(u,v,G)
                probability = 0.01 #The probab. of forming a triadic closure when there are only 1 common friends
                p = 1-math.pow((1-probability),k) # p = 1- (1-probability)^k , where k = no. of common friends
                tmp = []
                tmp.append(u)
                tmp.append(v)
                tmp.append(p)
                array1.append(tmp)
    # print(array1)
    for each in array1:
        u=each[0]
        v=each[1]
        p=each[2]
        r = random.uniform(0,1)
        if r<p:
            G.add_edge(u,v)

def change_bmi(G): #Showing the effect of Social Influence by increasing/decreasing bmi of nodes in eatouts/gym respectively
    fnodes = get_foci_nodes()
    for each in fnodes:
        if G.node[each]['name']=='eatout':
            for each1 in G.neighbors(each):
                if G.node[each1]['name']!=40:
                    G.node[each1]['name'] = G.node[each1]['name'] + 1
        
        if G.node[each]['name']=='gym':
            for each1 in G.neighbors(each):
                if G.node[each1]['name']!=15:
                    G.node[each1]['name'] = G.node[each1]['name'] - 1


G = create_Graph()
assign_bmi(G)
add_foci_nodes(G)
add_foci_edges()
time.sleep(4)
visualize(G)
for t in range(0,10):
    homophily(G)
    closure(G)
    change_bmi(G)
    visualize(G)

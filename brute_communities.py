import networkx as nx
import itertools
import intro2
import matplotlib.pyplot as plt


def communities_brute(G):
    nodes = G.nodes()
    n = G.number_of_nodes()

    first_community = []
    print("Generating the first community list ....")
    for i in range(1, int(n / 2 + 1)):
        comb = [list(x) for x in itertools.combinations(nodes, i)]
        # print("step:",i, "number of combinations found:", len(comb))
        first_community.extend(comb)
    print("First Community populated succesfully..")
    second_community = []
    print("Generating the second community list ....")
    for i in range(len(first_community)):
        l = list(set(nodes) - set(first_community[i]))
        # print("step:",i, "number of combinations found:", len(l))
        second_community.append((l))
    print("Second Community populated succesfully..")
    # print(first_community)
    # print(second_community)
    # which division is the best?
    num_intra_edges1 = []
    num_intra_edges2 = []
    num_INTER_edges = []
    ratio = []  # ratio of number of intra/inter community edges
    e = G.number_of_edges()

    print("Calculating the ratios..")
    for i in range(len(first_community)):
        num_intra_edges1.append(G.subgraph(first_community[i]).number_of_edges())
        num_intra_edges2.append(G.subgraph(second_community[i]).number_of_edges())
        num_INTER_edges.append(e - num_intra_edges1[i] - num_intra_edges2[i])
        # Finding the ratio
        try:
            ratio.append(
                (float)(num_intra_edges1[i] + num_intra_edges2[i]) / num_INTER_edges[i]
            )
        except ZeroDivisionError:
            print("Zero division error for Inter community edges. Please retry..")
    print("All necessary ratios have been found!..")
    max_value = max(ratio)
    max_index = ratio.index(max_value)
    # print(ratio)
    print("(", first_community[max_index], "),(", second_community[max_index], ")")


# G = intro2.create_network(35)
# communities_brute(G)
# nx.draw(G, with_labels=1)
# plt.show()

G = nx.barbell_graph(6, 2)
communities_brute(G)
nx.draw(G, with_labels=1)
plt.show()

import networkx as nx
import matplotlib.pyplot as plt
import random
import time


def display_graph(
    G, pos, labels, type1_node_list, type2_node_list, empty_cells, figure_number
):
    plt.figure(figure_number)

    nodes_w = nx.draw_networkx_nodes(G, pos, node_color="white", nodelist=empty_cells)
    nodes_r = nx.draw_networkx_nodes(G, pos, node_color="red", nodelist=type2_node_list)
    nodes_g = nx.draw_networkx_nodes(
        G, pos, node_color="green", nodelist=type1_node_list
    )
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels=labels)
    # To make the node outline as black
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#000000")
    plt.axis("off")

    plt.show()


def get_boundary_nodes(G, N):

    boundary_nodes_list = []
    for u, v in G.nodes():
        if u == 0 or u == N - 1 or v == 0 or v == N - 1:
            boundary_nodes_list.append((u, v))
    return boundary_nodes_list


def get_neigh(G, u, v):
    x = []
    for each in nx.neighbors(G, (u, v)):
        x.append(each)
    return x


def get_unsatisfied_nodes_list(G, t=3):
    unsatisfied_nodes_list = []
    for u, v in G.nodes():
        type_of_this_node = G.node[(u, v)]["type"]
        if type_of_this_node == 0:
            continue
        else:
            similar_node = 0
            neigh = get_neigh(G, u, v)
            for each in neigh:
                if G.node[each]["type"] == type_of_this_node:
                    similar_node += 1

            if similar_node <= t:
                unsatisfied_nodes_list.append((u, v))

    return unsatisfied_nodes_list


def make_a_node_satisfied(G, labels, unsatisfied_nodes_list, empty_cells):
    if len(unsatisfied_nodes_list) != 0:
        node_to_shift = random.choice(unsatisfied_nodes_list)
        new_position = random.choice(empty_cells)
        G.node[new_position]["type"], G.node[node_to_shift]["type"] = (
            G.node[node_to_shift]["type"],
            0,
        )
        labels[node_to_shift], labels[new_position] = (
            labels[new_position],
            labels[node_to_shift],
        )


def generate_all_3_node_list(G, type1_node_list, type2_node_list, empty_cells):
    for n in G.nodes():
        choice = random.randint(0, 2)
        G.node[n]["type"] = choice
        if choice == 1:
            type1_node_list.append(n)
        elif choice == 2:
            type2_node_list.append(n)
        else:
            empty_cells.append(n)


def iterate(N, cycles, t):
    G = nx.grid_2d_graph(N, N)  # making an NxN grid

    # To add diagonal edges
    for u, v in G.nodes():
        if (u + 1 <= N - 1) and (v + 1 <= N - 1):
            G.add_edge((u, v), (u + 1, v + 1))
        if (u + 1 <= N - 1) and (v - 1 >= 0):
            G.add_edge((u, v), (u + 1, v - 1))

    pos = dict((n, n) for n in G.nodes())
    labels = dict(((i, j), i * 10 + j) for i, j in G.nodes())

    type1_node_list = []
    type2_node_list = []
    empty_cells = []
    generate_all_3_node_list(G, type1_node_list, type2_node_list, empty_cells)

    display_graph(
        G,
        pos,
        labels,
        type1_node_list,
        type2_node_list,
        empty_cells,
        "Before Iteration",
    )

    boundary_nodes_list = get_boundary_nodes(G, N)
    internal_nodes_list = list(set(G.nodes()) - set(boundary_nodes_list))

    x_axis = []
    y_axis = []
    for i in range(cycles):
        unsatisfied_nodes_list = get_unsatisfied_nodes_list(G, t)
        satisfied_nodes_list = list(
            set(G.nodes()) - set(unsatisfied_nodes_list) - set(empty_cells)
        )
        # Generating 100 data points for satisfaction% corresponding to time
        intervals = int(cycles / 100)
        if i % intervals == 0:
            satisfaction_percent = (
                100 * len(satisfied_nodes_list) / (N * N - len(empty_cells))
            )
            x_axis.append(i)
            y_axis.append(satisfaction_percent)
            cycles_fraction_left = (cycles - i) / cycles
            if int((1 - cycles_fraction_left) * 100) % 5 == 0:
                print(int((1 - cycles_fraction_left) * 100), "% of task completed..")

        make_a_node_satisfied(G, labels, unsatisfied_nodes_list, empty_cells)
        type1_node_list = []
        type2_node_list = []
        empty_cells = []
        generate_all_3_node_list(G, type1_node_list, type2_node_list, empty_cells)
        if i == 1:
            print(
                "Starting operation of ",
                N,
                " x ",
                N,
                " nodes with ",
                cycles,
                " cycles..",
            )
            a = time.time()
        if i == 100:
            b = time.time()
            time_taken = float("{0:.2f}".format(b - a))
            print("estimated time lapsed: ", time_taken, " seconds...")
            print(
                "estimated time remaining: ",
                float(
                    "{0:.2f}".format(time_taken * cycles_fraction_left * cycles / 100)
                ),
                " seconds..",
            )
            time.sleep(3)

    display_graph(
        G, pos, labels, type1_node_list, type2_node_list, empty_cells, "After Iteration"
    )
    print("Task complete")
    return x_axis, y_axis


# To make a plot of satisfaction % of all nodes varying with time
def plot_satisfaction(N=10, cycles=1000, t=3):
    x_axis, y_axis = iterate(N, cycles, t)
    time.sleep(1)
    # display_graph(G, pos, labels, type1_node_list, type2_node_list, empty_cells)
    plt.figure(100)
    plt.xlabel("Iteration")
    plt.ylabel("Satisfaction %")
    plt.title("Change of satisfaction with iterations on " + str(N * N) + " nodes")
    plt.plot(x_axis, y_axis)
    plt.xlim(0, cycles)
    plt.ylim(0, max(y_axis) + 10)

    plt.show()


if __name__ == "__main__":
    plot_satisfaction(N=10, cycles=1000, t=3)

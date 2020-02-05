import networkx as nx
import community
import leidenalg as la
import igraph as ig
import time
import matplotlib.pyplot as plt


def load_graph(file):
    return nx.read_edgelist(path=file, comments='#',
                            delimiter=" ", nodetype=int)


if __name__ == "__main__":

    file = 'data/entexno.txt'

    r = load_graph(file=file)
    #r = nx.karate_club_graph()

    G = ig.Graph.Read_Edgelist(file, directed=False)
    #G = ig.Graph.Famous('Zachary')
    # to remove loops and multiple edges
    G = ig.Graph.simplify(G)

    start = time.time()
    louvain_partition = community.best_partition(r)
    end = time.time()
    print("Louvain partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    leiden_partition = la.find_partition(G, la.ModularityVertexPartition)
    end = time.time()
    print("Leiden partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    multilevel_partition = G.community_multilevel(return_levels=False)
    end = time.time()
    print("Multilevel partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    fastgreedy = G.community_fastgreedy()
    fastgreedy_partition = fastgreedy.as_clustering()
    end = time.time()
    print("Fastgreedy partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    infomap_partition = G.community_infomap()
    end = time.time()
    print("Infomap partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    newman_partition = G.community_leading_eigenvector()
    end = time.time()
    print("Newman partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    start = time.time()
    label_propagation_partition = G.community_label_propagation()
    end = time.time()
    print("Label propagation partitioning finished! Time elapsed : {:.3f}s".format(float(end - start)))

    #start = time.time()
    #edge_betweenness_partition = G.community_edge_betweenness().as_clustering()
    #end = time.time()
    #print("Edge betweenness partitioning finished! Time elapsed : {:.3f}s".format(end - start))

    #start = time.time()
    #spinglass_partition = G.community_spinglass()
    #end = time.time()
    #print("Spinglass partitioning finished! Time elapsed : {:4.3}s".format(end - start))

    start = time.time()
    walktrap_partition = G.community_walktrap().as_clustering()
    end = time.time()
    print("Walktrap partitioning finished! Time elapsed : {:4.3}s".format(float(end - start)))
    # print(len(cl[0]), len(cl[1]), len(cl[2]), len(cl[3]), len(cl[4]))

    # Prints the number of clusters/communities found by each algorithm
    print("Louvain communities: ", len(set(louvain_partition.values())))
    print("Leiden communities: ", len(leiden_partition))
    print("Multilevel communities: ", len(multilevel_partition))
    print("Fastgreedy communities: ", len(fastgreedy_partition))
    print("Infomap communities: ", len(infomap_partition))
    print("Newman communities: ", len(newman_partition))
    print("Label propagation communities: ", len(label_propagation_partition))
    #print(len(edge_betweenness_partition))
    #print(len(spinglass_partition))
    print("Walktrap communities: ", len(walktrap_partition))

    # Prints the modularity score of the partitions found by each algorithm
    print("Modularity of louvain partition: ", community.modularity(louvain_partition, r))
    print("Modularity of leiden partition: ", ig.Graph.modularity(G, leiden_partition))
    print("Modularity of multilevel partition: ", ig.Graph.modularity(G, multilevel_partition))
    print("Modularity of fastgreedy partition: ", ig.Graph.modularity(G, fastgreedy_partition))
    print("Modularity of infomap partition: ", ig.Graph.modularity(G, infomap_partition))
    print("Modularity of newman partition: ", ig.Graph.modularity(G, newman_partition))
    #print("Modularity of label propagation partition: ", ig.Graph.modularity(G, label_propagation_partition))
    #print("Modularity of edge betweenness partition: ", ig.Graph.modularity(G, edge_betweenness_partition))
    #print("Modularity of spinglass partition: ", ig.Graph.modularity(G, spinglass_partition))
    print("Modularity of walktrap partition: ", ig.Graph.modularity(G, walktrap_partition))

    # Plots the community structures
    ig.plot(leiden_partition)

    # Drawing for networkx
    size = float(len(set(louvain_partition.values())))
    pos = nx.spring_layout(r)

    count = 0

    for com in set(louvain_partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in louvain_partition.keys()
                      if louvain_partition[nodes] == com]
        nx.draw_networkx_nodes(r, pos, list_nodes, node_size=20,
                               node_color=str(count / size))

    nx.draw_networkx_edges(r, pos, alpha=0.5)
    plt.show()

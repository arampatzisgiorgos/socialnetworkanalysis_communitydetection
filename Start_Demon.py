import networkx as nx
import DEMON.demon.alg as d
from f1_communities.nf1 import NF1
import csv
import time

FOLDER_NAME = "DBLP"
original_graph_path = 'data/' + FOLDER_NAME +  '/com-dblp.ungraph.txt'
ground_truth_comms_path = 'data/' + FOLDER_NAME + '/com-dblp.all.cmty.txt'

#load graph
G = nx.Graph()
graph_values = list(csv.reader(open(original_graph_path, 'r'), delimiter='\t'))
for value in graph_values:
    G.add_edge(value[0], value[1])


#DEMON algorithm
t = time.time()
dm = d.Demon(graph=G, epsilon=0.25, min_community_size=3)
predicted_communities = dm.execute()
print("DEMON time: " + repr(time.time() - t))


#write communities to file
with open('data/' + FOLDER_NAME + "/DEMON_predicted_communities.txt", "w") as csvfile:
    writer = csv.writer(csvfile, dialect="excel-tab")
    for comm in predicted_communities:
        writer.writerow(comm)


#F1 Score
print("___________ F1 Score ___________")
pred_coms = [tuple(x) for x in predicted_communities]

ground_truth_comms = list(csv.reader(open(ground_truth_comms_path, 'r'), delimiter='\t'))
ground_truth_coms = [tuple(x) for x in ground_truth_comms]

# Computing the NF1 scores and statistics
nf = NF1(pred_coms, ground_truth_coms)
results = nf.summary()
print(results['scores'])
print(results['details'])


'''print("___________ F1 Score from file ___________")
pred_coms_comms = list(csv.reader(open('data/pred_com.txt', 'r'), delimiter='\t'))
pred_coms = [tuple(x) for x in pred_coms_comms]

ground_truth_comms = list(csv.reader(open('data/ground_truth_com.txt', 'r'), delimiter='\t'))
ground_truth_coms = [tuple(x) for x in ground_truth_comms]

# Computing the NF1 scores and statistics
nf = NF1(pred_coms, ground_truth_coms)
results = nf.summary()
print(results['scores'])
print(results['details'])'''

from __future__ import division
import Queue
import copy
import collections

def is_valid_sequence(sent_format, word_seq):

    if len(sent_format) != len(word_seq):
        return False

    format_seq = map(lambda i: i[i.index("/")+1:], word_seq)

    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    return compare(sent_format, format_seq)

def may_form_valid_sequence(sent_format, word_seq):


    format_seq = map(lambda i: i[i.index("/")+1:], word_seq)

    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    return compare(sent_format[:len(format_seq)], format_seq)

graph = {}
def create_graph():
    f = open('input.txt', 'r')
    sequence = [line.strip().split("//") for line in f]
# sequence = [map(lambda p: p.replace("/", "_"), parts) for parts in sequence]

# for line in f:
#     parts = line.strip().split("//")
    for item in sequence:
        if graph.get(item[0]) is None:
            graph[item[0]] = []
        graph[item[0]].append((item[1], float(item[2])))

pos_adjacency_probs = {}
def create_pos_adjacencies():
    for key, adj_nodes in graph.iteritems():
        pos_dict_node = {}
        pos_seq = map(lambda x: x[0][x[0].index("/")+1:], adj_nodes)
        for pos in pos_seq:
            if pos_dict_node.get(pos) is None:
                pos_dict_node[pos] = 0
            pos_dict_node[pos] += 1
        pos_adjacency_probs[key] = {k: v/len(pos_seq) for k,v in pos_dict_node.iteritems()}


def generate(startWord, sentFormat):
    q = Queue.Queue()
    q.put(([startWord+"/"+sentFormat[0]],1))
    max_prob = 0
    max_path = ""
    iteration_count = 0
    while not q.empty():
        source,last_prob = q.get()
        lastWord = source[len(source)-1]
        adj = graph[lastWord] if graph.get(lastWord) is not None else []
        for node in adj:
            sourceCopy = copy.deepcopy(source)
            sourceCopy.append(node[0])

            if may_form_valid_sequence(sentFormat, sourceCopy):

                if is_valid_sequence(sentFormat, sourceCopy):
                    current_prob = last_prob*node[1]
                    if current_prob > max_prob:
                        max_prob = current_prob
                        max_path = sourceCopy
                else:

                    current_prob = last_prob*node[1]
                    q.put((sourceCopy, current_prob));
        iteration_count += 1
    return max_path, max_prob, iteration_count


def generate_with_heuristic(startWord, sentFormat):
    q = Queue.PriorityQueue()
    q.put((-1, ([startWord+"/"+sentFormat[0]],1)))
    max_prob = 0
    max_path = ""
    iteration_count = 0
    while not q.empty():
        heuristic, (source, last_prob) = q.get()
        lastWord = source[len(source)-1]
        adj = graph[lastWord] if graph.get(lastWord) is not None else []
        for node in adj:
            sourceCopy = copy.deepcopy(source)
            sourceCopy.append(node[0])

            if may_form_valid_sequence(sentFormat, sourceCopy):

                if is_valid_sequence(sentFormat, sourceCopy):
                    current_prob = last_prob*node[1]
                    if current_prob > max_prob:
                        max_prob = current_prob
                        max_path = sourceCopy
                else:
                    if pos_adjacency_probs.get(node[0]) is None:
                        continue

                    nplus1_probability = -pos_adjacency_probs[node[0]][sentFormat[len(source)+1]]  \
                         if pos_adjacency_probs[node[0]].get(sentFormat[len(source)+1]) is not None else 0
                    if nplus1_probability == 0: # if you put these in the queue they will eventually be evaluated
                        continue
                    current_prob = last_prob*node[1]
                    heuristic_prob = current_prob*nplus1_probability
                    q.put((heuristic_prob, (sourceCopy, current_prob)))
        iteration_count += 1

    return max_path, max_prob, iteration_count

#Tests
print is_valid_sequence(["NNP", "VDB","DT","NN"], ["beasts/NNP","made/VDB","stayed/DT","garments/NN"])
print may_form_valid_sequence(["NNP", "VDB","DT","NN"], ["beasts/NNP","made/VDB","stayed/DT"])


create_graph()
create_pos_adjacencies()

print graph.get('cry/NN')
test_start_word = "hans"
test_sent_format = ["NNP", "VBD", "DT", "NN"]
print generate(test_start_word,test_sent_format)
print generate_with_heuristic(test_start_word,test_sent_format)

test_start_word = "benjamin"
test_sent_format = ["NNP", "VBD", "DT", "NN"]
print generate(test_start_word,test_sent_format)
print generate_with_heuristic(test_start_word,test_sent_format)

test_start_word = "a"
test_sent_format = ["DT", "NN", "VBD", "NNP"]
print generate(test_start_word,test_sent_format)
print generate_with_heuristic(test_start_word,test_sent_format)

test_start_word = "benjamin"
test_sent_format = ["NNP", "VBD", "DT", "JJS", "NN"]
print generate(test_start_word,test_sent_format)
print generate_with_heuristic(test_start_word,test_sent_format)

test_start_word = "a"
test_sent_format = ["DT", "NN", "VBD", "NNP", "IN", "DT", "NN"]
print generate(test_start_word,test_sent_format)
print generate_with_heuristic(test_start_word,test_sent_format)


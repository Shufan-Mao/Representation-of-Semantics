from Programs.Spatial_Models import cooc_matrix, spatial_analysis
from Programs.Graphical_Models import graphical_analysis, STN

########################################################################################################################
# In Humans, corpora generated are lists of sentences, to feed the linear models, need to first transform the sentences
# into word tokens
# list of sentences into list of words, for spatial models
########################################################################################################################


########################################################################################################################
# transform list of sentences into list of words (if no boundary), keep or remove period, get vocabulary of the corpus
########################################################################################################################

def corpus_transformation(linear_corpus, period, boundary):
    word_bag = []
    vocab_index_dict = {}
    vocab_list = []
    for sentence in linear_corpus:
        sent = sentence.copy()
        if not period:
            sent.remove('.')
        for word in sent:
            if not boundary:
                word_bag.append(word)
            if word not in vocab_index_dict:
                l = len(vocab_list)
                vocab_index_dict[word] = l
                vocab_list.append(word)
        if boundary:
            word_bag.append(sent)
    return word_bag, vocab_list, vocab_index_dict

########################################################################################################################
# get the co-occurrence/similarity matrix for each model variation
########################################################################################################################

def build_model(word_bag, vocab_list, vocab_index_dict, model_parameters):
    encoding = {}
    encoding['window_type'] = model_parameters['window_type']
    encoding['window_size'] = model_parameters['window_size']
    encoding['window_weight'] = model_parameters['window_weight']
    normalization = model_parameters['normalization']
    sim_type = model_parameters['encode']
    if sim_type[0] == 'r':
        reduction = 'svd'
    else:
        reduction = 'non'
    boundary = model_parameters['boundary']
    if boundary == 'yes':
        boundary = True
    else:
        boundary = False
    grand_matrix = cooc_matrix.get_cooc_matrix(vocab_list, vocab_index_dict, word_bag, encoding, normalization,
                                                   reduction, boundary)
    if reduction == 'non':
        sim_matrix = spatial_analysis.get_sr_matrix(grand_matrix, vocab_list, vocab_list, vocab_index_dict, sim_type)
    else:
        sim_matrix = spatial_analysis.get_sr_matrix(grand_matrix[0], vocab_list, vocab_list, vocab_index_dict, sim_type)
    return grand_matrix, sim_matrix

def build_structured_model(corpus): # model adjacency matrix for non-lexical nextworks:
    constituent_net = STN.Stn(corpus)
    node_list = constituent_net.network[1]
    constituent_matrix = graphical_analysis.get_adjacency_matrix(constituent_net)[0]
    return constituent_matrix, node_list













import math
import numpy as np
from cytoolz import itertoolz

PAD = '*PAD*'
VERBOSE = False
period = True


def corpus_transformation(linear_corpus, period_mark):  # list of sentence into list of words, for spatial models
    corpus = []
    vocab_index_dict = {}
    vocab_list = []
    for sentence in linear_corpus:
        for word in sentence:
            corpus.append(word)
            if word not in vocab_index_dict:
                l = len(vocab_list)
                vocab_index_dict[word] = l
                vocab_list.append(word)
        if period_mark:
            corpus.append('.')
    if period_mark:
        vocab_list.append('.')
        vocab_index_dict['.'] = len(vocab_list)-1
    return corpus, vocab_list, vocab_index_dict

########################################################################################################################
# HAL co-occurence count, varied by window type, window size and window weight
########################################################################################################################

def create_ww_matrix(vocab_list, vocab_index_dict, tokens, encoding):  # no function call overhead - twice as fast
    window_type = encoding['window_type']
    window_size = encoding['window_size']
    window_weight = encoding['window_weight']
    # count
    num_vocab = len(vocab_list)
    count_matrix = np.zeros([num_vocab, num_vocab])
    if VERBOSE:
        print('\nCounting word-word co-occurrences in {}-word moving window'.format(window_size))

    for i in range(window_size):
        tokens.append(PAD)

    windows = itertoolz.sliding_window(window_size + 1, tokens)  # + 1 because window consists of t2s only
    for window in windows:
        # print(window)
        if window[0] in vocab_index_dict:
            for i in range(window_size):
                if window[i+1] in vocab_index_dict:
                    dist = 1/(i+1)
                    if window_weight == "linear":
                        count_matrix[vocab_index_dict[window[0]], vocab_index_dict[window[i+1]]] += dist
                    elif window_weight == "flat":
                        count_matrix[vocab_index_dict[window[0]], vocab_index_dict[window[i+1]]] += 1
    # window_type
    if window_type == 'forward':
        final_matrix = count_matrix
    elif window_type == 'backward':
        final_matrix = count_matrix.transpose()
    elif window_type == 'summed':
        final_matrix = count_matrix + count_matrix.transpose()
    elif window_type == 'concatenated':
        final_matrix = np.concatenate((count_matrix, count_matrix.transpose()), axis=1)
    else:
        raise AttributeError('Invalid arg to "window_type".')
    #  print('Shape of normalized matrix={}'.format(final_matrix.shape))
    return final_matrix


def get_ppmi_matrix(ww_matrix):  # get ppmi martix from co-occurrence matrix
    size = ww_matrix.shape
    ppmi_matrix = np.zeros(size)
    pmi_matrix = np.zeros(size)
    row_sum = ww_matrix.sum(1)
    column_sum = ww_matrix.sum(0)
    grand_sum = ww_matrix.sum()
    for i in range(size[0]):
        for j in range(size[1]):
            if ww_matrix[i][j] != 0:
                ppmi_matrix[i][j]=math.log2(ww_matrix[i][j]*grand_sum/(row_sum[i]*column_sum[j]))
                pmi_matrix[i][j] = ppmi_matrix[i][j]
                if ppmi_matrix[i][j] < 0:
                    ppmi_matrix[i][j] = 0
            else:
                ppmi_matrix[i][j] = 0
                pmi_matrix[i][j] = 0
    return ppmi_matrix, pmi_matrix
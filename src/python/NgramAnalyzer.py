import heapq as hq


class NgramAnalyzer():

    def __init__(self, label_map, n, c):

        num_files = len(label_map)  # number of files
        self.c = c  # number of classes
        self.n = n  # number of bytes per features

        self.label_counts = self.compute_label_counts(
            label_map)  # files per class
        self.p_y = [1.0 * lc / num_files for lc in self.label_counts]

    def compute_label_counts(self, label_map):
        ''' counts the number of files per class, given a map of
        filename to class label  '''

        label_counts = [0] * self.c

        # iterate over the map and update the label counts
        for idx in label_map.itervalues():
            label_counts[idx] += 1

        return label_counts

    def compute_mutual_information(self, ngram_counts):
        '''computes the classic mutual information given ngram counts

        Parameters
        ----------
        param: ngram_counts - list of counts of ngram occurrence per class
        type: list(<int>)

        Returns
        -------
        param: mutual_info - mutual information
        type: float 
        '''

        # values needed for computing mutual information
        p_x_1_given_y = [
            nc / lc for nc, lc in zip(ngram_counts, self.label_counts)]  # p(x=1|y)
        p_x_1_and_y = [
            x_1_y * y for x_1_y, y in zip(p_x_1_given_y, p_y)]  # p(x=1,y)
        p_x_1 = sum(p_x_1_and_y)  # p(x=1)

        # compute difference in entropy
        mutual_info = 0
        for x_1_and_y, x_1_y, p_y_i in zip(p_x_1_and_y, p_x_1_given_y, self.p_y):
            mutual_info += 0 if x_1_y == 0 else x_1_y * \
                p_y_i * log(x_1_y / p_x_1, 2)
            mutual_info += 0 if x_1_y == 1 else (
                1 - x_1_y) * p_y_i * log((1 - x_1_y) / (1 - p_x_1), 2)

        return mutual_info

    def compute_top_k_ngrams(self, ngram_tuple_list, k):
        ''' given a list of tuples of the form (ngram, ngram_count), returns a tuple list
        (ngram, MI) of the top K ngrams with the highest mutual information 

        Parameters
        ----------
        param: ngram_tuple_list - list of tuples of the form (ngram, ngram_count)
        type: list(<tuple(<str,list(<float>)>)>)

        param: k - number of ngrams we would like to have returned
        type: int

        Returns
        -------
        param: top_k_list - top k ngrams with highest mutual info
        type: list(<tuple(<str,float>)>)

        '''

        top_k_list = []  # tuple heap

        for ngram_tuple in ngram_tuple_list:

            # get the next ngram tuple...
            ngram = ngram_tuple[0]
            ngram_counts = ngram_tuple[1]

            # ...and compute its mutual information
            mutual_info = self.compute_mutual_information()

            # if the heap hasn't been filled yet...
            if len(top_k_set) < k:
                hq.heappush(top_k_set, (mutual_info, ngram))

            # or if it has, and the mutual information is greater than the
            # minimum, pop the minimum tuple out, and push in the new tuple
            elif len(top_k_set) == k and mutual_info > top_k_set[0][0]:

                # equivalent to pop->push, but supposedly faster
                hq.heapreplace(top_k_set, (mutual_info, ngram))

        # reverse the order of the tuples; initially had to do (mi,ng) for the heap,
        # but it makes more sense to order it (ng,mi)
        top_k_list = [(tup[1], tup[0]) for tup in top_k_list]

        return top_k_list

class NgramExtractor():

    def __init__(self, label_map, n, c):

        self.ngram_map = {}  # map of ngrams to frequencies
        self.label_map = label_map  # map of filenames to class label
        self.n = n  # number of bytes per features
        self.c = c  # number of classes

    def add_to_ngram_map(self, ngram_set, label):
        ''' Given a set of n-grams found in a filename of a particular class,
        update the ngram map

        Parameters
        ----------
        param: label - class label of the file
        type: str

        param: ngram_set - set of ngrams found in a file
        type: set(<str>)

        Returns
        -------
        None

        Updates
        -------
        self.ngram_map

        '''
        for ngram in ngram_set:
            if not ngram not in self.ngram_map:
                self.ngram_map[ngram] = [0] * c
            self.ngram_map[ngram][label] += 1

    def count_ngrams(self, filenames):
        ''' Given a set of filenames, count the number of files per class that each n-gram
        occurs in, and update the ngram map

        Parameters
        ----------
        param: filenames - iterator for files
        type: iterable

        Returns
        -------
        param: self.ngram_map converted to a list of tuples
        type: list(<tuple(<str,list(<int>)>)>)

        Updates
        -------
        self.ngram_map

        '''

        for filename in filenames:
            byte_list = []
            ngram_set = set()

            # read each line, appending bytes (pairs of hex chars) to a list
            with open(filename, "r") as f:
                rows = f.readlines()
                for row in rows:
                    byte_list += row.split()[1:]
                    # remove any line-feeds
                    byte_list[-1] = byte_list[-1].rstrip('\n')

            # get the first n-gram of the file and put it in the set
            ngram_seq = byte_list[:n]
            ngram = ''.join(ngram_seq)
            assert len(ngram) == self.n * 2  # 2 hex chars per byte ('gram')
            ngram_set.add(ngram)

            for byte in byte_list[n:]:
                # get the next ngram and add it to the set
                ngram_seq = ngram_seq[1:]
                ngram_seq.append(byte)
                ngram = ''.join(ngram_seq)
                assert len(ngram) == self.n * 2
                ngram_set.add(ngram)

            # add it to the map
            add_to_ngram_map(ngram_set, label)

        return [(k, v) for k, v in self.ngram_map.iteritems()]

from math import log

def accumulate(k, x):
	''' simple accumulate function for summing the elements of two iterables '''
    return [i+j for i,j in zip(k,x)]

def compute_mutual_information(label_counts,ngram_list):
    ''' Computes the mutual information for each n-gram, given its frequencies '''
    
    num_files = sum(label_counts) # number of files
    p_y = [1.0*lc/num_files for lc in label_counts] # p(y)
    
    ngram_mi = {} # map that holds the mutual information per n-gram
    
    for ngram_tuple in ngram_list:

        ngram = ngram_tuple[0]
        ngram_counts = ngram_tuple[1]

        # values needed for computing mutual information 
        p_x_1_given_y = [nc/lc for nc,lc in zip(ngram_counts,label_counts)] # p(x=1|y)
        p_x_1_and_y = [x_1_y*y for x_1_y,y in zip(p_x_1_given_y,p_y)] # p(x=1,y)
        p_x_1 = sum(p_x_1_and_y) # p(x=1)
        
        mutual_info = 0
        
        for x_1_given_y,p_y_i in zip(p_x_1_given_y,p_y):
        	
        	# needed to handle p(x|y) = 0 case
            mutual_info += 0 if x_1_given_y == 0 else x_1_y*p_y_i*log(x_1_y/p_x_1,2)
            mutual_info += 0 if x_1_given_y == 1 else (1-x_1_y)*p_y_i*log((1-x_1_y)/(1-p_x_1),2)
            
        ngram_mi[ngram] = mutual_info
    
    return ngram_mi

def filename_to_label(filename):
	''' function to return the label of a given filename '''
	pass

def add_to_ngram_map(filename,label,ngram_set,ngram_map):
    ''' adds an ngram to the global ngram_map '''
   
   # label_idx = convert_to_idx(label)

    for ngram in ngram_set:
        if not ngram in ngram_map:
            ngram_map[ngram] = [0]*c
        ngram_map[ngram][label] += 1

def ngram_count(filenames):
    ''' given a set of files, returns a map of ngrams->frequencies '''
    
    ngram_map = {}
   
    for filename in filenames:
        byte_list = []

        # read each line, appending bytes (in hex) to a list. TODO: is there a 
        # faster/more efficient way to do this??
        with open(filename, "r") as f:
            rows = f.readlines()
            for row in rows:
                byte_list += row.split()[1:]
                byte_list[-1] = byte_list[-1].rstrip('\n') # get rid of any annoying return lines
        
        # get the first n-gram of the file
        ngram_seq = byte_list[:n] 
        ngram = ''.join(ngram_seq)
        ngram_set = set([ngram]) # initialize the set with the first ngram

        for byte in byte_list[n:]:
            
            # get the next ngram
            ngram_seq = ngram_seq[1:]
            ngram_seq.append(byte)
            ngram = ''.join(ngram_seq)
            
            # add it to the set
            ngram_set.add(ngram)
            
        # update the map with the new n-gram
        add_to_ngram_map(filename,ngram_set,ngram_map)
    
    # Turn into tuples (needed for spark)
    return [(k, v) for k, v in ngram_map.iteritems()]
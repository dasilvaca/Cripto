from math import sqrt

l = "sjfbasbpgbdpgadg"

def _repeated_seq_pos(text, seq_len):
    seq_pos = {}  # entries of sequence : [positions]
    for i, char in enumerate(text):
        next_seq = text[i:i+seq_len]
        if next_seq in seq_pos.keys():
            seq_pos[next_seq].append(i)
        else:
            seq_pos[next_seq] = [i]
    repeated = list(filter(lambda x: len(seq_pos[x]) >= 2, seq_pos))
    rep_seq_pos = [(seq, seq_pos[seq]) for seq in repeated]
    return rep_seq_pos


def _get_spacings(positions):
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]


def _get_factors(number):
    factors = set()
    for i in range(1, int(sqrt(number))+1):
        if number % i == 0:
            factors.add(i)
            factors.add(number//i)
    return sorted(factors)


def _candidate_key_lengths(factor_lists, max_key_len):
    all_factors = [factor_lists[lst][fac] for lst in range(len(factor_lists)) for fac in range(len(factor_lists[lst]))]
    # exclude factors larger than suspected max key length
    candidate_lengths = list(filter(lambda x:  x <= max_key_len, all_factors))
    # sort by probability (descending)
    sorted_candidates = sorted(set(candidate_lengths), key=lambda x: all_factors.count(x), reverse=True)
    return sorted_candidates


def find_key_length(cyphertext, seq_len, max_key_len):
    # find repeated sequences and their positions
    rsp = _repeated_seq_pos(text=cyphertext, seq_len=seq_len)
    seq_spc = {}
    for seq, positions in rsp:
        seq_spc[seq] = _get_spacings(positions)
    # calculate spacings between positions of each repeated
    # sequence and factor out spacings
    factor_lists = []
    for spacings in seq_spc.values():
        for space in spacings:
            factor_lists.append(_get_factors(number=space))
    # get common factors by descending frequency,
    # which constitute candidate key lengths
    ckl = _candidate_key_lengths(factor_lists=factor_lists, max_key_len=max_key_len)
    key_len = ckl[0]
    return key_len


def getDivisors(n):
    l = []
    for i in range(2,n):
        if n % i == 0:
            l.append(i)
    return l

#l argument should be a list containing all bytes of the file (read with toList)
def getTuples(l):
    res = {}
    freq =[]
    count = 0
    i = 0
    while i < len(l): # Loop through all the list
        elt= l[i:i+3] # Take at least 3-character length for tuples
        long = len(elt)
        if long == 3: #should be 3 if not means we are at the end of the list
            for j in range(i+1,len(l)): #Find further in the list for the same pattern
                if l[i:i+long] == l[j:j+long]: #If match the 3-char check for more
                    while l[i:i+long] == l[j:j+long]:
                        long = long + 1
                    long = long -1
                    elt = l[i:i+long] # Now we have a tuple 
                    diff = j - i # Compute the distance
                    freq.extend(getDivisors(diff)) #Add the divisors to the list 
                    print ("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % (elt,i,j, diff,getDivisors(diff))) #Print information about the tuple (can be deleted)
                    count = count +1
                    j = j + long + 1
            i = i + long -3 +1
        else:
            i = i + 1
    return count, freq


def countOcc(l): # return list with (decimal_char, occ) 
    d={}
    for elt in l:
        if d.has_key(elt):
            d[elt] += 1
        else:
            d[elt] = 1
    return sorted(d.items(),key=lambda x: x[1], reverse=True)

def explode(key,li):
    dic = {}
    for e in range(1,key+1):
        dic[e] = []
    i = 0
    for index in range(len(li)):
        if i == key:
            i = 0
        dic[i+1].append(li[index])
        i = i + 1
    return dic

def decipher(l,diff):
    newl = list()
    for e in l:
        val = e - diff
        if val < 0:
            newl.append(256 + (val % -256))
        else:
            newl.append(val)
    return newl

def recreate(dic):
    i = 0
    output = []
    try:
        while 1:
            for l in dic.values():
                output.append(l[i])
            i = i + 1
    except:
        pass
    return output

res = explode(10, l) #We consider in this exemple a key length of 10 and l the original list
for i in range(1,10+1): #For each sub-list
    occ = countOcc(res[i]) #Make a frequency analysis
    shift = (occ[0][0] - 32) % 256 # Consider the most frequent element of being a space(32 in decimal)
    print ("Frequency analysis for the index: %s\tshift:%s\n%s\n" % (i,shift,occ)) #Print informations (can be deleted)
    res[i] = decipher(res[i],shift) #Try do decipher using a classical ceaser function and the determined shift

final = recreate(res) #Once we have processed all sub-list recreate a list with all the sub-lists.
print (''.join([chr(x) for x in final])) #Print the result
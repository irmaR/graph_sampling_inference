
# Some utilities for graph sampling scripts

import math



def kld(p, q):
    """
    Function that computes Kullback-Leibler divergence of two discrete probability distributions.
    The probability distributions 'p' and 'q' must be python lists.
    Log2 is used in this implementation, so the outcome is in bits. 
    """
    sum = 0
    for i in range(len(p)):
        sum += p[i] * ( math.log(p[i],  2) - math.log(q[i],  2) )
    return sum

def kld_dict_old(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        q_list.append(q[k])
    return kld(p_list,  q_list)


def kld_dict(p, q):
    """The same as 'kld()', but made to handle distributions given as python dictionaries."""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
##        else:
##            q_list.append(0.00000000001)
    return kld(p_list,  q_list)


def hellinger(p, q):
    """
    Calculates the Hellinger distance (using Bhattacharyya coefficient) among discrete probability distributions 'p' and 'q', given as python lists.
    It is bounded to [0, 1], unlike the Bhattacharyya, which is unbounded.
    Often the Hellinger distance is wrongly reffered to as Bhattacharyya distance.
    """
    coef = 0
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    argu = 1 - coef
    if argu <= 0:   # can happen to be 0, because of Python's rounding
        argu = 0.000000000000001
    return math.sqrt(argu)

def hellinger_dict(p,  q):
    """The same as 'hellinger()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
##        else:
##            q_list.append(0.00000000001)
    return hellinger(p_list,  q_list)
    


def bhatta(p, q):
    """
    Calculates the Bhattacharyya distance among discrete probability distributions 'p' and 'q', given as python lists
    """
    coef = 0
    for i in range(len(p)):
        coef = coef + math.sqrt(p[i] * q[i])
    return -1 * math.log(coef)
    
def bhatta_dict(p,  q):
    """The same as 'bhatta()', but made to handle distributions given as python dictionaries"""
    p_list = []
    q_list=[]
    for k in p.keys():
        p_list.append(p[k])
        if k in q.keys():
            q_list.append(q[k])
##        else:
##            q_list.append(0.00000000001)
    return bhatta(p_list,  q_list)
    
    
def abs_d_diff(p, q):
    """
    Returns the absolute difference among discrete probability distributions 'p' and 'q', which are given as python dictionaries.
    A sum of absolute differences at each value.
    """
    diff = 0
    for k in p.keys():
        diff = diff + abs(p[k] - q[k])
    return diff


def cum_abs_d_diff(p_table,  q_table):
    """
    Returns a cumulative absolute difference among two discrete probability distribution tables - so, collections of distributions.
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    Absolute differences of all distributions are summed together and returned
    """
    err = 0
    for k in p_table.keys():
        ierr = abs_d_diff(p_table[k],  q_table[k])
        err = err + ierr
    return err


def avg_kld(p_table,  q_table):
    """
    Returns an average Kullback-Leibler divergence of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_kld = 0
    for k in p_table.keys():
        kld_i = kld_dict(p_table[k],  q_table[k])
        cum_kld = cum_kld + kld_i
    return float(cum_kld)/len(p_table.keys())


def avg_hellinger(p_table,  q_table):
    """
    Returns an average Hellinger distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_hd = 0
    for k in p_table.keys():
        hd_i = hellinger_dict(p_table[k],  q_table[k])
        cum_hd = cum_hd + hd_i
    return float(cum_hd)/len(p_table.keys())


def avg_bhatta(p_table,  q_table):
    """
    Returns an average Bhattacharyya distance of two discrete probability distribution tables - that is. collections of distributions
    Each table is represented as a dictionary
            - its keys are parent value tuples, e.g.: '('high', 'high')'
            - its values are distributions in form of python dictionaries, e.g.: '{'high': 0.4388059701492537, 'low': 0.34746268656716417, 'mid': 0.2137313432835821}'
    """
    cum_bd = 0
    for k in p_table.keys():
        bd_i = bhatta_dict(p_table[k],  q_table[k])
        cum_bd = cum_bd + bd_i
    return float(cum_bd)/len(p_table.keys())

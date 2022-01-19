"""
Metrics

main functions:
hit_rate
hit_rate_at_k
precision
precision_at_k
money_precision_at_k
recall
recall_at_k
money_recall_at_k
ap_k
map_k
reciprocal_rank
"""
import numpy as np

def hit_rate(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(bought_list, recommended_list)
    return (flags.sum() > 0) * 1

def hit_rate_at_k(recommended_list, bought_list, k=5):
    # lets assume that recommended list presorted according goods importance
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list[:k] if k > 0 else recommended_list)
    hit_rate = (np.sum(np.in1d(recommended_list, bought_list)) > 0) *1
    return hit_rate

def precision(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(recommended_list)

def precision_at_k(recommended_list, bought_list, k=5):
    return precision(recommended_list[:k], bought_list)

def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
    # lets assume that recommended_list and prices_recommended is agreed
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list[:k])
    checked_list = np.isin(bought_list, recommended_list) * bought_list
    checked_list = checked_list[checked_list!=0]    
    prices_recommended_in_bought = [np.sum(np.where(recommended_list == recommended_id, prices_recommended[:k], 0)) 
                          for recommended_id in checked_list]
    return np.sum(prices_recommended_in_bought) / np.sum(prices_recommended[:k])

"""def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
    recommended_list = np.array(recommended_list)[:k]
    prices_recommended = np.array(prices_recommended)[:k]
    flags = np.isin(recommended_list, bought_list)
    return np.dot(flags, prices_recommended).sum() / prices_recommended.sum()"""

def recall(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    flags = np.isin(bought_list, recommended_list)
    return flags.sum() / len(bought_list)


def recall_at_k(recommended_list, bought_list, k=5):
    return recall(recommended_list[:k], bought_list)


def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    prices_recommended = np.array(prices_recommended)[:k]
    prices_bought = np.array(prices_bought)
    flags = np.isin(recommended_list, bought_list)
    return np.dot(flags, prices_recommended).sum() / prices_bought.sum()


def ap_k(recommended_list, bought_list, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    recommended_list = recommended_list[recommended_list <= k]
    relevant_indexes = np.nonzero(np.isin(recommended_list, bought_list))[0]
    if len(relevant_indexes) == 0:
        return 0
    amount_relevant = len(relevant_indexes)
    sum_ = sum(
        [precision_at_k(recommended_list, bought_list, k=index_relevant + 1) for index_relevant in relevant_indexes])
    return sum_ / amount_relevant

def map_k(recommended_lists, bought_lists, k=5):
    if np.shape(recommended_lists)[0] == np.shape(bought_lists)[0]:
        result_list = np.sum([ap_k(recommended_list_i, bought_list_i, k) \
                         for recommended_list_i, bought_list_i in zip(recommended_lists, \
                                                                      bought_lists)])/ \
                np.shape(recommended_lists)[0]
    else:
        result_list = False
    return result_list

def reciprocal_rank(recommended_list, bought_list, k=1):
    ku = np.array([])
    for item in recommended_list[:k]:
        ind = np.where(bought_list == item)[0]
        if np.shape(ind) > 0:
            ku = np.append(ku,np.where(bought_list == item)[0][0])
    return np.mean(1/ku)

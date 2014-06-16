__author__ = 'pok'
import sys

sys.path.append("../utility/")
from rec_data_model import RecDataModel
from similarity import pearson
from sort import quick_sort


def user_cf(file_path, k=100, n=100):
    """
    Making recommendation via user_cf.
    :param k use for set the length of similar user set.
    :param n use for top-n rec, default is 10, while n equals -1 show all recommended result .
    """

    #Load data.
    data_model = RecDataModel(file_path)
    data_model.load_user_model()
    data_model.load_item_model()

    #Get similar user set.
    user_list = data_model.get_user_list()
    similarity_set = {}
    for i in user_list:
        tmp_set = {}
        for j in user_list:
            if i != j:
                a, b = data_model.get_corate(i, j)
                tmp_set[j] = pearson(a, b)
        users, similarity = quick_sort(tmp_set, r=True)
        tmp_set = {}
        for u in range(k):
            tmp_set[users[u]] = similarity[u]
        similarity_set[i] = tmp_set

    #make rec.
    rec = {}
    for u in similarity_set:
        rate_u = data_model.get_user_vec(u)
        rec_par = {}
        tmp_rec = {}
        tmp_set = similarity_set.get(u)
        for su in tmp_set:
            rate_su = data_model.get_user_vec(su)
            for item in rate_su:
                if item not in rate_u:
                    if item not in rec_par:
                        #su rate, su avg, similarity
                        param = [(rate_su.get(item), data_model.get_user_avg(su), tmp_set.get(su))]
                        rec_par[item] = param
                    else:
                        param = rec_par.get(item)
                        param.append((rate_su.get(item), data_model.get_user_avg(su), tmp_set.get(su)))
                        rec_par[item] = param

        for item in rec_par:
            avg_item = data_model.get_item_avg(item)
            fenzi = 0.0
            fenmu = 0.0
            for su_rate, avg_su, simi in rec_par.get(item):
                fenzi += (su_rate - avg_su) * simi
                fenmu += simi
            fenmu += 1
            tmp_rec[item] = avg_item + fenzi / fenmu

        items, pred = quick_sort(tmp_rec, r=True)
        tmp_rec = {}
        for i in range(n):
            tmp_rec[items[i]] = pred[i]
        rec[u] = tmp_rec
    return rec

__author__ = 'pok'
import sys

sys.path.append("../utility/")
from rec_data_model import RecDataModel
from similarity import pearson
from similarity import adjust_cos
from sort import quick_sort


def user_cf(file_path, k=100, n=-1):
    """
    Making recommendation via user_cf.
    :param k use for set the length of similar user set.
    :param n use for top-n rec, default is -1, while n equals -1 show all recommended result .
    """

    if n == 0:
        return {{}}

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
        rec_u = {}
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
            rec_u[item] = avg_item + fenzi / fenmu

        if n != -1:
            items, pred = quick_sort(rec_u, r=True)
            rec_u = {}
            for i in range(n):
                rec_u[items[i]] = pred[i]
        rec[u] = rec_u
    return rec


def item_cf(file_path, n=-1):
    """
    Making recommendation via item_cf.
    This function try to return a recommendation like:
    rec={
        user:{
            item:pred
        }
    }
    """

    if n == 0:
        return {{}}

    #load data
    data_model = RecDataModel(file_path)
    data_model.load_item_model()
    data_model.load_user_model()
    data_model.avg_item_model()
    item_list = data_model.get_item_list()

    #compute item similarity
    item_sim = {}
    for i in item_list:
        item_sim[i] = {}
    for i in range(len(item_list)):
        item_i = item_list[i]
        for j in range(i, len(item_list)):
            item_j = item_list[j]
            rate_i, rate_j = data_model.get_item_union(item_i, item_j)
            acos = adjust_cos(rate_i, rate_j)
            if i == j: acos = 0.0
            item_sim[item_i][item_j] = acos
            item_sim[item_j][item_i] = acos

    #make rec
    rec = {}
    user_list = data_model.get_user_list()
    for u in user_list:
        rec_u = {}
        rate_u = data_model.get_user_vec(u)
        for i in item_list:
            if i not in rate_u:
                i_sim = item_sim[i]
                fenzi = 0.0
                fenmu = 0.0
                for ui in rate_u:
                    fenzi += rate_u[ui] * i_sim[ui]
                    fenmu += i_sim[ui]
                if fenmu != 0:
                    rec_u[i] = fenzi / fenmu
                else:
                    rec_u[i] = 0.0
        if n != -1:
            items, pred = quick_sort(rec_u, r=True)
            rec_u = {}
            for i in range(n):
                rec_u[items[i]] = pred[i]
        rec[u] = rec_u
    return rec


def slope_one(file_path, n=-1):
    """
    Making recommendation via slope one.
    This function try to return a recommendation like:
    rec={
        user:{
            item:pred
        }
    }
    """

    #load data model
    data_model = RecDataModel(file_path)
    data_model.load_user_model()
    data_model.load_item_model()
    item_list = list(data_model.get_item_list())
    user_list = list(data_model.get_user_list())

    #compute dev(i,j)
    dev = {}
    tmp = {}
    for i in item_list:
        tmp[i] = (0.0, 0)
    for i in item_list:
        dev[i] = tmp
    for i in range(len(item_list)):
        rate_i = data_model.get_item_vec(item_list[i])
        if rate_i and len(rate_i) > 0:
            for j in range(i, len(item_list)):
                if i != j:
                    rate_j = data_model.get_item_vec(item_list[j])
                    if rate_j and len(rate_j) > 0:
                        dev_ij = 0.0
                        dev_count = 0
                        for iu in rate_i:
                            if iu in rate_j:
                                dev_ij += rate_i[iu] - rate_j[iu]
                                dev_count += 1
                        if dev_count > 0:
                            dev_ij /= dev_count
                            dev[item_list[i]][item_list[j]] = (dev_ij, dev_count)
                            dev[item_list[j]][item_list[i]] = (dev_ij, dev_count)

    #make rec
    rec = {}
    for u in user_list:
        print u
        rate_u = data_model.get_user_vec(u)
        rec_u = {}
        for i in item_list:
            if i not in rate_u:
                pred = 0.0
                count = 0.0
                i_dev = dev.get(i)
                for iu in rate_u:
                    dev_ij, dev_count = i_dev[iu]
                    pred += (rate_u.get(iu) - dev_ij) * dev_count
                    count += dev_count
                if count > 0:
                    rec_u[i] = pred / count
                else:
                    rec_u[i] = 0.0
        if n != -1:
            items, pred = quick_sort(rec_u, r=True)
            rec_u = {}
            for i in range(n):
                rec_u[items[i]] = pred[i]
        rec[u] = rec_u
    return rec
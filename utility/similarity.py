__author__ = 'pok'
import math


def pearson(coll_a, coll_b):
    """
    Compute the pearson coefficient of two list.
    :param coll_a:
    :param coll_b:
    """

    if len(coll_a) == 0 or len(coll_b) == 0:
        return 0.0
    elif len(coll_a) != len(coll_b):
        return 0.0
    else:
        ave_a = average(coll_a)
        ave_b = average(coll_b)
        a_b = 0.0
        a = 0.0
        b = 0.0
        for i in range(len(coll_b)):
            a_b += (coll_a[i] - ave_a) * (coll_b[i] - ave_b)
            a += math.pow(coll_a[i] - ave_a, 2.0)
            b += math.pow(coll_b[i] - ave_b, 2.0)
        return a_b / (math.sqrt(a) * math.sqrt(b) + 1)


def adjust_cos(coll_a, coll_b):
    """
    Compute the adjusted cosine of the collection.
    :param coll_a:
    :param coll_b:
    """

    return pearson(coll_a, coll_b)


def average(coll):
    """
    Compute the average of the list.
    :param coll:
    """

    if len(coll) > 0:
        return float(sum(coll)) / len(coll)
    else:
        return 0.0
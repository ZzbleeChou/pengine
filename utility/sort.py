__author__ = 'pok'


def _swap(array, a, b):
    """
        Swap two elements which indexes are a and b from array.
    """

    if len(array) and a != b:
        tmp = array[a]
        array[a] = array[b]
        array[b] = tmp


def _tran_collection(coll, key):
    """
        t=Transform the map/dict obj to an sortable list.
        If key equals 0, sorted at dict's keys,
        else if key equals 1 , sorted at dist's values.
    """

    keys = []
    array = []
    if type(coll) == list:
        array = coll[:]
    elif type(coll) == dict:
        if key == 1:
            array = list(coll.values())
            keys = list(coll)
        elif key == 0:
            keys = list(coll.values())
            array = list(coll)
    return keys, array


def bubble_sort(coll, key=1, r=False):
    """
        Sorting the array via bubble algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    _keys, _values = _tran_collection(coll, key)

    # ascending sort.
    if not r:
        for i in range(len(_values)):
            for j in range(len(_values) - i - 1):
                if _values[j] > _values[j + 1]:
                    _swap(_values, j, j + 1)
                    _swap(_keys, j, j + 1)
    #descending sort.
    else:
        for i in range(len(_values)):
            for j in range(len(_values) - i - 1):
                if _values[j] < _values[j + 1]:
                    _swap(_values, j, j + 1)
                    _swap(_keys, j, j + 1)
    if len(_keys) and key == 1:
        return _keys, _values
    elif len(_keys) and key == 0:
        return _values, _keys
    else:
        return _values


def select_sort(coll, key=1, r=False):
    """
        Sorting the array via selection algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    _keys, _values = _tran_collection(coll, key)

    # ascending sort.
    if not r:
        for i in range(len(_values)):
            _min = _values[i]
            _index = i
            for j in range(i + 1, len(_values)):
                if _min > _values[j]:
                    _min = _values[j]
                    _index = j
            _swap(_values, i, _index)
            _swap(_keys, i, _index)
    # descending sort.
    else:
        for i in range(len(_values)):
            _max = _values[i]
            _index = i
            for j in range(i + 1, len(_values)):
                if _max < _values[j]:
                    _max = _values[j]
                    _index = j
            _swap(_values, i, _index)
            _swap(_keys, i, _index)
    if len(_keys) and key == 1:
        return _keys, _values
    elif len(_keys) and key == 0:
        return _values, _keys
    else:
        return _values


def insert_sort(coll, key=1, r=False):
    """
        Sorting the array via insert algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    _keys, _values = _tran_collection(coll, key)

    # ascending sort.
    if not r:
        for i in range(len(_values)):
            for j in range(0, i):
                if _values[j] > _values[i]:
                    for k in range(i, j, -1):
                        _swap(_values, k, k - 1)
                        _swap(_keys, k, k - 1)
    # descending sort.
    else:
        for i in range(len(_values)):
            for j in range(0, i):
                if _values[j] < _values[i]:
                    for k in range(i, j, -1):
                        _swap(_values, k, k - 1)
                        _swap(_keys, k, k - 1)
    if len(_keys) and key == 1:
        return _keys, _values
    elif len(_keys) and key == 0:
        return _values, _keys
    else:
        return _values


def merge_sort(coll, key=1, r=False):
    """
        Sorting the array via merge algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    _keys, _values = _tran_collection(coll, key)

    # merge
    def _merge(s, e):
        if e - s == 1:
            return
        elif e == s:
            return
        else:
            mid = (s + e) / 2
            _merge(s, mid)
            _sort(s, mid)
            _merge(mid + 1, e)
            _sort(mid + 1, e)

    # sort
    def _sort(s, e):
        tmp_values = []
        tmp_keys = []
        mid = (s + e) / 2
        i = s
        j = mid + 1
        while i <= mid and j <= e:
            if not r:
                if _values[i] < _values[j]:
                    tmp_values.append(_values[i])
                    if len(_keys): tmp_keys.append(_keys[i])
                    i += 1
                else:
                    tmp_values.append(_values[j])
                    if len(_keys): tmp_keys.append(_keys[j])
                    j += 1
            else:
                if _values[i] > _values[j]:
                    tmp_values.append(_values[i])
                    if len(_keys): tmp_keys.append(_keys[i])
                    i += 1
                else:
                    tmp_values.append(_values[j])
                    if len(_keys): tmp_keys.append(_keys[j])
                    j += 1
        if i <= mid:
            for k in range(i, mid + 1):
                tmp_values.append(_values[k])
                if len(_keys): tmp_keys.append(_keys[k])
        if j <= e:
            for k in range(j, e + 1):
                tmp_values.append(_values[k])
                if len(_keys): tmp_keys.append(_keys[k])
        for i in range(s, e + 1):
            _values[i] = tmp_values[i - s]
            if len(_keys): _keys[i] = tmp_keys[i - s]

    if len(_values) > 0:
        _merge(0, len(_values) - 1)
        _sort(0, len(_values) - 1)
    if len(_keys) and key == 1:
        return _keys, _values
    elif len(_keys) and key == 0:
        return _values, _keys
    else:
        return _values


def quick_sort(coll, key=1, r=False):
    """
        Sorting the array via qucik sort algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    _keys, _values = _tran_collection(coll, key)

    #quick sort recursion function.
    def _quick_sort(b, e):
        if b >= e:
            return
        else:
            mid = _partition(b, e)
            _quick_sort(b, mid - 1)
            _quick_sort(mid + 1, e)

    #partition function.
    def _partition(b, e):
        _partition_value = _values[b]
        while b < e:
            if not r:
                while _partition_value <= _values[e] and b < e:
                    e -= 1
                _swap(_values, b, e)
                _swap(_keys, b, e)
                while _partition_value >= _values[b] and b < e:
                    b += 1
                _swap(_values, b, e)
                _swap(_keys, b, e)
            else:
                while _partition_value >= _values[e] and b < e:
                    e -= 1
                _swap(_values, b, e)
                _swap(_keys, b, e)
                while _partition_value <= _values[b] and b < e:
                    b += 1
                _swap(_values, b, e)
                _swap(_keys, b, e)
        return b

    _quick_sort(0, len(_values) - 1)
    if len(_keys) and key == 1:
        return _keys, _values
    elif len(_keys) and key == 0:
        return _values, _keys
    else:
        return _values


def unit_test():
    a1 = [1, 2, 3, 4, 5]
    a2 = [2, 3, 1, 5, 4]
    a3 = [5, 4, 3, 2, 1]
    a4 = [1, 1, 2, 2, 3]
    a5 = []
    a6 = [1, 5, 2, 3]
    d1 = {'a': '1', 'b': '2', 'c': '3'}
    d2 = {'c': 3, 'b': 2, 'a': 1}
    d3 = {}
    d4 = {'b': 2, 'c': 3, 'a': 1}
    d5 = {'a': 3, 'b': 2, 'c': 1}
    array = [a1, a2, a3, a4, a5, a6, d1, d2, d3, d4, d5]
    for i in array:
        print quick_sort(i)
        print quick_sort(i, r=True)


if __name__ == '__main__':
    unit_test()
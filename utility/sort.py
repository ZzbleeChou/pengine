__author__ = 'pok'


def swap(array, a, b):
    """
        Swap two elements which indexes are a and b from array.
    """

    if a != b:
        tmp = array[a]
        array[a] = array[b]
        array[b] = tmp


def bubble_sort(array, r=False):
    """
        Sorting the array via bubble algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    # ascending sort.
    if not r:
        for i in range(len(array)):
            for j in range(len(array) - i - 1):
                if array[j] > array[j + 1]:
                    swap(array, j, j + 1)
    #descending sort.
    else:
        for i in range(len(array)):
            for j in range(len(array) - i - 1):
                if array[j] < array[j + 1]:
                    swap(array, j, j + 1)
    return array


def select_sort(array, r=False):
    """
        Sorting the array via selection algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    # ascending sort.
    if not r:
        for i in range(len(array)):
            _min = array[i]
            _index = i
            for j in range(i + 1, len(array)):
                if _min > array[j]:
                    _min = array[j]
                    _index = j
            swap(array, i, _index)
    # descending sort.
    else:
        for i in range(len(array)):
            _max = array[i]
            _index = i
            for j in range(i + 1, len(array)):
                if _max < array[j]:
                    _max = array[j]
                    _index = j
            swap(array, i, _index)
    return array


def insert_sort(array, r=False):
    """
        Sorting the array via insert algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    # ascending sort.
    if not r:
        for i in range(len(array)):
            for j in range(0, i):
                if array[j] > array[i]:
                    for k in range(i, j, -1):
                        swap(array, k, k - 1)
    # descending sort.
    else:
        for i in range(len(array)):
            for j in range(0, i):
                if array[j] < array[i]:
                    for k in range(i, j, -1):
                        swap(array, k, k - 1)
    return array


def merge_sort(array, r=False):
    """
        Sorting the array via merge algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    # merge
    def merge(array, s, e):
        if e - s == 1:
            return
        elif e == s:
            return
        else:
            mid = (s + e) / 2
            merge(array, s, mid)
            sort(array, s, mid)
            merge(array, mid + 1, e)
            sort(array, mid + 1, e)

    # sort
    def sort(array, s, e):
        tmp = []
        mid = (s + e) / 2
        i = s
        j = mid + 1
        while i <= mid and j <= e:
            if not r:
                if array[i] < array[j]:
                    tmp.append(array[i])
                    i += 1
                else:
                    tmp.append(array[j])
                    j += 1
            else:
                if array[i] > array[j]:
                    tmp.append(array[i])
                    i += 1
                else:
                    tmp.append(array[j])
                    j += 1
        if i <= mid:
            for k in range(i, mid + 1):
                tmp.append(array[k])
        if j <= e:
            for k in range(j, e + 1):
                tmp.append(array[k])
        for i in range(s, e + 1):
            array[i] = tmp[i - s]

    if len(array) > 0:
        merge(array, 0, len(array) - 1)
        sort(array, 0, len(array) - 1)
    return array


def quick_sort(array, r=False):
    """
        Sorting the array via qucik sort algorithm.
        While r=FALSE, ascending sorted,
        else descending sorted.
    """

    #quick sort recursion function.
    def q(array, b, e):
        if b >= e:
            return
        else:
            mid = partition(array, b, e)
            q(array, b, mid - 1)
            q(array, mid + 1, e)

    #partition function.
    def partition(array, b, e):
        key = array[b]
        while b < e:
            if not r:
                while key <= array[e] and b < e:
                    e -= 1
                swap(array, b, e)
                while key >= array[b] and b < e:
                    b += 1
                swap(array, b, e)
            else:
                while key >= array[e] and b < e:
                    e -= 1
                swap(array, b, e)
                while key <= array[b] and b < e:
                    b += 1
                swap(array, b, e)
        return b

    q(array, 0, len(array) - 1)
    return array


def unit_test():
    a1 = [1, 2, 3, 4, 5]
    a2 = [2, 3, 1, 5, 4]
    a3 = [5, 4, 3, 2, 1]
    a4 = [1, 1, 2, 2, 3]
    a5 = []
    a6 = [1, 5, 2, 3]
    array = [a1, a2, a3, a4, a5, a6]
    for i in array:
        print merge_sort(i)
        print merge_sort(i, True)


if __name__ == '__main__':
    unit_test()
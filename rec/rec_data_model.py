__author__ = 'pok'


class RecDataModel:
    """
    A model for handling the training set.
    The Training should be a csv file.
    The form of the file should like:
        USER,ITEM,RATE (not nec)
        1,1,5(Example)
    This model can be use in both user_cf and item_cf.
    """

    __file_path = ''
    __user_model = {}
    __item_model = {}
    __avg_item_model = {}
    __user_list = []
    __item_list = []
    DEFAULT_RATE = '1.0'

    def __init__(self, file_path):
        """
        Initial the training set file path.
        """

        self.__file_path = file_path

    def load_user_model(self):
        """
        Load records and transform them into user model.
        user_model->{
            user:{
                item:rate
                }
        }
        """

        self.__user_model = self.__load_model(0)

    def load_item_model(self):
        """
        Load records and transform them into item model.
        item_model->{
            item:{
                user:rate
                }
        }
        """

        self.__item_model = self.__load_model(1)

    def __load_model(self, _type):
        """
        Load records.
        IF type equals 0, transform as user model,
        ELSE IF type equals 1, transform as item model.
        """

        _index = -1
        _sub_index = -1
        if _type == 0:
            _index = 0
            _sub_index = 1
        elif _type == 1:
            _index = 1
            _sub_index = 0
        tmp_model = {}
        tmp_user = []
        tmp_item = []
        f = open(self.__file_path, 'r')
        data = f.read().split('\n')
        for record in data:
            record = record.split(',')
            if len(record) < 2:
                continue
            if record[0] not in tmp_user:
                tmp_user.append(record[0])
            if record[1] not in tmp_item:
                tmp_item.append(record[1])
            if len(record) == 2:
                record.append(self.DEFAULT_RATE)
            if record[_index] in tmp_model:
                tmp_rate = tmp_model.get(record[_index])
                tmp_rate[record[_sub_index]] = float(record[2])
                tmp_model[record[_index]] = tmp_rate
            else:
                tmp_rate = {record[_sub_index]: float(record[2])}
                tmp_model[record[_index]] = tmp_rate
        self.__user_list = tmp_user
        self.__item_list = tmp_item
        return tmp_model

    def get_user_vec(self, user):
        """
        Get the vector on user model.
        """

        return self.__user_model.get(user)

    def get_item_union(self, item_a, item_b):
        """
        :return Two users' union rating set.
        """

        a = []
        b = []
        rate_a = self.get_avg_item_vec(item_a)
        rate_b = self.get_avg_item_vec(item_b)
        for key in rate_a:
            a.append(rate_a.get(key))
            if key not in rate_b:
                b.append(0.0)
            else:
                b.append(rate_b.get(key))
        for key in rate_b:
            if key not in rate_a:
                a.append(0.0)
                b.append(rate_b.get(key))
        return a, b

    def get_corate(self, user_a, user_b):
        """
        Get two users' co-rating item, and return two arrays.
        :return ([],[])
        """

        a = []
        b = []
        rate_a = self.get_user_vec(user_a)
        rate_b = self.get_user_vec(user_b)
        for key in rate_a:
            if key in rate_b:
                a.append(rate_a.get(key))
                b.append(rate_b.get(key))
        return a, b

    def get_user_list(self):
        """
        :return user list
        """

        return self.__user_list

    def get_item_list(self):
        """
        :return item list.
        """

        return self.__item_list

    def get_user_avg(self, user):
        """
        :return The average rating of the user.
        """

        rate = self.get_user_vec(user)
        if rate and len(rate) > 0:
            avg = 0.0
            for k in rate:
                avg += rate.get(k)
            return avg / len(rate)
        else:
            return 0.0

    def get_item_vec(self, item):
        """
        :return The vector of the item.
        """

        return self.__item_model.get(item)

    def get_avg_item_vec(self, item):
        """
        :return The vector of the item -ed avg.
        """

        return self.__avg_item_model.get(item)

    def get_item_avg(self, item):
        """
        :return The average of the item rating.
        """

        rate = self.get_item_vec(item)
        if rate and len(rate) > 0:
            avg = 0.0
            for k in rate:
                avg += rate.get(k)
            return avg / len(rate)
        else:
            return 0.0

    def avg_item_model(self):
        """
        Transform the item model to average item model.
        """

        user_avg = {}
        for u in self.__user_list:
            user_avg[u] = self.get_user_avg(u)
        for i in self.__item_model:
            tmp = self.__item_model.get(i)
            for u in tmp:
                tmp[u] = tmp[u] - user_avg[u]
            self.__avg_item_model[i] = tmp

    def get_user_avg(self, user):
        """
        :return The average of the item rating.
        """

        rate = self.get_user_vec(user)
        if rate and len(rate) > 0:
            avg = 0.0
            for k in rate:
                avg += rate.get(k)
            return avg / len(rate)
        else:
            return 0.0
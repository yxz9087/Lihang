# -*-coding:utf-8-*-
# Project: CH8  
# Filename: adaboost
# Author: 😏 <smirk dot cao at gmail dot com>

from sklearn.metrics import accuracy_score
import numpy as np


def clf_great_than_(x_, v_):
    """
    weak learner

    :param x_:
    :param v_: threshold
    :return: classify results
    """
    y_ = np.zeros(x_.size, dtype=int)
    y_[x_ > v_] = 1
    y_[x_ < v_] = -1
    return y_


def clf_less_than_(x_, v_):
    """

    :param x_:
    :param v_: threshold
    :return: classify results
    """
    y_ = np.zeros(x_.size, dtype=int)
    y_[x_ < v_] = 1
    y_[x_ > v_] = -1
    return y_


class BiSection(object):
    """
    threshold classifier
    error rate: $e_m=\sum_{i=1}^{N}P(G_m(x_i)\ne y_i)=\sum_{i=1}^{N}w_{mi}I(G_m(x_i)\ne y_i)$
    """
    def __init__(self, ):
        self.v_min = None
        self.f_min = None
        self.fs = []

    def fit(self, x_, y_, d_=None):
        if d_ is None:
            d_ = np.ones(x_.size) / x_.size
        v_start = min(x_) - 0.5
        v_end = max(x_) + 0.5
        threshold_lst = self.__gen_threshold_lst(v_start, v_end)

        # init
        err_min = np.inf
        v_min = v_start
        err_his_f = []

        # search
        for f in self.fs:
            err_his = []
            for v in threshold_lst:
                y_pred = f(x_, v)
                err = np.sum(d_[y_pred != y_])
                err_his.append((v, err))
                if err < err_min:
                    err_min = err
                    v_min = v
                    f_min = f
            err_his_f.append(err_his)
        self.f_min = f_min
        self.v_min = v_min
        return v_min, f_min, err_his_f

    def predict(self, x_):
        y_pred = self.f_min(x_, self.v_min)
        return y_pred

    def __gen_threshold_lst(self, start_, end_):
        # todo: update algo
        return np.arange(start_, end_, 1)


class AdaBoost(object):

    def __init__(self, ds, max_iter=10):
        self.ds_ = ds
        self.fs = []
        self.d_ = None
        self.max_iter_ = max_iter
        self.clfs_ = []

    def fit(self, x_, y_):
        self.d_ = np.ones(x_.size)/x_.size
        for m in range(self.max_iter_):
            clf = self.ds_()
            clf.fs = self.fs
            v, fv, err_his_f = clf.fit(x_, y_, d_=self.d_)
            # print(v, fv)
            G_ = clf.predict(x_)
            e_ = np.sum(self.d_[G_ != y_])
            e_ = np.round(e_, 4)
            alpha_ = np.log((1 - e_) / e_) / 2
            alpha_ = np.round(alpha_, 4)
            # print(alpha_, e_, self.d_)
            self.d_ = self.d_ * np.exp(-alpha_ * y_ * G_) / np.sum(self.d_ * np.exp(-alpha_ * y_ * G_))
            self.d_ = np.round(self.d_, 5)
            # f_ = alpha_ * clf.predict(x_)
            # f_ = np.round(f_, 4)
            # sign_f_ = np.sign(alpha_ * clf.predict(x_))
            self.clfs_.append((alpha_, clf))
            print(accuracy_score(self.predict(x_), y_))
            # alpha
            # res
            #

    def predict(self, x_):
        res = 0
        for clf in self.clfs_:
            res += clf[0]*clf[1].predict(x_)
            # print(id(clf), clf[0], clf[1].predict(x_))
        return np.sign(res)


if __name__ == '__main__':
    pass

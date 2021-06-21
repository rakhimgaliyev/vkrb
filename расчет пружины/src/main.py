# -*- coding: utf-8 -*-

import math
import random
import matplotlib.pyplot as plt

from config import Config
from spring import Spring
from data import array_of_delta_sp, array_of_i_p_sp


def print_smt(value, description="DATA"):
    print()
    print("------------------------" + description + "------------------------")
    print(value)
    print("------------------------" + description + "------------------------")
    print()


def show_n_tau_from_smth(all_springs, front, attr="L_szhat"):
    plt.xlabel("n_τ, коэффициент запаза", fontsize=12)

    ylabel = 'Lсж, длина пружины в сжатом состоянии'
    if attr == "delta_sp":
        ylabel = "Δ, диаметр проволоки"
    if attr == "d_sr_sp":
        ylabel = "d_ср, средний диаметр пружины"
    if attr == "i_p_sp":
        ylabel = "i_p, количество рабочих витков пружины"
    plt.ylabel(ylabel, fontsize=12)

    all_springs_x = [i.n_tau for i in all_springs]
    all_springs_y = [getattr(j, attr) for j in all_springs]
    plt.scatter(all_springs_x, all_springs_y)

    front_springs_x = [i.n_tau for i in front]
    front_springs_y = [getattr(j, attr) for j in front]
    plt.scatter(front_springs_x, front_springs_y, c="r")

    # выбранная пружина
    for spring in front:
        if math.fabs(spring.delta_sp - 5.384799999999999 / 1000) < 0.00001 and spring.i_p_sp == 6:
            front_springs_x = [spring.n_tau]
            front_springs_y = [getattr(spring, attr)]
            plt.scatter(front_springs_x, front_springs_y, c="black")


def show_front(all_springs, front):
    show_n_tau_from_smth(all_springs, front, attr="L_szhat")

def filter_front_by_d_sr(springs, d_sr=26/0.67):
    new_spring_arr = []
    for spring in springs:
        print(spring.d_sr_sp)
        if (spring.d_sr_sp < d_sr * 10 ** (-3)):
            new_spring_arr.append(spring)
    return new_spring_arr


if __name__ == "__main__":
    config = Config()

    springs = []
    for delta_sp in array_of_delta_sp:
        for i_p_sp in array_of_i_p_sp:
            spring = Spring(config, delta_sp, i_p_sp)
            if spring.is_spring_ok():
                springs.append(spring)
    springs = filter_front_by_d_sr(springs)
    front = []
    if len(springs) == 0:
        print("SPRING DO NOT FIT LIMITS")
        exit(0)

    # generate Pareto-front
    for spring in springs:
        not_dominating = True
        for front_elem in front:
            if spring.dominates_by_pareto(front_elem):
                print(front.index(front_elem))
                print(len(front))
                front = [x for x in front if not x.equals(front_elem)]
                print(len(front))
            if front_elem.dominates_by_pareto(spring):
                not_dominating = False
        if not_dominating and not spring.on_array(front):
            front.append(spring)

    for spring in springs:
        spring.d_sr_sp = spring.d_sr_sp * 0.67

    for spring in front:
        print(spring)

    print("ALL SPRINGS ARR LEN: ", len(springs))
    print("FRONT SPRINGS ARR LEN: ", len(front))

    show_front(springs, front)
    plt.figure()
    show_n_tau_from_smth(springs, front, "delta_sp")
    plt.figure()
    show_n_tau_from_smth(springs, front, "d_sr_sp")
    plt.figure()
    show_n_tau_from_smth(springs, front, "i_p_sp")
    plt.show()

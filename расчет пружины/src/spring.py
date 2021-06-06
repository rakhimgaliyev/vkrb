import math
import random


class Spring:
    def __init__(self, config, delta_sp, i_p_sp):
        self.config = config

        self.h_sp = config.h_sp
        self.k_sp = config.k_sp
        self.G_sp = config.G_sp
        self.n_p = config.n_p
        self.m_sp = config.m_sp
        self.ro_sp = config.ro_sp
        self.gap_sp = config.gap_sp
        self.i_0p_sp = config.i_0p_sp

        self.P_p = config.P_p
        self.f_sp = self.P_p / self.k_sp

        self.P_p0 = self.P_p * (self.f_sp - self.h_sp) / self.f_sp

        self.delta_sp = delta_sp
        self.i_p_sp = i_p_sp

        self.d_sr_sp = self._get_d_sr_sp()
        # c - индекс пружины
        self.c_sp = self.d_sr_sp / self.delta_sp

        #
        self.n_c_sp = self._get_n_c_sp()
        # высота пружины в свободном состоянии
        self.L_sv_sp = self._get_L_sv_sp()

        # Высота пружины в сжатом состоянии
        self.L_szhat = self.L_sv_sp - self.f_sp

        # Наибольшее напряжение кручения
        self.t_max = self._get_t_max()

        # Коэффициент запаса
        self.n_tau = self._get_n_tau()

    # Возвращает число рабочих витков пружины (8.55)
    def _get_d_sr_sp(self):
        return (
            self.f_sp
            * self.m_sp
            * self.G_sp
            * self.delta_sp ** 4
            / (8 * self.P_p * self.i_p_sp)
        ) ** (1 / 3)

    # Возвращает число собственных колебаний пружины (8.59)
    def _get_n_c_sp(self):
        return (
            9.55
            * self.delta_sp
            / (self.i_p_sp * self.d_sr_sp ** 2)
            * (self.m_sp * self.G_sp / (2 * self.ro_sp)) ** (1 / 2)
        )

    # Высота (длина) пружины в свободном состоянии (стр 333)
    def _get_L_sv_sp(self):
        return (
            (self.i_p_sp + self.i_0p_sp) * self.delta_sp
            + self.f_sp
            + self.i_p_sp * self.gap_sp
        )

    # t_max - Наибольшее напряжение кручения
    def _get_t_max(self):
        hi = 1 + 1.45 / self.c_sp
        return 8 * hi * self.d_sr_sp * self.P_p / (math.pi * self.delta_sp ** 3)

    # n_tau - коэффициент запаса
    def _get_n_tau(self):
        k_tau_sp = self.config.k_tau_sp
        e_p_tau_sp = self.config.e_p_tau_sp

        _lambda = 0.02e-3
        e_m_tau_sp = 0.5 + (1 - 0.5) * math.exp(-_lambda * self.delta_sp)

        return self.config.t_1_sp / (k_tau_sp / e_m_tau_sp / e_p_tau_sp * self.t_max)

    def is_spring_ok(self):
        if self._is_resonance_possible() or self.n_tau < 1.2:
            return False
        return True

    # Возвращает true, если возможен резонанс (8.59)
    def _is_resonance_possible(self):
        if (
            self.n_c_sp / self.n_p == int(self.n_c_sp / self.n_p)
            or self.n_c_sp / self.n_p < 8
        ):
            return True
        return False

    def dominates_by_pareto(self, other):
        if self.L_szhat < other.L_szhat and self.n_tau > other.n_tau:
            return True
        return False

    def equals(self, other):
        if (
            self.d_sr_sp == other.d_sr_sp
            and self.delta_sp == other.delta_sp
            and self.i_p_sp == other.i_p_sp
        ):
            return True
        return False

    def on_array(self, springs):
        for s in springs:
            if self.equals(s):
                return True
        return False

    def __str__(self):
        return (
            "Spring:\n\tP_p0 = {P_p0} H\n\tP_p = {P_p} H\n\tk_sp = {k_sp} H/m\n\t"
            "G_sp = {G_sp} Pa\n\tn_p = {n_p} rpm\n\td_sr = {d_sr_sp} mm\n\ti_p = {i_p_sp}"
            "\n\tdelta = {delta_sp} mm\n\tf_sp = {f_sp} mm\n\th_sp = {h_sp} mm\n\tro = {ro_sp} kg/m^3"
            "\n\tn_c_sp = {n_c_sp} rpm\n\tL_szhat = {L_szhat}\n\tn_tau = {n_tau} mm".format(
                P_p0=self.P_p0,
                P_p=self.P_p,
                k_sp=self.k_sp,
                G_sp=self.G_sp,
                n_p=self.n_p * 60,
                d_sr_sp=self.d_sr_sp * 1e3,
                i_p_sp=self.i_p_sp,
                delta_sp=self.delta_sp * 1e3,
                f_sp=self.f_sp * 1e3,
                h_sp=self.h_sp * 1e3,
                ro_sp=self.ro_sp,
                n_c_sp=self.n_c_sp * 60,
                L_szhat=self.L_szhat * 1e3,
                n_tau=self.n_tau,
            )
        )

    # def __str__(self):
    #     return (
    #         "Spring:"
    #         "\n\td_sr_sp = {d_sr_sp} mm\n\t"
    #         "L_szhat = {L_szhat}\n\t".format(
    #             d_sr_sp=self.d_sr_sp * 1e3,
    #             L_szhat=self.L_szhat * 1e3,
    #             n_tau=self.n_tau,
    #         )
    #     )

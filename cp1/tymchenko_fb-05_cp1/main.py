import math
import pandas as pd
import numpy as np
import re
class Class:
    def __init__(self,
                 n_f,
                 alf):
        self.n_f = n_f
        self.alf = alf
        self.text = self.\
            get_text()
    def get_freq_of_letters(self):
        d = {}
        for l in self.alf:d.update({l: 0})
        for i in self.text:d[i] += 1
        for l in self.alf:d.update({l: round(d[l] / len(self.text), 5)})
        return d
    def get_text(self):
        text = open(self.n_f, encoding='utf8').read().lower().replace('\n', '')
        text = re.sub(r'[^а-яё ]', '', text).replace(' ', '')
        open(self.n_f, encoding='utf8').close()
        return text
    def get_entropiy(self,
                     d):
        entropies = []
        for k in d.keys():
            if d[k] != 0:
                entropies.append(abs(float(d[k]) * math.log2(d[k]) / len(self.alf)))
        return sum(entropies)
    def get_calc_e(self,
                   e_value,
                   total_value):
        return 1 - (e_value /
                    math.log2(total_value))
    def get_freq_of_bigrams(self,alf, crs=True):
        d = {}
        for l1 in alf:
            for l2 in alf:
                d.update({l1 + l2: 0})
        if crs == True:
            for i in range(len(self.text) - 1):
                d[self.text[i] + self.text[i + 1]] += 1
            for key in d.keys():
                d[key] = round(d[key] / (len(self.text) - 1), 5)
        else:
            if len(self.text) % 2 == 1:self.text += "а"
            for i in range(len(self.text) - 1):
                if i % 2 == 1:continue
                d[self.text[i] + self.text[i + 1]] += 1
            for key in d.keys():
                d[key] = round(d[key] / (len(self.text) - 1), 5)
        return d
class Wb(Class):
    def print_data(self):
        t1 = self.\
            get_freq_of_letters()
        e_t1 = self.\
            get_entropiy(t1)
        print(f'H1={e_t1}\n'
              f'Надлишковість - {self.get_calc_e(e_t1, len(self.alf))}')
        t11 = self.get_freq_of_bigrams(self.alf, True)
        e_t11 = self.get_entropiy(t11)
        print(f'H2={e_t11}\n'
              f'Надлишковіть -  {self.get_calc_e(e_t11, len(self.alf))}')
        t12 = self.\
            get_freq_of_bigrams(self.alf, False)
        et12 = self.\
            get_entropiy(t12)
        print(f'H2={et12}\n'
              f'Надлишковість -{self.get_calc_e(et12, len(self.alf))}')
        return t1,t11,t12
class w_b(Class):
    def print_data(self):
        t2 = self.\
            get_freq_of_letters()
        e_t2 = self.\
            get_entropiy(t2)
        print(f'H1={e_t2}\n'
              f'Надлишковість - {self.get_calc_e(e_t2, len(self.alf))}')
        t21 = self.\
            get_freq_of_bigrams(self.alf,
                                True)
        e_t21 = self.\
            get_entropiy(t21)
        print(f'H2={e_t21}\n'
              f'Надлишковість -{self.get_calc_e(e_t21, len(self.alf))}')
        t22 = self.get_freq_of_bigrams(self.alf, False)
        et22 = self.get_entropiy(t22)
        print(f'H2-p = {et22}\n'
              f'Надлишковість - {self.get_calc_e(et22, len(self.alf))}')
        return t2, t21, t22

def save_results(fd, sd, td, fd1, sd_t_1, sd_t_2):
    pd.DataFrame(fd.values(), index=fd.keys()).to_excel('Частота букв.xlsx')
    time_verable = np.array(list(td.
                                 values()))
    pd.DataFrame(time_verable.reshape((34, 34)), index=fd.
                 keys(), columns=fd.
                 keys()).to_excel(
        'біграми.xlsx')
    time_verable = np.array(list(fd1.
                                 values()))
    pd.DataFrame(time_verable.reshape((34, 34)),
                 index=fd.keys(),
                 columns=fd.keys()).\
        to_excel(
        'перехресні-біграми.xlsx')
    pd.DataFrame(sd.values(),
                 index=sd.keys()).\
        to_excel('букви_без_пробілів.xlsx')
    v2 = np.array(list(sd_t_1.values()))
    pd.DataFrame(v2.reshape((33, 33)),
                 index=sd.keys(),
                 columns=sd.keys()).\
        to_excel('біграми без пробілів.xlsx')
    time_verable, k_test2 = np.array(list(sd_t_2.
                                          values())), pd.\
        DataFrame(v2.
                  reshape((33, 33)),
                                                                             index=sd.keys(),
                                                                             columns=sd.keys())
    k_test2.to_excel('перехресні-біграми без пробілів.xlsx')
if __name__ == '__main__':
    alf = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
    alf_with_prob = alf+' '
    with_prob = Wb('text.txt', alf_with_prob)
    t1, \
    t11, \
    t12 = with_prob.print_data()
    without_prob = w_b('text.txt', alf)
    t2, \
    t21, \
    t22 = without_prob.print_data()
    save_results(t1,
                 t2,
                 t11,
                 t12,
                 t21,
                 t22)
# Name: Tahseen Bin Taj

import doctest, datetime, numpy
import matplotlib.pyplot as plt

def date_diff(d1, d2):
    '''
    (str), (str) -> (int)
    Takes two datetime.date objects as inputs and finds the difference
    in days between them.
    >>> date_diff('2019-10-31', '2019-11-2')
    2
    '''
    d1 = str_to_date(d1)
    d2 = str_to_date(d2)
    return (d2 - d1).days


def get_age(d1, d2):
    '''
    (str), (str) -> (int)
    Takes two datetime.date objects as inputs and finds the age of the patient
    using it in years.
    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    '''
    a_year = 365.2425
    return int(date_diff(d1, d2)/a_year)

def str_to_date(d):
    '''
    (str) -> (datetime.date)
    Takes a string as an input and returns it in datetime.date format.
    >>> str_to_date('2019-11-2')
    datetime.date(2019, 11, 2)
    >>> str_to_date('2018-10-31')
    datetime.date(2018, 10, 31)
    '''
    d = d.split('-')
    date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    return date


def stage_three(input_filename, output_filename):
    """
    (str), (str) -> (dict)
    Takes two filenames as inputs and returns a dictionary with days in pandemic
    as keys and I, H, R as subkeys with their counts as values.
    >>> stage_three('stage2.tsv', 'stage3.tsv')
    {0: {'I': 1, 'D': 0, 'R': 0}, 1: {'I': 3, 'D': 0, 'R': 0}, \
2: {'I': 8, 'D': 0, 'R': 0}, 3: {'I': 20, 'D': 0, 'R': 0}, \
4: {'I': 47, 'D': 2, 'R': 0}, 5: {'I': 107, 'D': 11, 'R': 0}, \
6: {'I': 259, 'D': 20, 'R': 0}, 7: {'I': 621, 'D': 55, 'R': 1}, \
8: {'I': 1524, 'D': 113, 'R': 0}, 9: {'I': 197, 'D': 10, 'R': 1}}
    """
    in_file = open(input_filename, 'r', encoding = 'utf-8')
    out_file = open(output_filename, 'w', encoding = 'utf=8')
    count = 0
    ret = {}
    for line in in_file:
        edited = line.split('\t')
        if count == 0:
            i_date = edited[2]
        count += 1
        edited[2] = str(date_diff(i_date, edited[2]))
        edited[3] = str(get_age(edited[3], i_date))
        if edited[6][0].upper() in 'IDR':
            edited[6] = edited[6][0].upper()
        else:
            edited[6] = 'D'
        if int(edited[2]) not in ret:
            ret[int(edited[2])] = dict.fromkeys(['I', 'D', 'R'], 0)
        ret[int(edited[2])][edited[6]] += 1
        edited = '\t'.join(edited)
        out_file.write(edited)
    in_file.close()
    out_file.close()
    return ret

def plot_time_series(d):
    '''
    (dict) -> (list of lists)
    Takes a dictionary as input and returns a list of lists containing
    the count of I, D and R.
    '''
    ret_list = []
    for key in d:
        temp = []
        temp.append(d[key]['I'])
        temp.append(d[key]['R'])
        temp.append(d[key]['D'])
        ret_list.append(temp)
    plt.plot(ret_list)
    plt.legend(['Infected', 'Recovered', 'Dead'])
    plt.title('Time series of early pandemic, by Tahseen Bin Taj')
    plt.xlabel('Days into Pandemic')
    plt.ylabel('Number of People')
    plt.savefig('time_series.png')
    return ret_list
    
if __name__ == '__main__':
    doctest.testmod()

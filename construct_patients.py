# Name: Tahseen Bin Taj

import matplotlib.pyplot as plt
import doctest

Male = ['MALE', 'MAN', 'BOY', 'HOMME', 'H', 'M']
Female = ['FEMALE', 'WOMAN', 'GIRL', 'FEMME', 'F']
Valid = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "C", "F", ".", "°", " "]

def gender(s):
    """
    (str) -> (str)
    Returns either M, F or X for Male, Female or non-binary genders respectively.
    >>> gender('h')
    'M'
    >>> gender('nonbinary')
    'X'
    """
    s = s.upper()
    if s in Male:
        return 'M'
    elif s in Female:
        return 'F'
    else:
        return 'X'

def postal(s):
    """
    (str) -> (str)
    Returns a valid postal code or 000 given an arbitrary string as postal code.
    >>> postal('H2X 1B3')
    'H2X'
    >>> postal('N/A')
    '000'
    """
    if len(s) >= 3 and s[0] == 'H' and s[1].isdigit() and s[2].isalpha():
        return s[:3]
    return '000'

def temperature(t):
    """
    (str) -> (float)
    Given a string as an input for a temperature, if it is not a valid input, it
    returns 0.0. It returns the value as a float if the value is less than 45
    or else, if the value is greater than 45, it converts the value to
    fahrenheit and returns it.
    >>> temperature('123 F')
    50.56
    >>> temperature('44 C')
    44.0
    >>> temperature('na')
    0.0
    """
    temp = ''
    count = 0
    t = t.replace(',', '.').upper()
    for i in t:
        if i not in Valid or t == '0':
            return 0.0
        elif i in Valid:
            if i in 'C F°':
                continue
            else:
                temp += i
    if float(temp) > 45:
        temp = round((float(temp)-32)*(5/9), 2)
    return float(temp)

def temperatures_delimiter(l):
    """
    (list) -> (str)
    Given a list of floats, it returns a string which joins the elements in
    it by semicolons.
    >>> temperatures_delimiter([1.0, 2.0, 3.0])
    '1.0;2.0;3.0'
    """
    ret = ''
    for i, c in enumerate(l):
        if i+1 < len(l):
            ret += (str(c) + ";")
        else:
            ret += str(c)
    return ret

def nearest_five(i):
    """
    (int) -> (int)
    Given an integer as an input, it returns the value rounded to the nearest 5.
    >>> nearest_five(44)
    45
    >>> nearest_five(42)
    40
    """
    return 5 * round(i/5)

class Patient:
    """
    Represents a patient.
    Attributes: num (int), day_diagnosed (int), age (int), sex_gender (str)
                postal (str), state (str), temps (list), days_symptomatic (int)
    """
    def __init__(self, n, dd, a, sex, p, st, t, ds):
        self.num = int(n)
        self.day_diagnosed = int(dd)
        self.age = int(a)
        self.sex_gender = gender(sex)
        self.postal = postal(p)
        self.state = st
        self.temps = [temperature(t)]
        self.days_symptomatic = int(ds)
        
    def __str__(self):
        return '\t'.join([str(self.num), str(self.age), self.sex_gender, \
                          self.postal, str(self.day_diagnosed), self.state, \
                          self.days_symptomatic, temperatures_delimiter(self.temps)])
    
    def update(self, other):
        if self.num == other.num and self.sex_gender == other.sex_gender and\
           self.postal == other.postal:
            self.days_symptomatic = other.days_symptomatic
            self.state = other.state
            self.temps += other.temps
        else:
            raise AssertionError("num/sex_gender/postal are not the same")

def stage_four(input_filename, output_filename):
    """
    (str), (str) -> (dict)
    Given filenames as input, it writes the formatted patient info into the output
    file and returns a dictionary with keys being patient numbers and values being
    their respecting information.
    """
    in_file = open(input_filename, 'r', encoding = 'utf-8')
    out_file = open(output_filename, 'w', encoding = 'utf-8')
    ret = {}
    for line in in_file:
        l = line.replace('\n', '').split('\t')
        pat = Patient(l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8])
        if pat.num not in ret:
            ret[pat.num] = pat
        else:
            ret[pat.num].update(pat)
    for i in sorted(ret.keys()):
        out_file.write(str(ret[i]) + "\n")
    in_file.close()
    out_file.close()
    return ret

def fatality_by_age(d):
    """
    (dict) -> (list)
    Given a dictionary of patients as input, it graphs the probability of fatality
    by age against age and returns the probability of fatality in the ascending
    order of age.
    """
    age = {}
    probability_of_fatality = []
    for pat in d.values():
        if nearest_five(pat.age) not in age:
            age[nearest_five(pat.age)] = pat.state
        else:
            age[nearest_five(pat.age)] += pat.state
    for a in sorted(age):
        if (age[a].count('D')+age[a].count('R')) != 0:
            probability_of_fatality.append(age[a].count('D')/(age[a].count('D')+age[a].count('R')))
        else:
            probability_of_fatality.append(1.0)
    plt.plot(sorted(age.keys()), probability_of_fatality)
    plt.ylim((0, 1.2))
    plt.title('Probability of death vs age, by Tahseen Bin Taj')
    plt.ylabel('Deaths / (Deaths+Recoveries)')
    plt.xlabel('Age (to nearest 5)')
    plt.savefig('fatality_by_age.png')
    return probability_of_fatality

if __name__ == "__main__":
    doctest.testmod()

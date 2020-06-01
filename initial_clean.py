# Name: Tahseen Bin Taj

import doctest


def which_delimiter(s):
    '''
    (str) -> (str)
    Returns the most commonly used delimiter in the string
    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('0\\t1\\t2\\t3,4')
    '\\t'
    >>> which_delimiter('0_1_2_3')
    Traceback (most recent call last):
    AssertionError: It's not delimited by space or comma or tab.
    '''
    if ' ' in s or ',' in s or '\t' in s:
        space = s.count(' ')
        comma = s.count(',')
        tab = s.count('\t')
        if space > comma and space > tab:
            return ' '
        elif comma > space and comma > tab:
            return ','
        else:
            return '\t'
    else:
        raise AssertionError("It's not delimited by space or comma or tab.")


def stage_one(input_filename, output_filename):
    """
    (str), (str) -> (int)
    Takes two file names as input and returns the number of lines written to the output file.
    >>> stage_one('260913566.txt', 'stage1.tsv')
    3000
    """
    in_file = open(input_filename, 'r', encoding = 'utf-8')
    out_file = open(output_filename, 'w', encoding = 'utf-8')
    count = 0
    for line in in_file:
        edited = line.replace(which_delimiter(line), '\t')
        edited = edited.split('\t')
        edited[2] = edited[2].replace('/', '-').replace('.', '-')
        edited[3] = edited[3].replace('/', '-').replace('.', '-')
        edited = '\t'.join(edited).upper()
        out_file.write(edited)
        count += 1
    return count


def stage_two(input_filename, output_filename):
    """
    (str), (str) -> (int)
    Takes two filenames as inputs and returns the number of lines written to the output file.
    stage_two('stage1.tsv', 'stage2.tsv')
    3000
    """
    in_file = open(input_filename, 'r', encoding = 'utf-8')
    out_file = open(output_filename, 'w', encoding = 'utf-8')
    count = 0
    for line in in_file:
        edited = line.split('\t')
        count += 1
        while len(edited) != 9:
            # Check whether it is a temperature unit at the second last position or the second last
            # and the third last indexes of the list, edited store string type data.
            # If it is true for either, remove the second last string and add it to the third last
            # string separated by a space.
            if edited[-2].lower() in 'cf' or (edited[-2].isalpha() and edited[-3].isalpha()):
                edited[-2] = edited[-3] + " " + edited.pop(-2)            # Check whether the third last string index is a digit and the first character of
            # the second last string is a digit. If so, convert them into a decimal number.
            elif edited[-2][0].isdigit() and edited[-3].isdigit():
                edited[-2] = edited[-3] + "." + edited.pop(-2)            # If the string at index -4 is not alphabetic and either the string at index -5 is not alphabetic
            # or the strings from the index -6 to -3 is alphabetic, remove and add the string at index -4 to the
            # string at index -5 separated by a space.
            elif (not edited[-4].isalpha()) and (not edited[-5].isalpha()) or ''.join(edited[-6:-3]).isalpha():
                edited[-4] = edited[-5] + " " + edited.pop(-4)
        edited = '\t'.join(edited)
        out_file.write(edited)
    in_file.close()
    out_file.close()
    return count


if __name__ == '__main__':
    doctest.testmod()

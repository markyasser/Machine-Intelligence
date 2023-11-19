import utils


def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    # if string is empty return True
    if string == '':
        return True
    # Check if string is a palindrome
    if string[0] == string[-1]:
        return palindrome_check(string[1:-1])
    else:
        return False

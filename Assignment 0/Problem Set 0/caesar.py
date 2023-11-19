from typing import Tuple, List
from helpers.test_tools import read_text_file, read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
    This function takes the ciphered text (string) and the dictionary (a list of strings where each string is a word).
    It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary.
    '''
    best_deciphered_text = ''
    best_shift = 0
    best_num_not_in_dict = len(ciphered.split())

    dict_set = set(dictionary)

    for shift in range(1, 26):
        # Decipher the ciphered text using the current shift value
        deciphered_text = ''
        num_not_in_dict = 0
        for char in ciphered:
            if char != ' ':
                char = chr(ord('a') + (ord(char) - ord('a') - shift) % 26)
            deciphered_text += char

        # Count the number of words that are not in the dictionary
        num_not_in_dict = sum(
            1 for word in deciphered_text.split() if word not in dict_set)

        # Update the best deciphered text, shift value, and number of words not in the dictionary if the current deciphered text has fewer words not in the dictionary
        if num_not_in_dict < best_num_not_in_dict:
            best_deciphered_text = deciphered_text
            best_shift = shift
            best_num_not_in_dict = num_not_in_dict

    return (best_deciphered_text, best_shift, best_num_not_in_dict)

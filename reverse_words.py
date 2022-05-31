"""
Reverse a sentence's words without extra libraries or string methods
"""

import unittest
import string

def swap(i, j, collection):
    """Interchange the positions i and j in the collection"""
    collection[j], collection[i] = collection[i], collection[j]

def reverse_word(word, start, end):
    left = start
    right = end
    # Find the first whitespace or keep right to the end
    for x in range(start, end+1):
        if word[x] in string.whitespace:
            right = x - 1
            break
    while left < right:
        if word[right] not in string.whitespace:
            swap(left, right, word)
            left += 1
            right -= 1

def solution(characters):
    """ Modify the input characters, return nothing"""
    start = 0
    end = 0
    for char in characters:
        if char not in string.whitespace:
            end += 1
        else:
            # Found a word boundary
            reverse_word(characters, start, end - 1)
            # Initialize to the next word
            start = end + 1
            end += 1
    # Reverse the last word as well
    reverse_word(characters, start, end - 1)

class TestSolution(unittest.TestCase):
    
    def setUp(self):
        self.q_and_a = {
            "hello world": "olleh dlrow",
            "": "",
            "12345": "54321"
        }
    
    def test_solution(self):
        for item in self.q_and_a.items():
            print(item)
            # Character array
            question = list(item[0])
            # Solution is also an array
            answer = list(item[1])
            # Modify the question object inplace by calling solution
            solution(question)
            # Now for each mutated question, it must be equal to answer
            
            self.assertEqual(question, answer)

if __name__ == '__main__':
    unittest.main()

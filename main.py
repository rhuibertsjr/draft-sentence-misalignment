### main.py: Human Machine Interface - Sentence alignment                       -
##
## Authors: rhuibertsjr
## Date: 16 - 11 - 2023
#
import test

def levenshtein_distance(word1, word2):
    # Create a matrix to store the distances
    matrix = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    # Initialize the first row and column of the matrix
    for i in range(len(word1) + 1):
        matrix[i][0] = i
    for j in range(len(word2) + 1):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,         # deletion
                               matrix[i][j - 1] + 1,         # insertion
                               matrix[i - 1][j - 1] + cost)  # substitution

    # The bottom-right cell of the matrix contains the Levenshtein distance
    return matrix[len(word1)][len(word2)]


def sentence_align(reference, recognised, threshold=3):

    reference_words  = reference.split()
    recognised_words = recognised.split()

    # rhjr: results
    aligned_reference_words = reference_words
    aligned_recognised_words = recognised_words

    # rhjr: temporary results
    deletion = 0
    insertion = 0

    # rhjr: fix lengths
    while len(reference_words) > len(recognised_words):
        recognised_words.append("")

    for index, word in enumerate(reference_words):
        edit_distance = levenshtein_distance(word, recognised_words[index])

        # rhjr: check out of bounds
        if index + 1 < len(recognised_words):

            next_edit_distance = 0

            next_ref_edit_distance = levenshtein_distance(
                recognised_words[index + 1], recognised_words[index])

            next_rec_edit_distance = levenshtein_distance(
                word, recognised_words[index + 1])

            next_edit_distance = min(
                next_ref_edit_distance, next_rec_edit_distance)

        #end

        if edit_distance < next_edit_distance:
            #print(word, recognised_words[index], edit_distance)
            continue
        else:
            if index + 1 < len(recognised_words):
                if next_edit_distance >= threshold:
                    aligned_recognised_words.insert(index, "")
                    deletion += 1
                else:
                    aligned_reference_words.insert(index, "")
                    insertion += 1
                #end
            #end
        #end
    #end

    for index in range( len( aligned_recognised_words ) - 1, -1, -1):
        if aligned_recognised_words[index] == "":
            aligned_recognised_words.pop()  # rhjr: remove trailing words.
        else:
            break  
        #end
    #end

    return aligned_reference_words, aligned_recognised_words

#end sentence_align():

def tests_run():
    assert(len(test.reference) == len(test.recognised))

    for index, sentence in enumerate(test.reference):
        aligned_reference_words, aligned_recognised_words = sentence_align(
            sentence, test.recognised[index])

        print("Reference words:\t\t\t", aligned_reference_words)
        print("Aligned recognized words:\t", aligned_recognised_words)
        print()

#end tests_run():

tests_run()

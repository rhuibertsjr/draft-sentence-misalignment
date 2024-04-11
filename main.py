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

    # rhjr: temporary results
    deletion = 0
    insertion = 0

    # rhjr: fix lengths
    while len(reference_words) < len(recognised_words):
        reference_words.append('')
    while len(recognised_words) < len(reference_words):
        recognised_words.append('')

    for index, word in enumerate(reference_words):

        if (len(recognised_words) <= index):
            break

        edit_distance = levenshtein_distance(word, recognised_words[index])
        next_edit_distance = 0

        # rhjr: check out of bounds
        if index + 1 < len(recognised_words):

            if recognised_words[index] == "":
                continue

            next_ref_edit_distance = levenshtein_distance(
                recognised_words[index + 1], word)

            next_rec_edit_distance = levenshtein_distance(
                word, recognised_words[index + 1])

            # rhjr: move the better candidate
            next_edit_distance = min(
                next_ref_edit_distance, next_rec_edit_distance)

        #end

        if edit_distance < next_edit_distance:
            #print(word, recognised_words[index], edit_distance)
            continue
        else:
            if index + 1 < len(recognised_words):
                if next_edit_distance >= threshold:
                    recognised_words.insert(index, "")
                    deletion += 1
                else:
                    reference_words.insert(index, "")
                    insertion += 1
                    #end
                    #end
                    #end
                    #end

    remove_trailing_empty_words(reference_words)
    remove_trailing_empty_words(recognised_words)

    return reference_words, recognised_words

#end sentence_align():

def remove_trailing_empty_words(words):
    for index in range(len(words) - 1, -1, -1):
        if words[index] == "":
            words.pop()
        else:
            break
#end remove_trailing_empty_words():

def tests_run():
    assert(len(test.reference) == len(test.recognised))

    for index, sentence in enumerate(test.reference):
        aligned_reference_words, aligned_recognised_words = sentence_align(
            sentence, test.recognised[index])

        print("Reference words:\t\t\t\t\t", aligned_reference_words)
        print("Aligned recognized words:\t", aligned_recognised_words)
        print()

#end tests_run():

tests_run()

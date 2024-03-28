
reference = "The cat sat on the mat at the door"
recognized= "She rat the sat the mat at door aa"

reference_words = reference.split()
recognized_words = recognized.split()

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

print(reference)
print(recognized)

deletion = 0
insertion = 0

for i, rec_word in enumerate(reference_words):
    edit_distance = levenshtein_distance(rec_word, recognized_words[i])

    if i + 1 < len(recognized_words):
        edit_distance1 = levenshtein_distance(rec_word, recognized_words[i+1])

    if edit_distance < edit_distance1:
        print(rec_word, recognized_words[i], edit_distance)
    else:
        if i + 1 < len(recognized_words):

            if edit_distance1 >= 3:
                print(rec_word, recognized_words[i+1], edit_distance1)
                deletion += 1
            else:
                print(rec_word, recognized_words[i+1], edit_distance1)
                insertion += 1
                
    print()

print(deletion)
print(insertion)
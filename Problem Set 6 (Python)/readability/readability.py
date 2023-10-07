from cs50 import get_string

def main():
    text = get_string("Text: ")
    level = lexicon(text)

    if level < 16 and level > 1:
        print("Grade: "+ str(level))

    if level >= 16:
        print("Grade 16+")

    if level <= 1:
        print("Before Grade 1")

def lexicon(texty):

    n = len(texty)
    word_count = 1
    for i in range(0,n):
        if texty[i] == " ":
            word_count += 1

    letter_count = 0
    for x in range(0,n):
        if ord(texty[x]) <= 90 and ord(texty[x]) >= 65:
            letter_count += 1

        elif ord(texty[x]) <= 122 and ord(texty[x]) >= 97:
            letter_count += 1

    sentence_count = 0
    for y in range(0,n):

        if texty[y] == '.':
            sentence_count += 1

        if texty[y] == '!':
            sentence_count += 1

        if texty[y] == '?':
            sentence_count += 1

    L = float(letter_count) / float(word_count) * 100
    S = float(sentence_count) / float(word_count) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    indices = round(index)
    return indices


if __name__ == "__main__":
    main()



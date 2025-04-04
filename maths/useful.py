def find_trigrams(text):
    trigrams = {}
    for i in range(len(text) - 2):
        trigram = text[i : i + 3]
        if trigram in trigrams:
            trigrams[trigram].append(i)
        else:
            trigrams[trigram] = [i]

    multiple_trigrams = {
        key: value for key, value in trigrams.items() if len(value) > 1
    }
    for key in multiple_trigrams:
        multiple_trigrams[key] = [
            multiple_trigrams[key][i + 1] - multiple_trigrams[key][i]
            for i in range(len(multiple_trigrams[key]) - 1)
        ]
    return multiple_trigrams


def find_ngram(text, n):
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i : i + n]
        if ngram in ngrams:
            ngrams[ngram].append(i)
        else:
            ngrams[ngram] = [i]

    multiple_ngrams = {
        key: [
            ngrams[key][i + 1] - ngrams[key][i]
            for i in range(len(ngrams[key]) - 1)
        ] for key, value in ngrams.items() if len(value) > 1
    }
    return multiple_ngrams

print(find_trigrams("bondedejjcdkxDEMbonxxxdekosjqnxxxbonhallobon"))
print(find_ngram("bondedejjcdkxDEMbonxxxdekosjqnxxxbonhallobon", 3))

alphabet = "abcdefghijklmnopqrstuvwxyz"
ord_a = ord("a")
ord_e = ord("e")

IC_fr = 0.07

# Notre Dame de Paris
frequence_apparition_ndp = {
    "a": 8.46,
    "b": 1.02,
    "c": 3.21,
    "d": 3.78,
    "e": 17.6,
    "f": 1.11,
    "g": 1.12,
    "h": 1.07,
    "i": 7.4,
    "j": 0.48,
    "k": 0.0,
    "l": 6.05,
    "m": 2.7,
    "n": 6.38,
    "o": 5.19,
    "p": 2.68,
    "q": 1.21,
    "r": 6.56,
    "s": 7.56,
    "t": 7.26,
    "u": 6.63,
    "v": 1.65,
    "w": 0.0,
    "x": 0.03,
    "y": 0.03,
    "z": 0.01,
}

def striper(text):
    special_caracters = [" ", "\n", "\t", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"', "-"]
    for car in special_caracters:
        text = text.replace(car, "")
    return text.lower()


def get_frequences(text):
    frequence = {}
    for letter in text:
        if letter in frequence:
            frequence[letter] += 1
        else:
            frequence[letter] = 1
    return {k: v for k, v in sorted(frequence.items(), key=lambda item: item[1], reverse=True)}


# Indice de coïncidence mutuelle
def MIC(text_1, text_2):
    mic_text = 0
    n_1 = len(text_1)
    n_2 = len(text_2)
    for letter in alphabet:
        n_1_i = text_1.count(letter)
        n_2_i = text_2.count(letter)
        mic_text += n_1_i * n_2_i
    mic_text /= n_1 * n_2
    return mic_text


# Indice de coïncidence
def IC(text):
    ic_text = 0
    n = len(text)
    for letter in alphabet:
        n_i = text.count(letter)
        ic_text += n_i * (n_i - 1)
    ic_text /= n * (n - 1)

    return ic_text

def find_ngrams_distances(text, n):
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i : i + n]
        if ngram in ngrams:
            ngrams[ngram].append(i)
        else:
            ngrams[ngram] = [i]
            
    multiple_ngrams = {
        key: [ngrams[key][i + 1] - ngrams[key][i] for i in range(len(ngrams[key]) - 1)]
        for key, value in ngrams.items()
        if len(value) > 1
    }

    distances = []
    for value in multiple_ngrams.values():
        distances += value

    distances.sort()
    return distances

def find_ngrams_frequences(text, n=2):
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i : i + n]
        if ngram in ngrams:
            ngrams[ngram]+=1
        else:
            ngrams[ngram] = 1
    return {k: v for k, v in sorted(ngrams.items(), key=lambda item: item[1], reverse=True)}
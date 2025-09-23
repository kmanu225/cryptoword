LATIN_ALPHABET = "".join([chr(ord("a") + i) for i in range(26)])

ORD_LOWER_A = ord("a")
ORD_LOWER_E = ord("e")

IC_FR = 0.07

# Notre Dame de Paris
NOTRE_DAME_PARIS_FREQUENCIES = {
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
    special_caracters = [
        " ",
        "\n",
        "\t",
        ".",
        ",",
        ";",
        ":",
        "!",
        "?",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "'",
        '"',
        "-",
    ]
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
    return {
        k: v
        for k, v in sorted(frequence.items(), key=lambda item: item[1], reverse=True)
    }

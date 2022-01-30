from io import TextIOWrapper
import pandas as pd
import numpy as np
import json

alphabet = "abcdefghijklmnopqrstuvwxyz"
with open("src/data/generator/generative.json", "r") as f:
    data = json.load(f)

def main(cases):
    goods = []
    bads = []

    for _ in range(cases):
        goods.extend(good())
        bads.extend(bad())

    sentences = goods + bads
    states = [2 for _ in goods] + [0 for _ in goods]

    pd.DataFrame(list(zip(sentences, states)), columns=("sentence", "state")).to_csv("src/data/generator/generated.csv", index=False)

def mistake(text):
    text = list(text)
    for i, letter in enumerate(text):
        if not np.random.choice(45):
            text[i]

        if not np.random.choice(35):
            text.insert(i, alphabet[np.random.choice(26)])

    return "".join(text)

def rand_cap(text):
    text = list(text)
    for i, letter in enumerate(text):
        if not np.random.choice(45):
            text[i] = text[i].upper()

    return "".join(text)

def good():
    phrases = []
    text = []
    length = np.random.choice(3) + 1

    for _ in range(length):
        if not np.random.choice(8):
            i = np.random.choice(len(data["words"]["good"]))
            text.append(data["words"]["good"][i])

        else:
            i = np.random.choice(len(data["phrases"]["good"]))
            text.append(data["phrases"]["good"][i])

    i = np.random.choice(len(data["banana"]))
    text.append(data["banana"][i])


    for _ in range(length // 2):
        np.random.shuffle(text)
        phrase = " ".join(text)
        phrases.append(phrase.strip())

    return phrases

def bad():
    phrases = []
    text = []
    length = np.random.choice(4) + 1

    for _ in range(length):
        if not np.random.choice(8):
            i = np.random.choice(len(data["words"]["bad"]))
            text.append(data["words"]["bad"][i])

        else:
            i = np.random.choice(len(data["phrases"]["bad"]))
            text.append(data["phrases"]["bad"][i])

    i = np.random.choice(len(data["banana"]))
    text.append(data["banana"][i])

    for _ in range(length // 2):
        np.random.shuffle(text)
        phrase = " ".join(text)
        phrases.append(phrase.strip())

    return phrases

if __name__ == '__main__':
    main(200)
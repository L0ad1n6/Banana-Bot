from io import TextIOWrapper
import pandas as pd
import numpy as np
import json

alphabet = "abcdefghijklmnopqrstuvwxyz"
with open("src/data/generative.json", "r") as f:
    data = json.load(f)

def main(cases):
    goods = []
    bads = []

    for _ in range(cases):
        goods_ = good()
        bads_ = bad()

        goods_ = map(mistake, goods_)
        goods_ = map(rand_cap, goods_)

        bads_ = map(mistake, bads_)
        bads_ = map(mistake, bads_)

        goods.extend(goods_)
        bads.extend(bads_)

    pd.DataFrame(list(zip(sentences, states)), columns=("sentence", "state")).to_csv("src/data/datset.csv", index=False)

def mistake(text):
    text = list(text)
    for i, letter in enumerate(text):
        if not np.random.choice(4):
            text[i]

        if not np.random.choice(4):
            text.insert(i, alphabet[np.random.choice(26)])

    return "".join(text)

def rand_cap(text):
    text = list(text)
    for i, letter in enumerate(text):
        if not np.random.choice(4):
            text[i] = text[i].upper()

    return "".join(text)

def good():
    phrases = []
    text = []
    length = np.random.choice(4) + 1
    status = "bad" if np.random.choice(2) else "good" 

    for _ in range(length):
        if not np.random.choice(6):
            i = np.random.choice(len(data["words"][status]))
            text.append(data["words"][status])

        else:
            i = np.random.choice(len(data["phrases"][status]))
            text.append(data["phrases"][status])

    i = np.random.choice(len(data["banana"]))
    text.append(data["banana"][i])

    if status == "bad":
        i = np.random.choice(len(data["negations"]))
        text.append(data["negations"][i])

    for _ in range(length // 2):
        np.random.shuffle(text)
        phrases.append(" ".join(text).strip())

    return phrases

    




def bad():
    return

def neutral():
    return

if __name__ == '__main__':
    main()
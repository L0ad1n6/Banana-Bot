import pandas as pd

def b10(string):
    string = list(filter(str.isalnum, string.lower()))
    return int("1"+("".join([str(ord(char)).zfill(3) for char in string])))

def main():
    df = pd.read_csv("src/data/raw_dataset.csv")
    sentences = df.iloc[:, 0].values
    sentences = map(b10, sentences)

    states = df.iloc[:, 1].values

    pd.DataFrame(list(zip(sentences, states)), columns=("sentence", "state")).to_csv("src/data/datset.csv", index=False)
    
if __name__ == "__main__":
    main()
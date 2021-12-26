from typing import DefaultDict
import pandas as pd
import numpy as np
from model import model
from dataset import b10
import lightgbm as lgb
from sklearn.model_selection import train_test_split

def main():
    df = pd.read_csv("/Users/altan/Programming/Projects/Banana Bot/src/data/dataset.csv")
    x = df.iloc[:, 0:-1].values
    y = df.iloc[:, -1].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    d_train = lgb.Dataset(x_train, label=y_train)
    d_test = lgb.Dataset(x_test, label=y_test)

    params = {
        "learning_rate": 0.05,
        "num_leaves": 100,
        "boosting_type": "dart",
        "objective": "multiclassova",
        "metric": "multi_logloss",
        "num_class": 3,
        "force_col_wise": True,
        # "is_unbalance": True
    }

    model = lgb.train(params, d_train, 10000, valid_sets=[d_test])
    model.save_model("/Users/altan/Programming/Projects/Banana Bot/src/data/model.txt", num_iteration=model.best_iteration)

    # while True:
    #     text = input("Enter message: ")
    #     inp = np.array(b10(text)).reshape((1, 1))
    #     prediction = list(model.predict(inp))
    #     i = prediction.index(max(prediction))
    #     status = "good" if i == 2 else "neutral" if i == 1 else "bad"
    #     print(f"Predcition: {status} ({prediction[i]})")

if __name__ == "__main__":
    main()
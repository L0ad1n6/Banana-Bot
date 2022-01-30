import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import numpy as np
from dataset import b10
import seaborn as sns
from threading import Thread

def main():
    df = pd.read_csv("src/data/dataset/dataset.csv")
    x = df.iloc[:, 0:-1].values
    y = df.iloc[:, -1].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

    d_train = lgb.Dataset(x_train, label=y_train)
    d_test = lgb.Dataset(x_test, label=y_test)

    params = {
        "learning_rate": 0.07,
        "num_leaves": 100,
        "boosting_type": "dart",
        "objective": "multiclassova",
        "metric": "multi_logloss",
        "num_class": 3,
        "force_col_wise": True,
        # "is_unbalance": True
    }

    model = lgb.train(params, d_train, 10000, valid_sets=[d_test])
    model.save_model("src/data/model/model.txt", num_iteration=model.best_iteration)

    prediction = model.predict(x_test)
    adj = []
    for pred in prediction:
        adj.append(np.argmax(pred, axis=0))

    cm = confusion_matrix(y_test, adj)
    sns.heatmap(cm, annot=True)

    Thread(target=plt.show).start()

    while True:
        text = input("Enter message: ")
        inp = np.array(b10(text)).reshape((1, 1))
        prediction = list(model.predict(inp))
        i = list(prediction[0]).index(max(prediction[0]))
        status = "good" if i == 2 else "neutral" if i == 1 else "bad"
        print(f"Predcition: {status} ({prediction[0]})")

if __name__ == "__main__":
    main()
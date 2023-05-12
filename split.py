import pandas as pd

df = pd.read_csv("all.csv")

df["id"] = df["id"].apply(lambda x : "audio/"+x+".wav")

train=df.sample(frac=0.8,random_state=200)
rest=df.drop(train.index)
test=rest.sample(frac=0.5, random_state=200)
valid=rest.drop(test.index)


train.to_csv("train.csv", index=False)
valid.to_csv("valid.csv", index=False)
test.to_csv("test.csv", index=False)

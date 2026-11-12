import pandas as pd

none_results = pd.read_csv("none_results.txt", sep=" ", header=None, names=["graph", "none"])
few_results = pd.read_csv("few.txt", sep=" ", header=None, names=["graph", "none"])
alternate_results = pd.read_csv("alternate_results.txt", sep=" ", header=None, names=["graph", "none"])
many_results = pd.read_csv("many_results.txt", sep=" ", header=None, names=["graph", "none"])
#some_results = pd.read_csv("some_results.txt", sep=" ", header=None, names=["graph", "some"])

df = (alternate_results.rename(columns={"none": "A"})
      .merge(few_results.rename(columns={"none": "F"}), on="graph")
      .merge(many_results.rename(columns={"none": "M"}), on="graph")
      .merge(none_results.rename(columns={"none": "N"}), on="graph")
      #.merge(some_results.rename(columns={"none": "S"}), on="graph")
      )


# n is the first number in the first line of the graph file (read only)
df["n"] = df["graph"].map(lambda name: int(open(f"../../data/{name}.txt").readline().split()[0]))

df = df[["graph", "n", "A", "F", "M", "N"]]

df.to_csv("results.csv", index=False)
#df.to_csv("results2.csv", sep=" ", index=False) 

import pandas as pd


def read_results(path, col):
    """Read '<graph> <answer> <time>' lines, keep graph + answer, drop the TOTAL line."""
    df = pd.read_csv(path, sep=" ", header=None, usecols=[0, 1],
                     names=["graph", col], dtype=str)
    return df[df["graph"] != "TOTAL"]


none_results = read_results("none_results.txt", "N")
few_results = read_results("few_results.txt", "F")
alternate_results = read_results("alternate_results.txt", "A")
many_results = read_results("many_results.txt", "M")
some_results = read_results("some_results.txt", "S")

df = (alternate_results
      .merge(few_results, on="graph", how="outer")
      .merge(many_results, on="graph", how="outer")
      .merge(none_results, on="graph", how="outer")
      .merge(some_results, on="graph", how="outer")
      )

df["n"] = df["graph"].map(lambda name: int(open(f"../../data/{name}.txt").readline().split()[0]))

cols = ["A", "F", "M", "N", "S"]
df = df[["graph", "n"] + cols].sort_values("n")

with open("results.txt", "w") as f:
    df.to_csv(f, index=False)

# ---------- LaTeX table ----------
def fmt(v):
    if pd.isna(v):
        return "--"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)

def esc(s):
    return str(s).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")

lines = [
    r"\begin{longtable}{l" + "r" * (1 + len(cols)) + "}",
    r"  \toprule",
    "  Instance name & $n$ & " + " & ".join(cols) + r" \\",
    r"  \midrule",
    r"  \endfirsthead",
    r"  \toprule",
    "  Instance name & $n$ & " + " & ".join(cols) + r" \\",
    r"  \midrule",
    r"  \endhead",
    r"  \midrule",
    r"  \multicolumn{" + str(2 + len(cols)) + r"}{r}{\emph{continued on next page}} \\",
    r"  \endfoot",
    r"  \bottomrule",
    r"  \endlastfoot",
]
for _, row in df.iterrows():
    cells = [esc(row["graph"]), f"{row['n']:,}"] + [fmt(row[c]) for c in cols]
    lines.append("  " + " & ".join(cells) + r" \\")
lines.append(r"\end{longtable}")

table = "\n".join(lines)
print(table)
with open("results_table.tex", "w") as f:
    f.write(table)
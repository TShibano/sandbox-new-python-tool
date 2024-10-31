# gen_sample_data.py
# sampleデータを生成するPythonコード

# %% library
import random
import polars as pl

# %%
random.seed(42)

# %%
# data1:  
# data2:
# data3:

def gen_data1(n: int) -> pl.DataFrame:
    ids = list(range(1, n+1, 1))
    grp1 = random.choices(["A", "B", "C"], weights=[3, 2, 1], k=n)
    grp2 = random.choices(["X", "Y", "Z"], weights=[3, 2, 1], k=n)
    val = [random.normalvariate(0, 1) for _ in range(n)]
    data = pl.DataFrame({"id": ids, "group1": grp1, "group2": grp2, "value": val})
    return data

def gen_data2(n: int, id_start) -> pl.DataFrame:
    ids = list(range(id_start+1, id_start+n+1, 1))
    grp1 = random.choices(["A", "B", "C"], weights=[3, 2, 1], k=n)
    grp2 = random.choices(["X", "Y", "Z"], weights=[3, 2, 1], k=n)
    val = [random.normalvariate(0, 1) for _ in range(n)]
    data = pl.DataFrame({"id": ids, "group1": grp1, "group2": grp2, "value": val})
    return data


def gen_data_grp_weight() -> pl.DataFrame:
    grp1 = ["A"] * 3 + ["B"] * 3 + ["C"] * 3
    grp2 = ["A", "B", "C"] * 3
    weight = [random.randint(1, 9) for _ in range(9)]
    data = pl.DataFrame({"group1": grp1, "group2": grp2, "weight": weight})
    return data

# %% main
def main():
    n_data1 = 1_000_000
    n_data2 = 500_000
    data1 = gen_data1(n_data1)
    data2 = gen_data2(n_data2, n_data1)
    weight_data = gen_data_grp_weight()
    data1.write_csv("./sample_data/data1.csv")
    data2.write_csv("./sample_data/data2.csv")
    weight_data.write_excel("./sample_data/weight_data.xlsx")

main()
# gen_sample_data.csv
# %% ライブラリ
import random
import polars as pl

# %%
random.seed(42)
# %% データの生成
# 日本人の血液型(ABOの遺伝子型とRh型)を例にサンプルデータを作成する
n_sample = 100_000
ids = range(1, n_sample + 1)
abo_type_list = random.choices(
    ["AA", "AO", "BB", "BO", "AB", "OO"], weights=[10, 30, 5, 15, 10, 30], k=n_sample
)
rh_type_list = random.choices(["Rh+", "Rh-"], weights=[99, 1], k=n_sample)
val1_list = [random.normalvariate(0, 1) for _ in range(n_sample)]
val2_list = [random.randint(1, 9) for _ in range(n_sample)]

# %%
blood_df = pl.DataFrame(
    {
        "id": ids,
        "abo": abo_type_list,
        "rh": rh_type_list,
        "val1": val1_list,
        "val2": val2_list,
    }
)
# %%
blood_df.write_csv("./sample_data/blood_data.csv")

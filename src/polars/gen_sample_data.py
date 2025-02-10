# gen_sample_data.csv
# %% ライブラリ
import random
import polars as pl

# %%
random.seed(42)
# %% データの生成
# 日本人の血液型(ABOの遺伝子型とRh型)を例にサンプルデータを作成する
def gen_blood_data(n: int, save_dir: str) -> None:
    ids = range(1, n+ 1)
    abo_type_list = random.choices(
        ["AA", "AO", "BB", "BO", "AB", "OO"], weights=[10, 30, 5, 15, 10, 30], k=n
    )
    rh_type_list = random.choices(["Rh+", "Rh-", None], weights=[500, 5, 1], k=n)
    val1_list = [random.normalvariate(0, 1) for _ in range(n)]
    val2_list = [random.randint(1, 9) for _ in range(n)]
    blood_df = pl.DataFrame(
        {
            "ID": ids,
            "ABO": abo_type_list,
            "RH": rh_type_list,
            "VAL1": val1_list,
            "VAL2": val2_list,
        }
    )
    blood_df.write_csv(save_dir+"/blood_data.csv")
    # 重みデータは適当に作成
    weight_df = pl.DataFrame(
        {
            "ABO": ["AA", "AO", "BB", "BO", "AB", "OO"],
            "WEIGHT": [1, 2, 3, 4, 5, 6],
        }
    )
    weight_df.write_csv(save_dir+"/blood_data_weight.csv")

# %% 
def gen_data1(n: int, save_dir: str) -> pl.DataFrame:
    ids = list(range(1, n + 1, 1))
    grp1 = random.choices(["A", "B", "C"], weights=[1, 1, 1], k=n)
    grp2 = random.choices(["D", "E", "F"], weights=[1, 1, 1], k=n)
    grp3 = random.choices(["X", "Y", "Z", None], weights=[10, 10, 10, 1], k=n)
    val1 = [random.normalvariate(0, 1) for _ in range(n)]
    val2 = [random.normalvariate(0, 1) for _ in range(n)]
    val3 = [random.normalvariate(0, 1) for _ in range(n)]
    val4 = [random.normalvariate(0, 1) for _ in range(n)]
    val5 = [random.normalvariate(0, 1) for _ in range(n)]
    val6 = [random.normalvariate(0, 1) for _ in range(n)]
    data = pl.DataFrame(
        {
            "ID": ids,
            "GROUP1": grp1,
            "GROUP2": grp2,
            "GROUP3": grp3,
            "VALUE1": val1,
            "VALUE2": val2,
            "VALUE3": val3,
            "VALUE4": val4,
            "VALUE5": val5,
            "VALUE6": val6,
        }
    )
    data.write_csv(save_dir+"/data1.csv")
    # 重みデータは適当に作成
    weight_df = pl.DataFrame(
        {
            "GROUP1": ["A", "A", "A", "B", "B", "B", "C", "C", "C"],
            "GROUP2": ["D", "E", "F", "D", "E", "F", "D", "E", "F"],
            "WEIGHT": [1, 2, 3, 4, 5, 6, 7, 8, 9,]
            }
    )
    weight_df.write_csv(save_dir + "/data1_weight.csv")


# %% main
def main():
    n_blood = 100_000
    gen_blood_data(n_blood, save_dir="./sample_data")
    n_data1 = 1_000_00
    gen_data1(n_data1, save_dir="./sample_data")

main()
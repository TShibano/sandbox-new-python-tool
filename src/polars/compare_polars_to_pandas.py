# compare_polars_to_pandas.py
# Created by ctirus
# Date: 2025/02/09

# %% ----------------------------
# ---- Abstract
# * polars と pandas の速度パフォーマンスを比較する
# * 結論: 
# ** polars は pandas よりも，高速かほぼ同等の速度である
# ** 特に，データの読み込みでは，polars が　pandas よりも非常に高速であ
# * 比較項目
# ** データの読み込み速度
# ** データのフィルタリング速度
# ** データの列追加速度
# ** データのグルーピング速度
# ** データの結合速度
# * データについて
# ** data1.csv: 100万行 x 10列のデータ
# ** 1列目: int64
# ** 2-4列目: str
# ** 5-10列目: float64
# -------------------------------


# %% ----------------------------
# ---- Library
# -------------------------------
import time
import pandas as pd
import polars as pl

# 計測結果を格納するリスト
results = []

# %% ----------------------------
# ---- CSVデータの読み込み速度を比較
# -------------------------------
# Read data with Polars
start_time = time.time()
df_polars = pl.read_csv("./sample_data/data1.csv")
polars_duration = time.time() - start_time
print(f"Polars read duration: {polars_duration:.4f} seconds")
results.append(["Read CSV", polars_duration, None])

# Read data with Pandas
start_time = time.time()
df_pandas = pd.read_csv("./sample_data/data1.csv")
pandas_duration = time.time() - start_time
print(f"Pandas read duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% 後にデータの結合を行うためのデータ　
df_polars_weight = pl.read_csv("./sample_data/data1_weight.csv")
df_pandas_weight = pd.read_csv("./sample_data/data1_weight.csv")

# %% ----------------------------
# ---- データのフィルタリング速度を比較
# * str列のフィルタリング
# * float列のフィルタリング
# * 欠損行のフィルタリング
# -------------------------------
# 1. "group1" 列の値が "A" である行を抽出する
print("filtering string column")
start_time = time.time()
polars_filtered_group1 = df_polars.filter(pl.col("GROUP1") == "A")
polars_duration = time.time() - start_time
print(f"Polars filter group1 duration: {polars_duration:.4f} seconds")
results.append(["Filter group1", polars_duration, None])

start_time = time.time()
pandas_filtered_group1 = df_pandas[df_pandas["GROUP1"] == "A"]
pandas_duration = time.time() - start_time
print(f"Pandas filter group1 duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% ## "value1" 列の値が 0 以上である行を抽出する
print("filtering float column")
start_time = time.time()
polars_filtered_value1 = df_polars.filter(pl.col("VALUE1") >= 0)
polars_duration = time.time() - start_time
print(f"Polars filter value1 duration: {polars_duration:.4f} seconds")
results.append(["Filter value1", polars_duration, None])

start_time = time.time()
pandas_filtered_value1 = df_pandas[df_pandas["VALUE1"] >= 0]
pandas_duration = time.time() - start_time
print(f"Pandas filter value1 duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration


# %% ## "group3" 列の値が欠損している行を抽出する
print("filtering missing value")
start_time = time.time()
polars_filtered_missing = df_polars.filter(pl.col("GROUP3").is_null())
polars_duration = time.time() - start_time
print(f"Polars filter missing duration: {polars_duration:.4f} seconds")
results.append(["Filter missing", polars_duration, None])

start_time = time.time()
pandas_filtered_missing = df_pandas[df_pandas["GROUP3"].isnull()]
pandas_duration = time.time() - start_time
print(f"Pandas filter missing duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% ----------------------------
# ---- データの列追加速度を比較
# -------------------------------
#  %% ## "value1" 列と "value2" 列の値を足し算した結果を "value1_2" 列として新しい列を作成する
start_time = time.time()
df_polars = df_polars.with_columns(
    (pl.col("VALUE1") + pl.col("VALUE2")).alias("VALUE1_2")
)
polars_duration = time.time() - start_time
print(f"Polars add columns duration: {polars_duration:.4f} seconds")
results.append(["Add columns", polars_duration, None])

start_time = time.time()
df_pandas["VALUE1_2"] = df_pandas["VALUE1"] + df_pandas["VALUE2"]
pandas_duration = time.time() - start_time
print(f"Pandas add columns duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% ----------------------------
# ---- データのグルーピング速度を比較
# -------------------------------
# %% ## "group1" 列の値でグルーピングして， 6個の "valueN" 列それぞれの平均値を求める
start_time = time.time()
polars_grouped = df_polars.group_by(["GROUP1", "GROUP2"]).agg(
    [
        pl.col(r"^VALUE\d$").mean(),
    ]
)
polars_duration = time.time() - start_time
print(f"Polars group by duration: {polars_duration:.4f} seconds")
results.append(["Group by", polars_duration, None])

start_time = time.time()
pandas_grouped = df_pandas.groupby(["GROUP1", "GROUP2"], as_index=False)[
    [f"VALUE{i}" for i in range(1, 7)]
].mean()
pandas_duration = time.time() - start_time
print(f"Pandas group by duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% ----------------------------
# ---- データの結合速度を比較
# -------------------------------
# %% ## df と df_weight を "group1" 列 "group2" 列の値を使って結合する
start_time = time.time()
polars_merged = df_polars.join(df_polars_weight, on=["GROUP1", "GROUP2"], how="inner")
polars_duration = time.time() - start_time
print(f"Polars merge duration: {polars_duration:.4f} seconds")
results.append(["Merge", polars_duration, None])

start_time = time.time()
pandas_merged = pd.merge(
    df_pandas, df_pandas_weight, on=["GROUP1", "GROUP2"], how="inner"
)
pandas_duration = time.time() - start_time
print(f"Pandas merge duration: {pandas_duration:.4f} seconds")
results[-1][2] = pandas_duration

# %% 結果をデータフレームに変換
results_df = pl.DataFrame(results, schema=["Operation", "Polars Duration", "Pandas Duration"])
print(results_df)

# getting_start_polars.py
# Created by ctirus
# Date: 2025/02/09

# %% ----------------------------
# ---- Abstract
# * このPythonスクリプトでは，基本的なpolarsでのデータ処理方法を紹介する
# * 扱うデータは，血液型を参考に適当に作成したものを用いる
# * データの中身1
# ** ID
# ** ABO: ABO血液型
# ** RH: RH血液型
# ** VAL1: 適当な値
# ** VAL2: 適当な値
# * データの中身2
# ** 重み
# -------------------------------

# %% ----------------------------
# ---- WIP
# -------------------------------

# %% ----------------------------
# ---- Library
# -------------------------------
import polars as pl
import pandera.polars as pa  # pandera.polarsであることに注意
pl.__version__  # 1.3.0

# %% ----------------------------
# ---- データの読み込み
# -------------------------------

# %% ## 血液型データの読み込み
# Pandera のスキーマ定義
class BloodSchema(pa.DataFrameModel):
    ID: int = pa.Field(ge=1, unique=True, nullable=False)
    ABO: str = pa.Field(isin=["AA", "AO", "BB", "BO", "AB", "OO"])
    RH: str = pa.Field(isin=["Rh+", "Rh-"])
    VAL1: float
    VAL2: int = pa.Field(ge=1, le=9)

    class Config:
        strict = True  # 定義以外の列があった場合，エラーを出力する

    @classmethod
    def to_polars_schema(cls):
        """Pandera スキーマを Polars のスキーマに変換"""
        mapping = {
            str: pl.String,
            int: pl.Int64,
            float: pl.Float64,
        }
        return {
            field: mapping.get(dtype, pl.Utf8)
            for field, dtype in cls.__annotations__.items()
        }


# Pandera のスキーマから Polars のスキーマを生成
blood_schema = BloodSchema.to_polars_schema()
# データの読み込み
blood_file_path = "./sample_data/blood_data.csv"
blood_df = pl.read_csv(blood_file_path, schema=blood_schema)

# %% ## 重みデータの読み込み
# Pandera のスキーマ定義
class WeightSchema(pa.DataFrameModel):
    ABO: str = pa.Field(isin=["AA", "AO", "BB", "BO", "AB", "OO"])
    WEIGHT: float

    class Config:
        strict = True  # 定義以外の列があった場合，エラーを出力する

    @classmethod
    def to_polars_schema(cls):
        """Pandera スキーマを Polars のスキーマに変換"""
        mapping = {
            str: pl.String,
            float: pl.Float64,
        }
        # return {field: mapping[dtype.__origin__] for field, dtype in cls.__annotations__.items()}
        return {
            field: mapping.get(dtype, pl.Utf8)
            for field, dtype in cls.__annotations__.items()
        }


# Pandera のスキーマから Polars のスキーマを生成
weight_schema = WeightSchema.to_polars_schema()
# データの読み込み
weight_file_path = "./sample_data/blood_data.csv"
weight_df = pl.read_csv(weight_file_path, schema=blood_schema)

# %% ----------------------------
# ---- データを保存する
# * write_csv
# -------------------------------
blood_df.write_csv("./sample_data/blood_data_output.csv")
# %% ----------------------------
# ---- データフレームを簡単に調べる
# * head
# * tail
# * sample
# * glimpse
# * describe
# -------------------------------
# %% 行の先頭を表示
blood_df.head(n=3)
# %% 行の末尾を表示
blood_df.tail(n=5)
# %% ランダムに行を抽出
blood_df.sample(10)
# %% 各列を1行ずつ表示
blood_df.glimpse()
# %% データフレームの要約統計量を表示
blood_df.describe()


# %% ----------------------------
# ---- データフレームの操作: 行の抽出
# * filter
# -------------------------------
# %% ## VAL1 列に対して条件でフィルター
blood_df.filter(pl.col("VAL1") > 2.0)
# %% ## RH 列に対して条件でフィルター
blood_df.filter(pl.col("RH") == "Rh-")
# %% ## 正規表現を用いることも可能
blood_df.filter(pl.col("ABO").str.contains(r"A."))
# %% ## 複数条件を設定するときは，各条件を "()" で囲む
blood_df.filter((pl.col("ABO") == "BB") & (pl.col("RH") == "Rh-"))
# %% ## 欠損のフィルタリング
blood_df.filter(pl.col("RH").is_null())
# %% ## 欠損値以外のフィルタリング
blood_df.filter(pl.col("RH").is_not_null())

# %% ----------------------------
# ---- データフレームの操作: 列の選択
# * select
# -------------------------------
# %% ## 列名の選択
# 下記はどれでかいても良い
blood_df.select("ID", "RH")
blood_df.select(["ID", "RH"])
blood_df.select([pl.col("ID"), pl.col("RH")])
# %% ## 正規表現を用いることも可能
blood_df.select(pl.col(r"^VAL\d$"))
# %% ## 列の選択と同時に計算することも可能
blood_df.select(pl.col("VAL2") + 100)

# %% ----------------------------
# ---- データフレームの操作: ソート
# * sort
# -------------------------------
# %% ## VAL1 列で昇順ソート
blood_df.sort("VAL1", descending=True)
# %% ## 複数列でソート
blood_df.sort(["ABO", "RH"])

# %% ----------------------------
# ---- データフレームの操作: 列の追加
# * with_columns
# -------------------------------
# %% ## エクスプレッションを使って，計算する
# * with_columnsは，非破壊操作であるので，元のデータフレームに追加したい場合，代入する必要がある
# * 列名は .alias() もしくは 列名 = で指定する
blood_df = blood_df.with_columns((pl.col("ABO") + "_" + pl.col("RH")).alias("ABO_RH"))
blood_df = blood_df.with_columns(RH_ABO = (pl.col("RH") + "_" + pl.col("ABO")))
blood_df.head()
# %% ## 自作関数を適用する場合
# ただし，パフォーマンスの観点から，可能な限り native expressions API を使うことを考える
def get_abo_blood_type(abo: str) -> str:
    if (abo == "AA") or (abo == "AO"):
        return "A"
    elif (abo == "BB") or (abo == "BO"):
        return "A"
    elif abo == "AB":
        return "AB"
    elif abo == "OO":
        return "O"
    else:
        return "UNKNOWN"


blood_df.with_columns(pl.col("ABO").map_elements(get_abo_blood_type, str).alias("ABO_TYPE"))


# %% ----------------------------
# ---- 欠損値の対応
# * drop_nulls: 欠損値を除去する
# * fill_null: 欠損値を埋める
# -------------------------------
# %% ## 全ての列での欠損値を削除
blood_df.drop_nulls()
# %% ## 特定の列での欠損値を削除
blood_df.drop_nulls(["RH"])
# %% ## 欠損値を埋める
# * RH 列の欠損値を "UNKNOWN" で埋める
blood_df.with_columns(pl.col("RH").fill_null("UNKNOWN"))
# * RH 列の欠損値を "最頻値" で埋める
blood_df.with_columns(pl.col("RH").fill_null(pl.col("RH").mode().first()))

# %% ----------------------------
# ---- グルーピング
# * group_by: グループ単位で統計量を求める
# -------------------------------
blood_df.group_by(["ABO", "RH"]).agg(pl.col("VAL1").mean())

# %% ----------------------------
# ---- データの結合
# * join: データを結合する
# -------------------------------
blood_df.join(weight_df, on="ABO", how="inner")


# %% ----------------------------
# ---- ピボットとピボット解除
# * pivot: ピボット(縦長データ　-> 横長データ)
# * uppivot: ピボット解除(横長データ　-> 縦長データ)
# * 血液型データではなく，例データを用いる
# -------------------------------
# %% ## ピボット(pivot)
df = pl.DataFrame({
    "NAME": ["Alice", "Alice", "Bob", "Bob"],
    "YEAR": [2020, 2021, 2020, 2021],
    "SCORE": [80, 90, 85, 95]
})

df.head()

df_pivot = df.pivot(on="YEAR", index="NAME", values="SCORE", aggregate_function="mean")
df_pivot.head()

# %% ## ピボット解除(unpivot)
df_pivot_unpivot = df_pivot.unpivot(on=["2020", "2021"], index="NAME", variable_name="YEAR", value_name="SCORE")
df_pivot_unpivot


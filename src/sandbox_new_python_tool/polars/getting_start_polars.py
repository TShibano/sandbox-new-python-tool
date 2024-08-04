# getting_start_polars.py
# このPythonスクリプトでは，基本的なpolarsでのデータ処理方法を紹介する
# %% ライブラリのインポート
import polars as pl
import pandera.polars as pa    # pandera.polarsであることに注意

# %% polarsのバージョン
pl.__version__    # 1.3.0

# %% データの読み込み
file_path = "./sample_data/blood_data.csv"
df = pl.read_csv(file_path)
# %% Panderaによるデータフレームのチェック ===============
class BloodSchema(pa.DataFrameModel):
    id: int = pa.Field(ge=1, unique=True, nullable=False)
    abo: str = pa.Field(isin=["AA", "AO", "BB", "BO", "AB", "OO"])
    rh: str = pa.Field(isin=["Rh+", "Rh-"])
    val1: float
    val2: int = pa.Field(ge=1, le=9)

    class Config:
        strict = True    # 定義以外の列があった場合，エラーを出力する

# %%
df = BloodSchema.validate(df)

# %% データフレームを簡単に確認する ============
# %% 行の先頭を抽出　
df.head(n=3)
# %% 行の末尾を抽出
df.tail(n=5)
# %% ランダムに抽出
df.sample(10)
# %% 各列を1行ずつ表示
df.glimpse()
# %% データフレームの要約統計量を表示
df.describe()

# %% データフレームの操作 =====================
# %% 行の抽出(filter)
df.filter(pl.col("val1") > 2.0)
df.filter(pl.col("rh") == "Rh-")
# 正規表現を用いることも可能
df.filter(pl.col("abo").str.contains(r"A."))
# 複数条件を設定するときは，各条件を "()" で囲む
df.filter((pl.col("abo") == "BB") & (pl.col("rh") == "Rh-"))

# %% 列の選択(select)
# 下記はどれでかいても良い
df.select("id", "rh")
df.select(["id", "rh"])
df.select([pl.col("id"), pl.col("rh")])
# 正規表現を用いることも可能
df.select(pl.col(r"^val\d$"))
# 列の選択と同時に計算することも可能
df.select(pl.col("val2") + 100)

# %% 列の追加(with_columns)
# with_columnsは，非破壊操作であるので，元のデータフレームに追加したい場合，代入する必要がある
df.with_columns(abo_rh = pl.col("abo") + "_" + pl.col("rh"))
# 自作関数を適用する場合
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
df.with_columns(pl.col("abo").map_elements(get_abo_blood_type, str).alias("ABO_TYPE"))

# %% ユニーク

# %% 欠損値の対応
# 欠損値を削除

# 欠損値を埋める

# %% ピボット(pivot)


# %% ピボット解除(unpivot)

# %% グルーピング

# %% 
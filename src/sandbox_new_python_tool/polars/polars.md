# polars

## Abstract

Polarsの概要は以下になります([polars Gihub](https://github.com/pola-rs/polars)より，日本語訳)．

> Polarsは、メモリモデルとしてApache Arrow Columnar Format(列単位でデータを保持する形式)を使用し、Rustで実装されたOLAP(Online Analytical Processing)クエリエンジン上に構築されたデータフレームインターフェースである。
> 
> * 遅延評価（Lazy）| 即時評価（Eager）
> * マルチスレッド対応
> * SIMD（シングル・インストラクション・マルチプル・データ）
> * クエリ最適化
> * 強力な式API
> * ハイブリッドストリーミング（RAMを超えるデータセットの処理）
> * Rust | Python | NodeJS | R | などに対応


上記の特徴からpolarsは高いパフォーマンスを持っており，一方でPandasと似ている部分が多いことから，pandasからの移行先として注目されている．

## Usage
### Install
pipの場合は以下である．`polars`だけでは一部のライブラリが足らないことになりますので，全部入れておく．
```
pip install "polars[all]"
```

ryeの場合は以下である．
```
rye add "polars[all]"
rye sync
```

## Polarsの特徴-Pandasと比較して-

以下にPolarsとPandasの比較をテーブル形式でまとめまる。
(ChatGPTで作成．)

| **比較項目**      | **Polars**            | **Pandas**                            |
|------------------|-----------------------------------------------------|-------------------------------------------------------|
| **パフォーマンス** | 非常に高速（Rustで実装、マルチスレッドサポート）      | 高速（Cythonで実装、シングルスレッド）                |
| **メモリ効率**     | 高い（効率的なメモリ使用、データのコピーを最小化）      | 比較的低い（メモリ消費が多く、データのコピーが多い） |
| **APIと使いやすさ**| Pandasに似たAPI（学習コスト低、完全互換性はなし）      | 直感的で使いやすいAPI、豊富なドキュメントとサポート |
| **評価方法**      | 逐次評価と遅延評価をサポート          | 逐次評価のみサポート                |
| **学習リソース**   | 比較的少ないが増えてきている                  | 豊富（広く使われているため）                           |
| **エコシステム**   | 発展途上(ただし，`.to_pandas()`でPandasに変換可能なのでそこまで問題にならないか)       | 確立されており、多くの外部ライブラリと統合されている  |


## Reference
* Official
    * [pola.rs](https://pola.rs)
    * [polars User Guide](https://docs.pola.rs)
    * [polars github](https://github.com/pola-rs/polars)
* 日本語で書かれた記事
    * [](https://qiita.com/_jinta/items/fac13f09e8e8a5769b79#fn-lazy)
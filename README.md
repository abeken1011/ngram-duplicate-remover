# ngram-duplicate-remover
指定したngramで重複がある文章を削除するモジュール

#### オプション
df:処理したいデータフレーム

cc_column: 文章が入っているカラム名

ngram_range: 指定したngramで重複があるかを検索 default = 3

dic_location: 本文をmecabの分かち書きを行う際に使う辞書 default = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"

(optional)category: カテゴリが付与されている場合、そのカテゴリの中でのみ検索を行うので処理が高速化

#### example

```python  
from ngram-duplicate-remover import duplicate_remover
import pandas as pd                                                              

df = pd.read_csv("data.csv")     
df = df.dropna(subset=['カテゴリー名']) # カテゴリーごとに計算する場合、前処理でカテゴリーの欠損値を削除しておいてください
df = df.dropna(subset=["text"])
df2 = duplicate_remover.duplicate_remover(df, "text", category="カテゴリー名", ngram_range=3) # 重複のなくなったデータフレームを返却
```

# coding: utf-8

import time
import numpy as np
import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

def zero_one(x):
    if x != 0:
        return 1
    else:
        return 0

def duplicate_remover(
        df, cc_column, category=None, ngram_range=3, dic_location="/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
    ):
    owakati = MeCab.Tagger(f"-Owakati -d {dic_location}")
    parsed_copy_column = "parsed_copy_column"
    tmp = df.copy()
    
    # コピーを分かち書き
    tmp[parsed_copy_column] = tmp[cc_column].apply(owakati.parse)
    
    # Vectorizerを作成
    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        analyzer='word',
        token_pattern=r'\w{1,}',
        ngram_range=(ngram_range, ngram_range),
    )

    # カテゴリごとに計算
    for cat in df[category].unique():
        print(f"カテゴリ\t{cat}を計算中")
        tmp_cat = tmp.query(f"{category} == '{cat}'")
        if len(tmp_cat) > 1:
            # tfidfgをnumpy配列で格納
            X_tfidf = word_vectorizer.fit_transform(tmp_cat[parsed_copy_column]).toarray()

            # 文字列が出現したか否か01の配列に変更
            bool_array = np.vectorize(zero_one)(X_tfidf)

            # 被ったngram単語のインデックスを取得
            dup_index = np.where(np.apply_along_axis(sum, 0, bool_array) > 1)

            # 被ったカラムのインデックスを格納
            dup_cols = []

            # 被ったカラムのインデックスとその単語の位置を格納
            dup_words_col = {}
            # 行ごとに被りがあるか見ていく
            for i in range(bool_array.shape[0]):
                words = np.where(bool_array[i] > 0)
                # これまで出てきたワードの被った特徴カラムを格納 2以上で被りあり
                dup_words = np.in1d(words, dup_index)
                if dup_words.sum() > 1:
                    dup_words_col.setdefault(i, np.where(dup_words  == True))
                    dup_cols.append(i)

            # 重複したカラムで1個目のみを残す
            dup_words = np.array([])
            for ind, arr in dup_words_col.items():
                if np.in1d(arr, dup_words).sum() == 0:
                    dup_cols.remove(ind)
                dup_words = np.unique(np.append(dup_words, ind))
    
    return df.drop(df.index[dup_cols])
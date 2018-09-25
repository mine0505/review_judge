from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
from keras.models import load_model
import tensorflow as tf
import numpy as np
import MeCab
import json
import csv
import re

def owakati(data):
    tagger = MeCab.Tagger("-Owakati") #分かち書きするためのインスタンス
    sentence = tagger.parse(data)

    return sentence

def load_csv():
    issues = []
    # CSVファイルを読み込む
    with open("./eiga_score_texts.csv", 'r', encoding="utf-8") as f:
        csv_file = csv.reader(f, delimiter=',')
        
        # 配列に変換
        for row in csv_file:
            issues.append(row)

    issues.pop(0) # 1行目を削除

    return issues

def gen_dict(data):
    # 辞書作成用にレビューのテキストをロード
    texts = [t[1] for t in data if t[0] != "-"] # レビューのテキストの配列を作成

    # Word Index(辞書)の作成
    max_words = 80000 # 最大語彙数

    # テキストをベクトルに変換
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(texts) # word_index(辞書)を作成
    word_index = tokenizer.word_index # 辞書を取得
    print("一意な {} 個の語彙の辞書".format(len(word_index)))

    return tokenizer

def text_to_seq(tokenized_text, tokenizer):
    sequences = tokenizer.texts_to_sequences([tokenized_text]) # テキストをシーケンスに変換

    return sequences

def predict(model, input_text, sequences):
    maxlen = 400 # ひとつのレビューの最大の文の長さ(単語の個数)
    padded_seq = pad_sequences(sequences, maxlen=maxlen) # ゼロ埋め

    print(input_text)
    print(sequences)
    #print(padded_seq)

    # 予測
    prediction_text_label = ['(ノд-｀) < Oh...', '(σﾟ∀ﾟ)σ <Good!']

    results = model.predict([padded_seq], verbose=1)[0] # padded_seqは2次元の行列で渡す。
    #print(results)
    sorted_results = sorted([(i,e) for i,e in enumerate(results)], key=lambda x:x[1]*-1)
    #print(sorted_results)

    sorted_text_results = []
    for result in sorted_results:
        #print(result)
        id, probability = result
        sorted_text_results.append('{} : {}%'.format(prediction_text_label[id], round(float(probability)*100, 2)))

    print(sorted_text_results)

    response = []
    response.append('そのレビュー {} かな？'.format(prediction_text_label[np.argmax(results)]))
    response.append(sorted_text_results)
    response.append(results)

    return response

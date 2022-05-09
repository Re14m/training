#ライブラリのインポート
import streamlit as st
from janome.tokenizer import Tokenizer
import collections
import pandas as pd

#データセット読込
with open('result.txt', 'r', encoding='UTF-8') as f:
    text = f.read()
t = Tokenizer()

c = collections.Counter(token.base_form for token in t.tokenize(text)
                        if token.part_of_speech.startswith('名詞,固有名詞'))
print(c.most_common()[:30])

# 頻出単語を可視化
st.title('Streamlit Twitterフォロワー分析')
df = pd.DataFrame(c.most_common()[:30], columns=['単語', '回数'])
st.dataframe(df)
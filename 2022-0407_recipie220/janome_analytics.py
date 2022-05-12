# [TwitterAPIで乃木坂４６メンバーの話題度を比較分析するレシピ(https://axross-recipe.com/recipes/220)]

# パッケージのインストール
from janome.tokenizer import Tokenizer
import collections

# search_tweet.pyで生成したtxtを読込
with open('search_tweets.txt', 'r', encoding='UTF-8') as f:
    text = f.read()

# 形態素解析結果をtとする
t = Tokenizer()

# tを名詞と固有名詞に分けてcとしてカウント
c = collections.Counter(token.base_form for token in t.tokenize(text)
                        if token.part_of_speech.startswith('名詞,固有名詞'))

# カウント結果の上位30位を表示
print(c.most_common()[:30])
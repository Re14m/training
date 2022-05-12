#!/usr/bin/env python
# coding: utf-8

# モジュールのインポート
import openai

# APIキーの入力
# これはれいあむのなので使わないで欲しいﾅﾘ
openai.api_key = "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"

# promptに送るテキストを入力
text = "ベナオ個人ブログ\nBio\n私はPythonを主に扱うフリーランスエンジニアです。SNSやブログでプログラミングについての情報発信をしています。興味があるのは機械学習や自然言語処理です。電子決済システムの開発に関わっていました。\nBlog\n\n2021年3月2日\nTitle:人工知能は人間の仕事を奪うのか？\ntags:人工知能、機械学習、シンギュラリティ\nSummary: 人工知能が人間の知性を超えた時に人間の仕事が奪われるのではないかという危険性について説明する\nFull text:"

# APIの呼出しとパラメータ指定
response = openai.Completion.create(
    engine="davinci",
    prompt=text,
    temperature=0.7,
    max_tokens=1500,
    presence_penalty=0,
)

'''
engine：
使用する文章生成エンジンの種類を指定します。エンジンによって生成速度や性能に違いがあります。詳しくはOpenAIのページを参照してください。

prompt：
文章生成の材料になるテキストを入力します。

temperature：
値が1に近づくほどよりクリエイティブな文章に、0に近づくと論理的で問題に対して正確に返答するようになるようです。

max_tokens：
生成する文章の長さを指定します。試した限りでは1500辺りが限界のようです。

presence_penalty：
1に近づけるほど、過去に出力した結果と同様の結果を生成する可能性を減らします。
毎回異なる結果が欲しい場合は１に、再現性が欲しい場合は0に近づけます。
'''
# 結果を出力
print(response['choices'][0]['text'])
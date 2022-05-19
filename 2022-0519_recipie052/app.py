# [Amazon Translateを使った機械翻訳のレシピ(基礎編)](https://axross-recipe.com/recipes/52)

# パッケージのインポート
import boto3

# Translate用クライアントの作成
translate_client = boto3.client(service_name='translate')

# 三笠山のテキストファイルの Path を指定
BEFORE_PATH = './三笠山(ja).txt'
AFTER_PATH = './三笠山(en).txt'

# 三笠山のテキストを読み込む
with open(BEFORE_PATH, encoding='UTF-8') as f:
    text = f.read()

# 翻訳前のテキスト
print('***翻訳前のテキスト***\n', text)

# Translate_text API を利用
response = translate_client.translate_text(Text=text,  
                                           SourceLanguageCode='ja',  
                                           TargetLanguageCode='en')

# responseで返ってきたデータ
result_text = response['TranslatedText']

# 翻訳後のテキストを書き込む
with open(AFTER_PATH, encoding='UTF-8', mode='w') as f:
    f.write(result_text)

# 翻訳語のテキスト
print('\n***翻訳後のテキスト***\n', result_text)

# Request Syntax
{
   "SourceLanguageCode": "string",
   "TargetLanguageCode": "string",
   "TerminologyNames": [ "string" ],
   "Text": "string"
}

# Response Syntax
{
   "AppliedTerminologies": [ 
      { 
         "Name": "string",
         "Terms": [ 
            { 
               "SourceText": "string",
               "TargetText": "string"
            }
         ]
      }
   ],
   "SourceLanguageCode": "string",
   "TargetLanguageCode": "string",
   "TranslatedText": "string"
}
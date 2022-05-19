# [Amazon Translateを使った機械翻訳のレシピ(基礎編)](https://axross-recipe.com/recipes/52)

# パッケージのインポート
import boto3

# Translate用クライアントの作成
translate_client = boto3.client(service_name='translate')

# csv読込
with open('custom1.csv', 'rb') as f:
        data = f.read()

file_data = bytearray(data)
translate_client.import_terminology( 
    Name='custom1', 
    MergeStrategy='OVERWRITE', 
    TerminologyData={"File": file_data, "Format": 'CSV'})

# Request Syntax
{
   "Description": "string",
   "EncryptionKey": { 
      "Id": "string",
      "Type": "string"
   },
   "MergeStrategy": "string",
   "Name": "string",
   "TerminologyData": { 
      "File": blob,
      "Format": "string"
   }
}

# Response Syntax
{
   "TerminologyProperties": { 
      "Arn": "string",
      "CreatedAt": number,
      "Description": "string",
      "EncryptionKey": { 
         "Id": "string",
         "Type": "string"
      },
      "LastUpdatedAt": number,
      "Name": "string",
      "SizeBytes": number,
      "SourceLanguageCode": "string",
      "TargetLanguageCodes": [ "string" ],
      "TermCount": number
   }
}

# 例文
custom_text = 'あめを食べる'

# Translate_text API を利用
response = translate_client.translate_text(Text=custom_text, 
                                      SourceLanguageCode='ja', 
                                      TargetLanguageCode='en', 
                                      TerminologyNames=['custom1'])

# responseで返ってきたデータ
result_text = response['TranslatedText']

# 出力
print(result_text)
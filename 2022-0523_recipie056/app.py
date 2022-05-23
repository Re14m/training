# [Amazon Rekognitionを使った画像認識のレシピ(基礎編)](https://axross-recipe.com/recipes/56)

# パッケージのインポート
import boto3

# Rekognition利用クライアントの作成
rekognition_client = boto3.client(service_name='rekognition')

# 画像のPath
PHOTO_PATH = './dog.png'

# 画像ファイルの読込バイト列を取得
with open(PHOTO_PATH, 'rb') as p:
    source_bytes = p.read()

# RekognitionのAPI（DetectLabels）のラベル検出
response = rekognition_client.detect_labels(
               Image={
                   'Bytes': source_bytes
               }
)

# 返ってきたresponseからラベル名・信頼性を出力
for label in response['Labels']:
    print("{Name:30},{Confidence:.2f}%".format(**label))
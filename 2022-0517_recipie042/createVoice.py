# [Amazon Polly を使った音声合成のレシピ(応用編)](https://axross-recipe.com/recipes/42)

# パッケージのインポート
import boto3

# Polly用クライアントの作成
polly_client = boto3.Session(
               aws_access_key_id= 'AKIA3IZKHWT2W34DC277',                     
               aws_secret_access_key= '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',
               region_name='ap-northeast-1'
               ).client('polly')

# SynthesizeSpeech API を利用
response = polly_client.synthesize_speech(
           VoiceId='Mizuki',
           OutputFormat='mp3', 
           Text = 'こんにちは。レシピを見ていただきありがとうございます！')

# 返却したレスポンスから音声ファイルを作成
with open('speech01.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

# SynthesizeSpeech API を利用
response = polly_client.synthesize_speech(
           VoiceId='Joanna',
           OutputFormat='mp3', 
           Text = 'Hello, Thank you for reading the this recipe!!')

# 返却したレスポンスから音声ファイルを作成
with open('speech02.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

# 発話させる内容をSSMLで定義する
text = "<speak><phoneme type='ruby' ph='おこなっ'>行</phoneme>った</speak>"

# SynthesizeSpeech API を利用
response = polly_client.synthesize_speech(
           VoiceId='Mizuki',
           OutputFormat='mp3', 
           Text = text,
           TextType = 'ssml')

# 返却したレスポンスから音声ファイルを作成
with open('speech03.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())
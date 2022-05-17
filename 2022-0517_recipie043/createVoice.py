# [Amazon Polly を使った音声合成のレシピ(基礎編)](https://axross-recipe.com/recipes/43)
# パッケージのインポート
import boto3

# Polly用クライアントを作成
polly_client = boto3.Session(region_name='us-west-2').client('polly')

# SynthesizeSpeech API を利用
response = polly_client.synthesize_speech(
           VoiceId='Takumi',
           OutputFormat='mp3', 
           Text = 'こんにちは。レシピを見ていただきありがとうございます！')

# 返却したレスポンスから音声ファイルを作成
with open('speech.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

# Request Syntax
response = client.synthesize_speech(
    Engine='standard'|'neural',
    LanguageCode='arb'|'cmn-CN'|'cy-GB'|'da-DK'|'de-DE'|'en-AU'|'en-GB'|'en-GB-WLS'|'en-IN'|'en-US'|'es-ES'|'es-MX'|'es-US'|'fr-CA'|'fr-FR'|'is-IS'|'it-IT'|'ja-JP'|'hi-IN'|'ko-KR'|'nb-NO'|'nl-NL'|'pl-PL'|'pt-BR'|'pt-PT'|'ro-RO'|'ru-RU'|'sv-SE'|'tr-TR',
    LexiconNames=[
        'string',
    ],
    OutputFormat='json'|'mp3'|'ogg_vorbis'|'pcm',
    SampleRate='string',
    SpeechMarkTypes=[
        'sentence'|'ssml'|'viseme'|'word',
    ],
    Text='string',
    TextType='ssml'|'text',
    VoiceId='Aditi'|'Amy'|'Astrid'|'Bianca'|'Brian'|'Camila'|'Carla'|'Carmen'|'Celine'|'Chantal'|'Conchita'|'Cristiano'|'Dora'|'Emma'|'Enrique'|'Ewa'|'Filiz'|'Geraint'|'Giorgio'|'Gwyneth'|'Hans'|'Ines'|'Ivy'|'Jacek'|'Jan'|'Joanna'|'Joey'|'Justin'|'Karl'|'Kendra'|'Kevin'|'Kimberly'|'Lea'|'Liv'|'Lotte'|'Lucia'|'Lupe'|'Mads'|'Maja'|'Marlene'|'Mathieu'|'Matthew'|'Maxim'|'Mia'|'Miguel'|'Mizuki'|'Naja'|'Nicole'|'Penelope'|'Raveena'|'Ricardo'|'Ruben'|'Russell'|'Salli'|'Seoyeon'|'Takumi'|'Tatyana'|'Vicki'|'Vitoria'|'Zeina'|'Zhiyu'
)

# Response Syntax
{ 
    'AudioStream' : StreamingBody(),
    'ContentType' : 'string' ,
    'RequestCharacters' : 123 
}
# [AWSのサービスを活用した音声合成と機械翻訳の連携のレシピ](https://axross-recipe.com/recipes/63)

# パッケージのインポート
import tkinter as tk
from tkinter import ttk
import sys
import boto3
from pygame import mixer

MALE_POLLY_LIST = {
    'en':'Matthew',
    'ja':'Takumi',
    'fr':'Mathieu',
    'de':'Hans',
    'it':'Giorgio',
    'es':'Enrique'
    }
FEMALE_POLLY_LIST = {
    'en':'Joanna',
    'ja':'Mizuki',
    'fr':'Celine',
    'de':'Marlene',
    'it':'Carla',
    'es':'Conchita'
    }

# Polly用クライアントの作成
polly_client = boto3.client('polly')

# Translate用クライアントの作成
translate_client = boto3.client('translate')

# 関数の定義
def translate(level,lang_select,name):
    if lang_select.get() != 'ja':
        # Translate_text API を利用
        response = translate_client.translate_text(Text=name.get(),  
                                                SourceLanguageCode='ja',  
                                                TargetLanguageCode=lang_select.get())
        # responseで返ってきたデータ
        result_text = response['TranslatedText']

        polly(level,lang_select,result_text)
    else:
        polly(level,lang_select,name.get())

    return True

def polly(level,lang_select,result_text):
    if level.get() == 'Male':
        voice_id = MALE_POLLY_LIST[lang_select.get()]
    elif level.get() == 'Female':
        voice_id = FEMALE_POLLY_LIST[lang_select.get()]

    # SynthesizeSpeech API を利用
    response = polly_client.synthesize_speech(
           VoiceId=voice_id,
           OutputFormat='mp3', 
           Text=result_text)

    # 返却したレスポンスから音声ファイルを作成
    with open('speech.mp3', 'wb') as f:
            f.write(response['AudioStream'].read())
    
    mixer.init()        # 初期化
    mixer.music.load('speech.mp3')        # 再生したいファイルの Load
    mixer.music.play(1)        # 再生したい回数

    return True

root = tk.Tk()
root.title('Recipe Test')

# variable用のオブジェクト
level = tk.StringVar()
level.set('Male')

lang_select = tk.StringVar()
lang_select.set('ja')

# メニューバー
menubar = tk.Menu(root)
root.configure(menu = menubar)

filemenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='設定', underline=0, menu=filemenu)
filemenu.add_command(label='Exit', command=lambda: root.destroy())

gender = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='性別', underline=0, menu=gender)

language = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='言語', underline=0, menu=language)

# CheckList
gender.add_radiobutton(label = '男性', variable = level, value = 'Male')
gender.add_radiobutton(label = '女性', variable = level, value = 'Female')

language.add_radiobutton(label='日本', variable=lang_select, value='ja')
language.add_radiobutton(label='英語', variable=lang_select, value='en')
language.add_radiobutton(label='フランス語', variable=lang_select, value='fr')
language.add_radiobutton(label='ドイツ語', variable=lang_select, value='de')
language.add_radiobutton(label='イタリア語', variable=lang_select, value='it')
language.add_radiobutton(label='スペイン語', variable=lang_select, value='es')

# Frame1 Setting
frame1 = ttk.Frame(root, padding=16)
label1 = ttk.Label(frame1, text='Text')
name = tk.StringVar()
entry1 = ttk.Entry(frame1, textvariable=name)
button1 = ttk.Button(
    frame1,
    text='音声合成',
    command=lambda : translate(level,lang_select,name)
)

# Layout Setting
frame1.pack()
label1.pack(side=tk.LEFT)
entry1.pack(side=tk.LEFT)
button1.pack(side=tk.LEFT)

root.mainloop()
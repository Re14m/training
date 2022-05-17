# [Amazon Polly を使った音声合成のレシピ(応用編)](https://axross-recipe.com/recipes/42)

# パッケージのインポート
import tkinter as tk
from tkinter import ttk
import sys
import boto3
from pygame import mixer

# Polly をつかうためのクライアントを作成
polly_client = boto3.client('polly')

def polly(level,name):
    # SynthesizeSpeech API を利用
    response = polly_client.synthesize_speech(
           VoiceId=level.get(),
           OutputFormat='mp3', 
           Text=name.get())

    # 返却したレスポンスから音声ファイルを作成
    with open('speech.mp3', 'wb') as f:
            f.write(response['AudioStream'].read())
    
    mixer.init()        # 初期化
    mixer.music.load('speech.mp3')        # 再生したいファイルの Load
    mixer.music.play(1)        # 再生したい回数

root = tk.Tk()
root.title('Recipe Test')

# variable 用のオブジェクト
level = tk.StringVar()
level.set('Takumi')

# メニューバー
menubar = tk.Menu(root)
root.configure(menu = menubar)

filemenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='設定', underline=0, menu=filemenu)
filemenu.add_command(label='Exit', command=lambda: root.destroy())

gender = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label='性別', underline=0, menu=gender)

# CheckList
gender.add_radiobutton(label = '男性', variable = level, value = 'Takumi')
gender.add_radiobutton(label = '女性', variable = level, value = 'Mizuki')

# Frame1 Setting
frame1 = ttk.Frame(root, padding=16)
label1 = ttk.Label(frame1, text='Text')
name = tk.StringVar()
entry1 = ttk.Entry(frame1, textvariable=name)
button1 = ttk.Button(
    frame1,
    text='音声合成',
    command=lambda : polly(level,name)
)

# Layout Setting
frame1.pack()
label1.pack(side=tk.LEFT)
entry1.pack(side=tk.LEFT)
button1.pack(side=tk.LEFT)

root.mainloop()
# [Amazon Polly を使った音声合成のレシピ(基礎編)](https://axross-recipe.com/recipes/43)
# パッケージのインポート
from pygame import mixer

mixer.init()        # 初期化
mixer.music.load('speech.mp3')        # 再生したいファイルの Load
mixer.music.play(1)        # 再生したい回数
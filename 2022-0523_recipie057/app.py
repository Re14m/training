# [Amazon Rekognitionを使った画像認識のレシピ(応用編)](https://axross-recipe.com/recipes/57)

# パッケージのインポート
import boto3
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw


# 画像のPath
PHOTO_PATH = './human.png'

# class変数初期化
class DetectInfo(object):
    """
    検出情報格納用クラス

    Attributes
    ----------
    name : str
        人物名または物体名
    confidence : float
        検出した人物・物体の一致信頼度（0.0～100.0 %）
    top : int
        人物の顔または物体が写っている領域(四角形)の左上角のy座標
    left : int
        人物の顔または物体が写っている領域(四角形)の左上角のx座標
    height : int
        人物の顔または物体が写っている領域(四角形)の高さ
    width : int
        人物の顔または物体が写っている領域(四角形)の幅
    """
    def __init__(self):
        self.name = ""
        self.confidence = 0
        self.top = 0
        self.left = 0
        self.height = 0
        self.width = 0


def get_detect_list(response, img):
    """
    検出した物体の情報取得関数

    Parameters
    ----------
    response : dict
        AWS Rekognitionの解析結果データ
    img : ndarray
        画像データ

    Returns
    ----------
    detect_list : list
        検出した物体の情報の検出数分のリスト
    """
    img_height, img_width = img.shape[:2]  # 解析対象画像の高さと幅を取得
    detect_list = []

    for obj in response['Labels']:
        for instance in obj['Instances']:
            info = DetectInfo()
            info.name = obj['Name']
            info.confidence = instance['Confidence']
            # 物体の位置情報を算出
            info.top = int(img_height * instance['BoundingBox']['Top'])
            info.left = int(img_width * instance['BoundingBox']['Left'])
            info.height = int(img_height * instance['BoundingBox']['Height'])
            info.width = int(img_width * instance['BoundingBox']['Width'])
            detect_list.append(info)

    return detect_list

img = cv2.imread(PHOTO_PATH)

# Rekognition をつかうためのクライアントを作成
rekognition_client = boto3.client(service_name='rekognition')

with open(PHOTO_PATH, 'rb') as p:
    source_bytes = p.read()

# RekognitionのAPIである、DetectLabelsでラベルを検出する
response = rekognition_client.detect_labels(
               Image={
                   'Bytes': source_bytes
               }
)

detect_list = get_detect_list(response,img)

# 物体の枠
for info in detect_list:
    img = cv2.rectangle(img, (info.left, info.top),
                        (info.left + info.width, info.top + info.height),
                        (255, 0, 255), thickness=1)
    img = cv2.rectangle(img, (info.left + 4, info.top + 4),
                        (info.left + info.width - 4, info.top + info.height - 4),
                        (0, 255, 255), thickness=1)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
image = Image.fromarray(img)

# OS is MAC
# FONT = '/Library/Fonts/Arial Bold.ttf'

# OS is Windows
FONT = 'arial'
font = ImageFont.truetype(FONT, 12)

# 物体のラベル
for info in detect_list:
        name = info.name
        # get text size
        text_size = font.getsize(name)
        # set box size + 5px margins
        box_size = (text_size[0] + 2, text_size[1] + 3)
        # create image with correct size and #B22222 background
        box_img = Image.new('RGB', box_size, '#ffc0cb')
        # put text on box with 10px margins
        box_draw = ImageDraw.Draw(box_img)
        box_draw.text((1, 1), name, font=font, fill='#000000')
        # put box on image in position (0, 0)
        top = info.top + 20
        left = info.left + 20
        image.paste(box_img, (left, top))

img = np.array(image)
cv2.imwrite('after.png',img)

# 画像の表示
cv2.imread('after.png')
cv2.imshow('color', img)
cv2.waitKey(0)
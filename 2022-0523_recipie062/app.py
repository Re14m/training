# [AWSのサービスを活用した有名人画像認識アプリの開発のレシピ ～前編(画像認識)～](https://axross-recipe.com/recipes/62)

# パッケージのインポート
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import os
from tkinter import messagebox
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import cv2
import sys
import boto3
from botocore.exceptions import BotoCoreError, ClientError

FILE_EXT = ['.jpg', '.png', '.jpeg', '.jpe', '.jfif', '.gif', '.tif', '.tiff', '.bmp', '.dib', '.webp']         # 拡張子の制限
IMAGE_MAX = 1080         # resize処理最大の制限
IMAGE_REG = 400         # resize処理中間に拡大
IMAGE_MIN = 250         # resize処理最小の制限

CONFIDENCE = 75.0         # 目安のConfidence
ERROR_CDRAW = 20            # celeb_name描画時の制限
ERROR_ODRAW = 25            # object_name描画時の制限
FUNTTTF = 'msgothic'            # Fontの設定

# class変数初期化
class DetectInfo(object):
    def __init__(self):
        self.name = ""
        self.parent = []
        self.confidence = 0
        self.top = 0
        self.left = 0
        self.height = 0
        self.width = 0
        self.url = ''



# class変数初期化
class AnalysisData(object):
    def __init__(self):
        self.celeb = []             # 検出した有名人物情報リスト
        self.unknown = []           # 検出したUnknownリスト
        self.object = []            # 検出した物体情報リスト
        self.img = ''               # 画像データ(解析前/解析後)
        self.celeb_names = ''       # 検出した有名人の名前
        self.object_names = ''      # 検出した物体の名前
        self.celeb_cnt = 0          # 検出した有名人の人数
        self.unknown_cnt = 0        # Unknownの人数
        self.object_namelist = []   # 検出した物体の名前のリスト
        self.rate = 0               # 画像をリサイズするための比率
        self.filename = ''          # イメージのパス



class GuiApp(object):
    def __init__(self):
        pass

    def make_app(self, app=None):
        # Window Setting
        self.app = app
        self.app.title('有名人画像認識アプリ')
        self.ww = self.app.winfo_screenwidth()
        lw = 850
        self.wh = self.app.winfo_screenheight()
        lh = 650

        self.app.geometry(str(lw)+"x"+str(lh)+"+"+str(int(self.ww/2-lw/2))+"+"+str(0))

        # frame0 Setting
        self.frame0 = ttk.LabelFrame(
            self.app,
            text='Menu',
            width=1000, height=50,
            borderwidth=5,
            relief="sunken"
            )
        self.frame0.propagate(False)

        # frame1 Setting
        self.frame1 = ttk.LabelFrame(
            self.frame0,
            text='画像ファイルを選択してください',
            width=300, height=50, borderwidth=5, relief="sunken"
            )
        self.frame1.propagate(False)

        # frame2 Setting
        self.frame2 = ttk.LabelFrame(
            self.frame0,
            text='Rekognition',
            width=700, height=50,
            borderwidth=5,
            relief="sunken"
            )
        self.frame2.propagate(False)

        # Rekognition Setting
        self.buttonframe = ttk.Frame(
            self.frame2,
            width=100, height=45
            )
        self.buttonframe.propagate(False)

        # frame3 Setting
        self.frame3 = ttk.LabelFrame(
            self.app,
            text='Picture',
            width=800, height=500,
            borderwidth=5,
            relief="sunken"
            )
        self.frame3.propagate(False)

        # Layout Setting
        self.frame1.grid(row=0, column=0, padx=10)
        self.buttonframe.grid(row=0)
        self.frame2.grid(row=0, column=1, padx=10)
        self.frame0.grid(row=0, column=0, pady=10, columnspan=2)
        self.frame3.grid(row=1, column=0, padx=20, sticky=tk.W+tk.E)
        self.frame3.grid_rowconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=1)

        self.frame1_setting()
        self.frame2_setting()
        self.frame3_setting()

        self.load_open = True

        return True

    """
    Frame1 Setting '画像ファイルを選択してください'
    """
    def frame1_setting(self):
        # Widget Setting
        self.fstring = tk.StringVar()

        # Label Setting
        filename_label = ttk.Label(self.frame1, text='File名')
        filename_label.pack(side='left', anchor='center', expand=1)

        # textvariableにWidget用の変数を定義することで変数の値が変わるとテキストも動的に変わる
        self.filename_entry = ttk.Entry(self.frame1, text='', textvariable=self.fstring)
        self.filename_entry.pack(side='left', anchor='center', expand=1)

        # openFileFialog用のボタン
        button1 = ttk.Button(self.frame1, text='OPEN', command=self.open_file_dialog)
        button1.pack(side='left', anchor='center', expand=1)

        return True
    
    """
    Frame2 Setting 'Rekognition'
    """
    def frame2_setting(self):
        # Search用のボタン
        button2 = ttk.Button(self.buttonframe, text='SEARCH', command=self.image_analysis)
        button2.pack(side='left', anchor='center', expand=1)

        return True
    
    def mouse_y_scroll(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.canvas.yview_scroll(1, 'units')

        return True
    
    """
    Frame3 Setting 'Picture'
    """
    def frame3_setting(self):
        self.file_path = tk.StringVar(value='')
        # Label Setting
        label_path = ttk.Label(self.frame3, textvariable=self.file_path)
        label_path.grid(row=0, column=0, sticky=tk.W)

        # Canvas Settting
        self.canvas = tk.Canvas(self.frame3, width=750, height=450, scrollregion=(0, 0, 0, 0), bg='white')

        # Scroll bar Setting
        xscroll = tk.Scrollbar(
            self.frame3,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview)
        yscroll = tk.Scrollbar(
            self.frame3,
            orient=tk.VERTICAL,
            command=self.canvas.yview)

        # Canvas Setting
        self.canvas.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        self.canvas.bind("<ButtonPress-1>", lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind("<B1-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))
        self.canvas.bind("<MouseWheel>", self.mouse_y_scroll)

        # Layout Setting
        xscroll.grid(row=2, column=0, sticky=tk.E+tk.W)
        yscroll.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.canvas.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

        return True
    
    # 選択された画像に切り替える
    def chenge_before_img(self):
        tmpimgdir = tempfile.TemporaryDirectory()

        # 画像サイズのチェック
        if check_img(tmpimgdir, self.ans_data):
            # pillow input
            self.img = Image.open(open(self.ans_data.filename, 'rb'))
            self.width, self.height = self.img.size
            self.img = ImageTk.PhotoImage(self.img)

            self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
            self.image_on_canvas = self.canvas.create_image(
                0,  # x座標
                0,  # y座標
                image=self.img,  # 配置するイメージオブジェクトを指定
                tag="image",  # タグで引数を追加する。
                anchor=tk.NW
            )

            if self.filename_entry.get() != '':
                self.fstring.set('')
        else:
            self.fstring.set('')

        tmpimgdir.cleanup()

        self.load_open = True

        return True
    
    # label用のファイルチェック
    def check_file_path(self):
        if len(self.ans_data.filename.encode()) > 80:
            name = '.....' + self.ans_data.filename[-80:]
        else:
            name = self.ans_data.filename

        return name
    
    # Fileネームのチェック
    def check_filename(self):
        if self.ans_data.filename == '':  # ファイル選択しなかった場合はメイン画面へ戻る
            self.load_open = True
            messagebox.showerror('Error', 'Please select the file again')
        else:
            # ファイル名をチェックし、画像ファイルなら解析処理へ
            basename = os.path.basename(self.ans_data.filename)   # パス付きファイル名からファイル名のみ抽出
            ext = os.path.splitext(basename)[1]     # ファイル名から拡張子を抽出

            if ext in FILE_EXT:         # ファイルの拡張子チェック
                self.canvas.delete('image')
                name = self.check_file_path()
                self.file_path.set(name)
                self.frame3.update()
                self.chenge_before_img()       # 画像ファイルであれば解析処理へ
            else:
                messagebox.showerror('Error', 'Not an image file')
                self.fstring.set('')
            
            return True
    
    def open_file_dialog(self):
        self.ans_data = AnalysisData()       # 解析データクラス生成

        if self.filename_entry.get() == '':
            # ファイル選択ダイアログの表示
            ftyp = [
                ('画像ファイル', '*.jpg;*.png;*.jpeg;*.jpe;*.jfif;*.gif:*.tif;*.tiff;*.bmp;*.dib;*.webp'),
                ('テキストファイル', '*.txt'), ('全てのファイル', '*.*')]
            idir = ''
            self.ans_data.filename = filedialog.askopenfilename(filetypes=ftyp, initialdir=idir)
            self.fstring.set(self.ans_data.filename)
        else:
            self.ans_data.filename = self.filename_entry.get()

        self.check_filename()
        self.analysis_result = True

        return True

    # 解析後の画像に切り替える
    def change_after_img(self):
        tmpimgdir = tempfile.TemporaryDirectory()

        tmpfilename = tmpimgdir.name + '/after_img.jpg'
        cv2.imwrite(tmpfilename, self.ans_data.img)

        self.ans_data.filename = tmpfilename

        # pillow input
        self.img = Image.open(open(self.ans_data.filename, 'rb'))
        self.width, self.height = self.img.size
        self.img = ImageTk.PhotoImage(self.img)

        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        self.canvas.itemconfig(
            self.image_on_canvas,
            image=self.img
        )

        tmpimgdir.cleanup()

        self.load_open = True

        return True

    def image_analysis(self):
        # 画像解析を行う
        analysis_rekogniton(self.ans_data)

        if self.analysis_result:
            # メイン処理
            main_proc(self.ans_data)

            # 解析後の画像に切り替える
            if self.change_after_img():
                self.app.update()

            self.analysis_result = False
        
        return True



# get
def get_font_rate(ans_data):
    # フォントの比率を設定
    if int(8 * ans_data.rate) > 12:
        font_rate = int(8 * ans_data.rate)
    # フォントの比率を設定
    else:
        font_rate = 12

    return font_rate

# get
def get_img_rate(ans_data, r1, r2):
    # ボックスの比率を設定
    if int(r1 * ans_data.rate) > r2:
        img_rate = int(r1 * ans_data.rate)
    # ボックスの比率を設定
    else:
        img_rate = r2

    return img_rate

# get
def get_cname(celeb):
    if celeb.confidence >= CONFIDENCE:     # 一致信頼度が75%以上のものを認識結果として採用する
        name = celeb.name
    else:
        name = 'Unknown'

    # The text string can be a maximum of 20 bytes long.
    if len(name.encode()) > ERROR_CDRAW:
        name = name[:17] + '...'

    return name

# get
def get_oname(name):
    # The text string can be a maximum of 25 bytes long.
    if len(name.encode()) > ERROR_ODRAW:
        name = name[:22] + '...'

    return name

# get
def get_top(human, img_rate):
    # put box on image in position (0, 0)
    if (human.top - img_rate) > 0:
        top = human.top - img_rate
    else:
        top = 0

    return top

# 有名人の顔枠表示
def displaying_face_boxes(ans_data):
    img = ans_data.img
    font_rate = get_font_rate(ans_data)
    img_rate = get_img_rate(ans_data, 15, 20)

    # 有名人の顔枠
    for celeb in ans_data.celeb:
        img = cv2.rectangle(img, (celeb.left, celeb.top),
                            (celeb.left + celeb.width, celeb.top + celeb.height),
                            (0, 0, 255), thickness=1)
        img = cv2.rectangle(img, (celeb.left + 4, celeb.top + 4),
                            (celeb.left + celeb.width - 4, celeb.top + celeb.height - 4),
                            (255, 0, 0), thickness=1)

    # Unknownの顔枠
    for unknown in ans_data.unknown:
        img = cv2.rectangle(img, (unknown.left, unknown.top),
                            (unknown.left + unknown.width, unknown.top + unknown.height),
                            (0, 0, 255), thickness=1)
        img = cv2.rectangle(img, (unknown.left + 4, unknown.top + 4),
                            (unknown.left + unknown.width - 4, unknown.top + unknown.height - 4),
                            (255, 0, 0), thickness=1)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    font = ImageFont.truetype(FUNTTTF, font_rate)

    # 有名人の名前表示
    for celeb in ans_data.celeb:
        name = get_cname(celeb)
        # get text size
        text_size = font.getsize(name)
        # set box size + 5px margins
        box_size = (text_size[0] + 2, text_size[1] + 2)
        # create image with correct size and #90ee90 background
        box_img = Image.new('RGB', box_size, '#90ee90')
        # put text on box with 10px margins
        box_draw = ImageDraw.Draw(box_img)
        box_draw.text((1, 1), name, font=font, fill='#000000')
        # put box on image in position (0, 0)
        top = get_top(celeb, img_rate)
        image.paste(box_img, (celeb.left, top))

    # Unknownの名前表示
    for unknown in ans_data.unknown:
        name = 'Unknown'
        # get text size
        text_size = font.getsize(name)
        # set box size + 5px margins
        box_size = (text_size[0] + 2, text_size[1] + 3)
        # create image with correct size and #90ee90 background
        box_img = Image.new('RGB', box_size, '#90ee90')
        # put text on box with 10px margins
        box_draw = ImageDraw.Draw(box_img)
        box_draw.text((1, 1), name, font=font, fill='#000000')
        # put box on image in position (0, 0)
        top = get_top(unknown, img_rate)
        image.paste(box_img, (unknown.left, top))

    ans_img = np.array(image)

    return ans_img

# 物体の枠表示
def displaying_object_boxes(ans_data):
    img = ans_data.img
    font_rate = get_font_rate(ans_data)
    img_rate = get_img_rate(ans_data, 4, 5)

    # 物体の枠
    for info in ans_data.object:
        img = cv2.rectangle(img, (info.left, info.top),
                            (info.left + info.width, info.top + info.height),
                            (255, 0, 255), thickness=1)
        img = cv2.rectangle(img, (info.left + 4, info.top + 4),
                            (info.left + info.width - 4, info.top + info.height - 4),
                            (0, 255, 255), thickness=1)
 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    font = ImageFont.truetype(FUNTTTF, font_rate)

    for info in ans_data.object:
        name = info.name
        name = get_oname(name)
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
        top = info.top + img_rate
        left = info.left + img_rate
        image.paste(box_img, (left, top))

    ans_img = np.array(image)

    return ans_img

# メイン処理
def main_proc(ans_data):
    # 画像ファイルの加工
    ans_data.img = displaying_face_boxes(ans_data)
    ans_data.img = displaying_object_boxes(ans_data)

    return True

# 入力画像のリサイズ処理
def image_resize_check(ans_data):
    img_height, img_width = ans_data.img.shape[:2]  # 解析対象画像の高さと幅を取得

    max_size = max(img_height, img_width)

    if max_size > IMAGE_MAX:
        ans_data.rate = IMAGE_MAX / max_size

        ans_data.img = cv2.resize(ans_data.img, \
        (int(img_width * ans_data.rate), \
        int(img_height * ans_data.rate)))

    if max_size < IMAGE_MIN:
        ans_data.rate = IMAGE_REG / max_size

        ans_data.img = cv2.resize(ans_data.img, \
        (int(img_width * ans_data.rate), \
        int(img_height * ans_data.rate)))

    return True

# 日本語ファイル名
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except PermissionError as e:
        print(e)
        print("Can't open the file")
        messagebox.showerror('Error', "PermissionError: Can't open the file")
        return None
    except Exception as e:
        print(e)
        print("Can't open the file")
        messagebox.showerror('Error', "Exception: Can't open the file")
        return None

# 画像サイズのチェック
def check_img(tmpimgdir, ans_data):
    # 画像ファイルの表示
    img = imread(ans_data.filename)

    if img is not None:
        ans_data.img = img              # 解析対象画像のイメージデータを格納

        # 画像が制限を超えていないかどうか
        image_resize_check(ans_data)

         # 画像が制限を超えているとき
        if ans_data.rate > 0:
            tmpfilename = tmpimgdir.name + '/before_img.jpg'
            cv2.imwrite(tmpfilename, ans_data.img)

            ans_data.filename = tmpfilename

        return True

# 有名人の情報を取得する
def get_celebrity_list(response, img):

    img_height, img_width = img.shape[:2]  # 解析対象画像の高さと幅を取得
    celeb_list = []

    for celebrity in response['CelebrityFaces']:
        celeb = DetectInfo()
        celeb.name = celebrity['Name']
        celeb.confidence = celebrity['MatchConfidence']
        # 顔の位置情報を算出
        celeb.top = int(img_height * celebrity['Face']['BoundingBox']['Top'])
        celeb.left = int(img_width * celebrity['Face']['BoundingBox']['Left'])
        celeb.height = int(img_height * celebrity['Face']['BoundingBox']['Height'])
        celeb.width = int(img_width * celebrity['Face']['BoundingBox']['Width'])
        # 有名人のurlを取得
        celeb.url = celebrity['Urls']
        celeb_list.append(celeb)

    return celeb_list

# 有名人以外の情報を取得
def get_unknown_list(response, img):
    img_height, img_width = img.shape[:2]  # 解析対象画像の高さと幅を取得
    unknown_list = []

    for unknownface in response['UnrecognizedFaces']:
        unknown = DetectInfo()
        unknown.name = 'Unknown'
        # 顔の位置情報を算出
        unknown.top = int(img_height * unknownface['BoundingBox']['Top'])
        unknown.left = int(img_width * unknownface['BoundingBox']['Left'])
        unknown.height = int(img_height * unknownface['BoundingBox']['Height'])
        unknown.width = int(img_width * unknownface['BoundingBox']['Width'])
        unknown_list.append(unknown)

    return unknown_list

# 物体の情報を取得
def get_object_list(response, img):
    img_height, img_width = img.shape[:2]  # 解析対象画像の高さと幅を取得
    object_list = []

    for obj in response['Labels']:
        for instance in obj['Instances']:
            info = DetectInfo()
            info.name = obj['Name']
            info.parent = obj['Parents']
            info.confidence = instance['Confidence']
            # 物体の位置情報を算出
            info.top = int(img_height * instance['BoundingBox']['Top'])
            info.left = int(img_width * instance['BoundingBox']['Left'])
            info.height = int(img_height * instance['BoundingBox']['Height'])
            info.width = int(img_width * instance['BoundingBox']['Width'])
            object_list.append(info)

    return object_list

# awsのrekognitionを用いて、検出するライブラリ
def analysis_rekogniton(ans_data):
    with open(ans_data.filename, 'rb') as file_image:
        source_bytes = file_image.read()    # 画像ファイルを読み込み、バイト列を取得

    try:
        # 画像のバイト列をrekognition.recognize_celebritiesで解析
        rekognition = boto3.client('rekognition')
        response = rekognition.recognize_celebrities(Image={'Bytes': source_bytes})
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        print("Can't rekognition the image")
        messagebox.showerror('Error', "BotoCoreError, ClientError: Can't rekognition the image")
        sys.exit(-1)

    # rekognitionの検出結果から人物情報(名前、顔位置情報)を取得
    celeb_list = get_celebrity_list(response, ans_data.img)
    unknown_list = get_unknown_list(response, ans_data.img)

    try:
        # 画像のバイト列をrekognition.detect_labelsで解析
        response = rekognition.detect_labels(Image={'Bytes': source_bytes}, MinConfidence=75.0)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        print("Can't rekognition the image")
        messagebox.showerror('Error', "BotoCoreError, ClientError: Can't rekognition the image")
        sys.exit(-1)

    # rekognitionの検出結果から物体情報を取得
    object_list = get_object_list(response, ans_data.img)

    ans_data.celeb = celeb_list     # 検出した人物情報リストを格納
    ans_data.unknown = unknown_list # 検出したUnknownリストを格納
    ans_data.object = object_list # 検出した物体情報リストを格納

    return True

def main():
    # Window Setting
    app = tk.Tk()
    # Window size non resizable
    app.resizable(width=False, height=False)
    # Function make
    gui_app = GuiApp()
    gui_app.make_app(app)
    # mainloop windows open
    app.mainloop()

if __name__ == '__main__':
    main()
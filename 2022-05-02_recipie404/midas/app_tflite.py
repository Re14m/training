import copy
import time

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

import tkinter as tk
import tkinter.simpledialog as simpledialog


def mouse_callback(event, x, y, flags, param):
    # マウス座標、距離相対値、距離絶対値、キャリブレーション座標 保持用のグローバル変数
    global mouse_point
    global relative_value_list, absolute_value_list, calibration_p_list
    global depth_map

    mouse_point = [x, y]

    # マウス左クリック
    if event == cv2.EVENT_LBUTTONDOWN:
        # 実測値を入力
        input_data = simpledialog.askstring(
            "",
            "実測値(cm)を入力",
        )
        try:
            absolute_value = int(float(input_data))

            # 距離絶対値
            absolute_value_list.append(absolute_value)
            # 距離相対値
            relative_value_list.append(depth_map[y][x])
            # キャリブレーション座標
            calibration_p_list.append([x, y])
        except:
            # 数値以外
            pass


def run_inference(interpreter, image):
    image_width, image_height = image.shape[1], image.shape[0]

    # リサイズ
    resize_image = cv2.resize(image, (256, 256))

    # 正規化
    resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB) / 255.0
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    resize_image = (resize_image - mean) / std

    # 形状変更
    resize_image = resize_image.reshape(1, 256, 256, 3)

    # tensor形式へ変換
    tensor = tf.convert_to_tensor(resize_image, dtype=tf.float32)

    # 推論
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], tensor)
    interpreter.invoke()
    result = interpreter.get_tensor(output_details[0]['index'])

    # 余分な次元を削除し、入力画像のサイズへリサイズ
    result = np.squeeze(result)
    result_depth_map = cv2.resize(result, (image_width, image_height))

    return result_depth_map


def linear_approximation(x, y):
    # 最小二乗法で1次関数(y = ax + b)の係数a, bを求める
    n = len(x)
    a = ((np.dot(x, y) - y.sum() * x.sum() / n) /
         ((x**2).sum() - x.sum()**2 / n))
    b = (y.sum() - a * x.sum()) / n
    return a, b


def draw_info(
    image,
    depth_map_,
    elapsed_time,
    mouse_point_,
    relative_value_list_,
    absolute_value_list_,
    calibration_p_list_,
    a=None,
    b=None,
):
    # 描画用フレーム作成
    rgb_frame = copy.deepcopy(image)
    depth_frame = copy.deepcopy(depth_map_)

    # 疑似カラー用の値レンジ調整
    depth_max = depth_frame.max()
    depth_frame = ((depth_frame / depth_max) * 255).astype(np.uint8)
    depth_frame = cv2.applyColorMap(depth_frame, cv2.COLORMAP_TURBO)

    # マウスポインタ上の推論値描画
    if mouse_point_ is not None:
        point_x = mouse_point_[0]
        point_y = mouse_point_[1]

        # キャリブレーション済の場合はcm表記で描画
        if a is not None and b is not None:
            display_d = "{0:.1f}".format(
                (((1 / depth_map_[point_y][point_x] * a)) + b)) + "cm"

            # RGB画像
            cv2.circle(rgb_frame, (point_x, point_y),
                       3, (0, 255, 0),
                       thickness=1)
            cv2.putText(rgb_frame, display_d, (point_x, point_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
                        cv2.LINE_AA)

            # Depth画像
            cv2.circle(depth_frame, (point_x, point_y),
                       3, (255, 255, 255),
                       thickness=1)
            cv2.putText(depth_frame, display_d, (point_x, point_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
                        cv2.LINE_AA)

    # キャリブレーションポイント描画
    for index, calibration_p in enumerate(calibration_p_list_):
        point_x = calibration_p[0]
        point_y = calibration_p[1]

        # RGB画像
        cv2.circle(rgb_frame, (point_x, point_y), 3, (0, 255, 0), thickness=1)
        cv2.putText(
            rgb_frame, "{0:.1f}".format(relative_value_list_[index]) + " : " +
            str(absolute_value_list_[index]) + "cm", (point_x, point_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)

        # Depth画像
        cv2.circle(depth_frame, (point_x, point_y),
                   3, (255, 255, 255),
                   thickness=1)
        cv2.putText(
            depth_frame, "{0:.1f}".format(relative_value_list_[index]) +
            " : " + str(absolute_value_list_[index]) + "cm",
            (point_x, point_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
            (255, 255, 255), 1, cv2.LINE_AA)

    # 推論時間描画
    # RGB画像
    cv2.putText(rgb_frame,
                "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
                cv2.LINE_AA)
    # Depth画像
    cv2.putText(depth_frame,
                "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
                cv2.LINE_AA)

    return rgb_frame, depth_frame


if __name__ == "__main__":
    # マウス座標、距離相対値、距離絶対値、キャリブレーション座標 保持用のグローバル変数
    global mouse_point
    global relative_value_list, absolute_value_list, calibration_p_list
    global depth_map
    mouse_point = None
    relative_value_list, absolute_value_list, calibration_p_list = [], [], []
    depth_map = None

    # モデルロード
    interpreter = tf.lite.Interpreter(
        model_path="lite-model_midas_v2_1_small_1_lite_1.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']

    # カメラ準備
    cap = cv2.VideoCapture(0)

    # Tkinter初期化
    root = tk.Tk()
    root.withdraw()

    # OpenCVウィンドウ初期化、マウス操作用のコールバックを登録
    rgb_window_name = 'rgb'
    cv2.namedWindow(rgb_window_name)
    cv2.setMouseCallback(rgb_window_name, mouse_callback)

    depth_window_name = 'depth'
    cv2.namedWindow(depth_window_name)
    cv2.setMouseCallback(depth_window_name, mouse_callback)

    while True:
        start_time = time.time()

        # カメラキャプチャ
        ret, frame = cap.read()
        if not ret:
            continue

        # Depth推定
        depth_map = run_inference(interpreter, frame)

        # 相対距離と絶対距離を最小二乗法を用いて線形近似
        a, b = None, None
        if len(calibration_p_list) >= 2:
            a, b = linear_approximation(
                np.array([(1 / v) for v in relative_value_list]),
                np.array(absolute_value_list),
            )

        elapsed_time = time.time() - start_time

        # 情報描画
        rgb_frame, depth_frame = draw_info(
            frame,
            depth_map,
            elapsed_time,
            mouse_point,
            relative_value_list,
            absolute_value_list,
            calibration_p_list,
            a,
            b,
        )

        cv2.imshow(rgb_window_name, rgb_frame)
        cv2.imshow(depth_window_name, depth_frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
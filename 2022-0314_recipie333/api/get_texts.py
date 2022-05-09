#!/usr/bin/env python
# coding: utf-8

from flask import request, jsonify, Blueprint
import numpy as np

from lib.function import get_data, cos_sim
from lib.nlp_function import text_to_vector

api = Blueprint("api", __name__)

#取得文章をベクトルに変換
data_path = "data/text.txt"
text_list = get_data(data_path)
text_vector_list = text_to_vector(text_list)

@api.route("/get_texts", methods=["GET"])
def get_texts():
    #類似度の閾値
    thred_value = 0.8

    text = request.args.get('value', '')

    #文章をベクトル化
    text_vector = text_to_vector([text])[0]

    cos_sim_list = []
    for i, t_v in enumerate(text_vector_list):
        #類似度取得
        sim_value = cos_sim(t_v, text_vector)
        #類似度が閾値以上の文章と類似度をリストに格納
        if sim_value >= thred_value:
            cos_sim_list.append({"text":text_list[i], "value":str(sim_value)})

    #類似度が降順に並び替え
    cos_sim_list = sorted(cos_sim_list, key=lambda x: x["value"], reverse=True)

    return jsonify(cos_sim_list)


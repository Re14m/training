#!/usr/bin/env python
# coding: utf-8

from transformers import BertJapaneseTokenizer, BertModel
import torch

MODEL_NAME = "cl-tohoku/bert-base-japanese-whole-word-masking"
max_length = 256

tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)

def text_to_vector(text_list):
    texts_vector = []

    for text in text_list:
        # 入力文章をエンコード
        encoding = tokenizer(text, max_length=max_length, padding="max_length", truncation=True, return_tensors="pt")
        attention_mask = encoding["attention_mask"]

        with torch.no_grad():
            # BERTで計算
            output = model(**encoding)
            last_hidden_state = output.last_hidden_state
            averaged_hidden_state = (last_hidden_state * attention_mask.unsqueeze(-1)).sum(1) / attention_mask.sum(1, keepdim=True)

        texts_vector.append(averaged_hidden_state[0].numpy())
    return texts_vector
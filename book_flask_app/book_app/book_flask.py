from flask import Flask, render_template, request, Response, make_response
from urllib import parse
import pickle
import pandas as pd
import xgboost
import numpy
import json
import sys
import codecs

# string = parse.unquote(data5, 'utf8')
# 위 코드는 html에서 데이터 입력하고 받을 때 이 때 데이터는 ascii 코드로 입력받음
# 약간 외계어 단어 형태가 되서 알맞은 형태가 아니기 때문에 따라서 이를 제대로 한글 형태로
# 받기 위해선 다시 utf-8 형태로 다시 바꿔줘야 알맞은 한글 형태로 바꿔줌.


# stdout의 인코딩을 UTF-8로 강제 변환한다
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


df = pd.read_csv('C:/Users/user/yes24_save.csv', encoding='utf-8-sig')

with open('C:/Users/user/xgbmodel.pkl','rb') as pickle_file:
        model = pickle.load(pickle_file)
    
        

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def index_():
    # args = request.form
    # string = args['category']
    data1 = request.values.get("price")
    data2 = request.values.get("weight")
    data3 = request.values.get("total_page")
    data4 = request.values.get("review_count")
    data5 = request.values.get("category")
    string = parse.unquote(data5, 'utf8')
    arr = [int(data1), int(data2), int(data3), int(data4), string]
    pred_ = model.predict([arr])
    list_ = df[(df['판매 지수'] >= int(pred_[0])) & (df['카테고리'] == arr[4])]
    link_ = list_.sort_values(by='판매 지수', ascending=False).tail(1)
    bookname = link_['책 이름']
    ref = link_['링크']
    bn = bookname[bookname.index[0]]
    re_link = ref[ref.index[0]]
    return render_template('prediction.html', bookname=bn, link=re_link)

if __name__ == "__main__":
    app.run(debug=True)
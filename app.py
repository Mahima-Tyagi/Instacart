# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12by0XtLMzzKNmSQpjo0K5xFFV6ykWcZj
"""

import pandas as pd
import pickle
from flask import Flask,jsonify,request, render_template,Response
import flask

model=pickle.load(open('model.sav','rb'))
product_name_dict=pickle.load(open('products_id_name.pkl','rb'))
df=pickle.load(open('test_final.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
  '''dislay index.html file when starts app'''
  return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
  '''when called predict with arguement'''
  to_predict_list=[int(x) for x in request.form.values()]
  ord_num=to_predict_list[0]
  df2=df[df.order_id==ord_num]
  datapt=df2.drop(['order_id'],axis=1)
  #resetting index
  datapt=datapt.set_index(['user_id','product_id'])
  #predicting
  pred=model.predict(datapt)
  datapt['pred']=pred
  datapt=datapt.reset_index()  
  #to return products
  product_ids=datapt[datapt.pred==1]['product_id']
  output=[]
  for i in list(product_ids):
      if len(product_ids)==0:
        return Response(render_template('output.html',data=['Nothing']))
      output.append(product_name_dict['product_name'][i])
  return Response(render_template('output.html',data=output))

if __name__=='__main__':
  app.run(host='0.0.0.0',port=5000)
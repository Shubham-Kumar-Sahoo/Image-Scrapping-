from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/image" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:
                        query = request.form['content'].replace(" ","")

                        dir="images/"
                        if not os.path.exists(dir):
                                os.makedirs(dir)

                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

                        response = requests.get(f"https://www.google.com/search?sxsrf=AB5stBiwVYm-lq4Gw5KUL8fZoalML98pfQ:1688931100672&q={query}&tbm=isch&sa=X&ved=2ahUKEwiX2bjSroKAAxVZx2EKHT3uAK4Q0pQJegQIDBAB&biw=1276&bih=577&dpr=1.5")
                        html=BeautifulSoup(response.content,'html.parser')

                        img = html.find_all('img')

                        del img[0]

                        img_db=[]
                        for i in img:
                                img_url=i['src']
                                image= requests.get(img_url)
                                img_data=image.content
                                dict={'imgurl':img_url}
                                img_db.append(dict)
                                with open (os.path.join(dir,f"{query}_{img.index(i)}.jpg"),"wb") as f:
                                        f.write(img_data)

                        # return "image laoded"
                        return render_template('result.html', results=img_db[0:len(img_db)-1])
                except Exception as e:
                        logging.info(e)
                        return 'something is wrong'
                        

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)

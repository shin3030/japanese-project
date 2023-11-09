from flask import Flask,render_template,request
import requests
url = 'http://lingpu.im.tku.edu.tw:35130/api/chat'

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("beginpage.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/get",methods=["GET","POST"])
def test():
    msg=request.form["msg"]
    print("Received message:", msg)
    input=msg
    return chat_respone(input)

def chat_completion(prompt, model_engine="gpt35", temperature=0.7, top_p=0.95, max_tokens=1024):
    args = {
        'prompt': prompt,
        'model_engine': model_engine,
        'temperature': temperature,
        'top_p': top_p,
        'max_tokens': max_tokens
    }
    
    response = requests.post(url, json=args)

    response_json = response.json()
    message = response_json['message']

    return message
def chat_respone(text):
    prompt =text+"只能用日文回答，並在下行提供繁體中文翻譯"
    response = chat_completion(prompt)
    return response

@app.route("/mintest")
def mintest():
    return render_template('mintest.html')

@app.route("/50")
def letter():
    return render_template("50.html")
@app.route("/map")
def jmap():
    return render_template("map.html")
@app.route("/N5voc")
def N5voc():
    return render_template("N5voc.html")
@app.route("/N5gra")
def N5gra():
    return render_template("N5gra.html")
@app.route("/story")
def story():
    return render_template("story.html")
@app.route("/ReadAloud")
def read():
    return render_template("ReadAloud.html")

if __name__=='__main__':
    app.run(debug=True)


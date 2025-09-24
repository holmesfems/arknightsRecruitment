from recruitment import recruitment,recruitFromOCR
import os

from flask import Flask,request
import json

port = int(os.environ["PORT"])
print(f"Server port = {port}")

app = Flask(__name__)

@app.route('/recruitment/', methods=['POST'])
def doRecruitment():
    jsonStr = request.data.decode('utf-8')  # デコード
    param = json.loads(jsonStr)
    text = param["text"]
    matchTag = recruitFromOCR.matchTag(text)
    if(matchTag.isEmpty()): return "タグがありません"
    reply = recruitment.recruitDoProcess(matchTag.matches,4,matchTag.isGlobal)
    return reply

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
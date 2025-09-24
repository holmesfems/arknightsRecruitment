from recruitment import recruitment,recruitFromOCR
import os

from flask import Flask

port = int(os.environ["PORT"])
print(f"Server port = {port}")

app = Flask(__name__)

@app.route('/recruitment/<text>', methods=['GET'])
def doRecruitment(text):
    matchTag = recruitFromOCR.matchTag(text)
    if(matchTag.isEmpty()): return "タグがありません"
    reply = recruitment.recruitDoProcess(matchTag.matches,4,matchTag.isGlobal)
    return reply

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
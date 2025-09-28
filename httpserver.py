from recruitment import recruitment,recruitFromOCR
import os
import uvicorn
from fastapi import FastAPI
#from flask import Flask,request
import json
from pydantic import BaseModel

port = int(os.environ["PORT"])
print(f"Server port = {port}")

app = FastAPI()

class TagData(BaseModel):
    text: str

class TagReplyData(BaseModel):
    title: str
    reply: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/recruitment/',response_model=TagReplyData)
def doRecruitment(data:TagData):
    text = data.text
    #text = request.args.get("text")
    print(text)
    matchTag = recruitFromOCR.matchTag(text)
    if(matchTag.isEmpty()): return "タグがありません"
    reply = recruitment.recruitDoProcess(matchTag.matches,4,matchTag.isGlobal)
    return reply

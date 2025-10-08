from recruitment import recruitment,recruitFromOCR
import os
import uvicorn
from fastapi import FastAPI
#from flask import Flask,request
import json
from pydantic import BaseModel,Field

port = int(os.environ["PORT"])
print(f"Server port = {port}")

app = FastAPI()

class TagData(BaseModel):
    text: str = Field(description="The raw data of OCR result. Each tag should be separated by line breaks")

class TagReplyData(BaseModel):
    title: str = Field(description="The recognized tags")
    reply: str = Field(description="The result to be displayed on screen")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/recruitment/',response_model=TagReplyData,description="Extract tags of arknights public recruitment from raw OCR data, and calculate high-rare tag combination")
def doRecruitment(data:TagData):
    text = data.text
    #text = request.args.get("text")
    #print(text)
    matchTag = recruitFromOCR.matchTag(text)
    if(matchTag.isEmpty()): return TagReplyData(title="エラー",reply="タグがありません")
    reply = recruitment.recruitDoProcess(matchTag.matches,4,matchTag.isGlobal)
    return TagReplyData(title=reply.embbedTitle,reply=reply.responseForAI)

class HighStarData(BaseModel):
    star: int = Field(description="The raw data of OCR result. Each tag should be separated by line breaks")

@app.post('/showHighStars/')
def doRecruitment(data:HighStarData):
    star = data.star
    #text = request.args.get("text")
    reply = recruitment.showHighStars(star)
    return {"title":reply.embbedTitle,"replyForAI":reply.responseForAI,"replyToShow":"".join(reply.embbedContents)}
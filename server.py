import os,base64
from pathlib import Path
from fastapi import FastAPI,UploadFile,File,Form,HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
BASE=Path(__file__).resolve().parent
MODEL=os.getenv("OPENAI_MODEL","gpt-5.6")
KEY=os.getenv("OPENAI_API_KEY")
app=FastAPI(title="Study Assistant GPT-5.6")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
class AskRequest(BaseModel):
    user_id:str="user1"; question:str; subject:str="عمومی"; mode:str="آموزشی"; book_code:str=""
def instructions(subject,mode,book):
    return f"""تو کمک‌یار نهم، معلم خصوصی دانش‌آموز پایه نهم هستی.
درس: {subject}
حالت پاسخ: {mode}
کتاب: {book or "مشخص نشده"}
فارسی، روشن و متناسب با پایه نهم جواب بده. مسائل را مرحله‌به‌مرحله توضیح بده.
اگر متن یا صفحه کتاب را نداری، حدس نزن و بگو عکس/متن صفحه لازم است."""
def get_client():
    if not KEY: raise HTTPException(503,"OPENAI_API_KEY روی سرور تنظیم نشده است.")
    return OpenAI(api_key=KEY)
@app.get("/health")
def health(): return {"ok":bool(KEY),"model":MODEL}
@app.get("/")
def home(): return FileResponse(BASE/"study_assistant.html")
@app.post("/v1/ask")
def ask(req:AskRequest):
    if not req.question.strip(): raise HTTPException(400,"سؤال خالی است.")
    try:
        r=get_client().responses.create(model=MODEL,instructions=instructions(req.subject,req.mode,req.book_code),input=req.question)
        return {"answer":r.output_text,"model":MODEL}
    except Exception as e: raise HTTPException(500,f"خطا در ارتباط با OpenAI: {e}")
@app.post("/v1/ask-image")
async def ask_image(user_id:str=Form("user1"),question:str=Form(""),subject:str=Form("عمومی"),mode:str=Form("آموزشی"),book_code:str=Form(""),image:UploadFile=File(...)):
    data=await image.read()
    if len(data)>10*1024*1024: raise HTTPException(413,"حجم عکس بیشتر از 10MB است.")
    typ=image.content_type or "image/jpeg"; url=f"data:{typ};base64,{base64.b64encode(data).decode()}"
    try:
        r=get_client().responses.create(model=MODEL,instructions=instructions(subject,mode,book_code),input=[{"role":"user","content":[{"type":"input_text","text":question or "این سؤال را از روی عکس حل و توضیح بده."},{"type":"input_image","image_url":url}]}])
        return {"answer":r.output_text,"model":MODEL}
    except Exception as e: raise HTTPException(500,f"خطا در پردازش عکس: {e}")

from ast import Bytes
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from summary_service import summarizer_main
from PyPDF2 import PdfFileReader
from io import BytesIO


model = summarizer_main.get_summary_model()
app = FastAPI()


class ArticleModel(BaseModel):
    body: str
    req_lines: int = 5


@app.get("/")
def root():
    return "Hello World"


@app.post("/summarize")
async def receivePdf(file: UploadFile):
    print(file.filename)
    docText = await processPdf(file)
    summary = model(docText, ratio=0.05)
    return summary


async def processPdf(file: UploadFile):
    bytes = BytesIO(await file.read())
    pdf = PdfFileReader(bytes)
    doc_text = ""
    for pageNo in range(pdf.numPages):
        page = pdf.getPage(pageNo)
        text = page.extractText()
        text = " ".join(text.split("\n"))
        doc_text += text
    return doc_text

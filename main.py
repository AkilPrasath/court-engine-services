from fastapi import FastAPI,  UploadFile
from PyPDF2 import PdfFileReader
from io import BytesIO
import requests

app = FastAPI()

summarization_url = "http://f1b4-34-75-184-202.ngrok.io"


@app.get("/")
def root():
    return "Hello World"


@app.post("/summarize")
async def receivePdf(file: UploadFile):
    summary = {"error": "error"}
    print(file.filename)
    docText = await processPdf(file)
    api = summarization_url+"/summarize"
    print("APII: {0}".format(api))
    summary = requests.post(api, json={"text": docText})

    return {"result": summary.text}


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

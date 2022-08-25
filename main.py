import uuid
from fastapi import FastAPI,  UploadFile

from PyPDF2 import PdfFileReader
from io import BytesIO
import requests
from elasticSearch import ElasticSearchUtil
from doc_preprocessor.documentParser import DocumentParser
import uvicorn

from elasticSearchModel import SearchModel
from mongodb.mongo_util import uploadToMongo
app = FastAPI()

summarization_url = "http://c8c8-34-74-123-138.ngrok.io"


@app.get("/")
def root():
    return "Hello World"


@app.post("/pdfUpload")
async def uploadPdf(file: UploadFile):
    parser = DocumentParser(await processPdf(file))
    parsedMap = parser.parse()
    elasticSearch = ElasticSearchUtil()
    id = uuid.uuid4()
    await uploadToMongo(file, id)
    return elasticSearch.insertToIndex(parsedMap, id)


@app.post("/summarize")
async def receivePdf(file: UploadFile):
    summary = {"error": "error"}
    print(file.filename)
    docText = await processPdf(file)
    api = summarization_url+"/summarize"
    print("APII: {0}".format(api))
    summary = requests.post(api, json={"text": docText})

    return {"result": summary.text}


@app.get("/search")
def search(searchModel: SearchModel):
    elasticSearch = ElasticSearchUtil()
    result = elasticSearch.search(searchModel)
    return result


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

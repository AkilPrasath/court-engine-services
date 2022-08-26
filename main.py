import uuid
from fastapi import FastAPI,  UploadFile

from PyPDF2 import PdfFileReader
from io import BytesIO
import requests
from elasticSearch import ElasticSearchUtil
from doc_preprocessor.documentParser import DocumentParser
from pydantic import BaseModel
from elasticSearchModel import SearchModel
from mongodb.mongo_util import searchSections, uploadToMongo
from fastapi.middleware.cors import CORSMiddleware

from sectionModel import SectionModel
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
summarization_url = "http://c8c8-34-74-123-138.ngrok.io"


@app.get("/")
def root():
    return "Hello World"


@app.post("/pdfUpload")
async def uploadPdf(file: UploadFile):
    print("sadfasdfdsjkfsaldgfhslfujd")
    bytes = BytesIO(await file.read())
    parser = DocumentParser(await processPdf(bytes))
    parsedMap = parser.parse()
    id = uuid.uuid4()
    elasticSearch = ElasticSearchUtil()
    await uploadToMongo(bytes, id)
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


@app.post("/search")
def search(searchModel: SearchModel):
    elasticSearch = ElasticSearchUtil()
    print(searchModel.dict)
    result = elasticSearch.search(searchModel)
    return result


@app.post("/section")
def section(sectionModel: SectionModel):
    finalMap = searchSections(sectionModel.sections)
    return finalMap


async def processPdf(bytes):
    pdf = PdfFileReader(bytes)
    doc_text = ""
    for pageNo in range(pdf.numPages):
        page = pdf.getPage(pageNo)
        text = page.extractText()
        text = " ".join(text.split("\n"))
        doc_text += text
    return doc_text

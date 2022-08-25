import pymongo
import gridfs
from io import BytesIO
from fastapi import UploadFile

conn_str = "mongodb+srv://akil:akil@court-engine-atlas.lavyisw.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)


async def uploadToMongo(file: UploadFile, id):
    client = pymongo.MongoClient(conn_str)
    db = client['court-engine-db']
    fs = gridfs.GridFS(db)
    bytes = BytesIO(await file.read())
    fid = fs.put(bytes)
    print("file ID:")
    print(fid)

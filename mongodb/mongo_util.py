import pymongo
import gridfs

conn_str = "mongodb+srv://akil:akil@court-engine-atlas.lavyisw.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)


async def uploadToMongo(bytes, id):
    client = pymongo.MongoClient(conn_str)
    db = client['court-engine-db']
    fs = gridfs.GridFS(db)

    fid = fs.put(bytes)

    collection = db["judgements"]

    collection.insert_one({"file_id": str(fid), "doc_id": str(id)})

    # print(fs.get(fid).read())

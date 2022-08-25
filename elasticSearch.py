
import uuid
import requests

from doc_preprocessor.grammar import getProcessedQueryText
from elasticSearchModel import SearchModel
base_url = "http://localhost:9200/"
indexName = "judgements/"


class ElasticSearchUtil():
    def __init__(self) -> None:
        pass

    def insertToIndex(self, doc, id):

        response = requests.post(base_url+indexName+"_doc/"+str(id), json=doc)
        return response.text

    def search(self, searchModel: SearchModel):
        processedQueryText = getProcessedQueryText(
            queryText=searchModel.queryText)
        query = self.generateFullQuery(searchModel)
        response = requests.post(base_url+indexName+"_search", json=query)
        return response.json()

    def generateFullQuery(self, searchModel: SearchModel):
        baseQuery = {}
        queryList = []
        queryList.extend(self.generateSingleQuery(
            searchModel.respondent, "respondent"))
        queryList.extend(self.generateSingleQuery(
            searchModel.petitioner, "petitioner"))
        queryList.extend(self.generateSingleQuery(
            searchModel.section, "sections"))
        queryList.extend(self.generateSingleQuery(
            searchModel.text_sections, "textSections"))
        baseQuery["query"] = {
            "bool": {
                "must": queryList
            }
        }
        return baseQuery

    def generateSingleQuery(self, stringList, fieldName):  # level match, filter
        subQuery = []
        for pet in stringList:
            if pet != "":
                subQuery.append(
                    {
                        "match": {
                            fieldName: pet
                        }
                    }
                )
        return subQuery

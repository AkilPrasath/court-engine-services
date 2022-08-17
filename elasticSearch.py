
import uuid
import requests
base_url = "http://localhost:9200/"
indexName = "judgements/_doc/"


class ElasticSearchUtil():
    def __init__(self) -> None:
        pass

    def insertToIndex(self, doc):
        id = uuid.uuid4()
        response = requests.post(base_url+indexName+str(id), json=doc)
        return response.text
    '''
    filters:
    {
        "respondent" : "",
        "petitioner" : "",
        "date" : "",
        "section" : "",
    }
    '''

    def search(self, queryText, filters):
        pass

from pydantic import BaseModel


class SearchModel(BaseModel):
    queryText: str
    fromDate: str
    toDate: str
    respondents: list
    petitioners: list
    sections: list
    text_sections: list

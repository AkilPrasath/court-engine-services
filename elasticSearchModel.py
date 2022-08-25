from pydantic import BaseModel


class SearchModel(BaseModel):
    queryText: str
    date: str
    respondent: list
    petitioner: list
    section: list
    text_sections: list
    court: str = "All"
    highCourtLocation: str = ""
    judgementNumber: str = ""

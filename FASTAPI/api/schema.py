from pydantic import BaseModel
from datetime import datetime

class ArticleSchema(BaseModel):
    title:str
    description:str
    author:str

class MyArticleSchema(ArticleSchema):
    title:str
    description:str
    author:str

    class Config:
        orm_model = True

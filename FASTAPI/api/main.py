from fastapi import FastAPI, Path, HTTPException, Depends, status
from typing import Optional
from .schema import ArticleSchema, MyArticleSchema
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create-articles', status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleSchema, db: Session = Depends(get_db)):
    try:
        new_article = models.Article(
            title=article.title,
            description=article.description,
            author=article.author
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article
    except:
        raise Exception("please try again")


@app.get('/articles', status_code=status.HTTP_200_OK, response_model=List[MyArticleSchema])
def get_article(db: Session = Depends(get_db)):
    my_articles = db.query(models.Article).all()
    return my_articles


@app.get('/articles/{id}', status_code=200)
def detail_article(id: int, db: Session = Depends(get_db)):
    # my_articles = db.query(models.Article).filter(models.Article.id == id).first()
    my_articles = db.query(models.Article).get(id)
    if my_articles:
        return my_articles
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Article with this {id} does not exist")


@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id: int, article: ArticleSchema, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({
        'title': article.title,
        "description": article.description,
        "author": article.author
    })
    db.commit()
    return {"message": "The data has been updated successfully"}


@app.delete('/articles/{id}', status_code=200)
def delete_article(id: int, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": f"The data with {id} has been deleted successfully"}

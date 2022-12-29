from fastapi import FastAPI
# from scrape import main
from scrapeFile import main
import time

app = FastAPI()


@app.get('/fetch/{id}')
def index(id):
    print(id)
    data = main(id)
    return data

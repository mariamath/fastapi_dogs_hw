from enum import Enum
from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import List
import time
app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return dict()

@app.get('/dog', response_model =List[Dog], summary = 'Get Dogs')
async def get_dog(kind: DogType | None = None):
    if kind:
        return [dog for _,dog in dogs_db.items() if dog.kind == kind]
    else:
        return [dog for _,dog in dogs_db.items()]

@app.get('/dog/{pk}')
async  def get_dog_pk(pk:int):
    for _,dog in dogs_db.items():
        if dog.pk == pk:
            return dog

@app.post('/dog')
async def post_dog(new_dog: Dog):
    for _,dog in dogs_db.items():
        if new_dog.pk == dog.pk:
            raise HTTPException(status_code =409, detail ='The specified PK already exists')
        else:
            dogs_db[new_dog.pk] = new_dog
            return new_dog

@app.post('/post')
async def post():
    new_timestamp = Timestamp(id = post_db[-1].id, timestamp = round(time.time()*1000))
    post_db.append(new_timestamp)
    return new_timestamp

@app.patch('/dog/{pk}')
async def patch(pk: int, p_dog: Dog ):
    if pk == p_dog.pk :
        if pk in dogs_db:
            dogs_db[pk] = p_dog
            return p_dog
        else:
            raise HTTPException(status_code=409, detail='There is no dog with such pk')
    else :
        raise HTTPException(status_code=409, detail='dog.pk does not coincide with pk given in url')
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import *
import os

app = FastAPI()


@app.get("/")
async def status():
    channels = await ToonChannel.all().count()
    images = await ToonData.all().count()

    return {"channels": channels, "images": images}


@app.get("/exist/{id_}")
async def exist_channel(id_: int):
    exist = await ToonChannel.exists(id=id_)

    return {"exist": exist}


register_tortoise(
    app,
    db_url=os.environ.get("DB_URL"),
    modules={"models": ["models"]},
    generate_schemas=True,
)

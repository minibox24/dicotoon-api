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


@app.get("/channels/{id_}/exist")
async def exist_channel(id_: int):
    exist = await ToonChannel.exists(id=id_)

    return {"exist": exist}


@app.get("/channels/{id_}")
async def channel_info(id_: int):
    channel = await ToonChannel.get(id=id_)
    all_ = await ToonData.filter(channel_id=id_).count()

    contributors = {}

    for user_id in [
        d["user_id"] for d in await ToonData.filter(channel_id=id_).values("user_id")
    ]:
        if user_id not in contributors:
            user = await ToonUser.get(id=user_id)
            contributors[user_id] = {
                "name": user.name,
                "avatar": user.avatar,
                "count": 0,
            }
        contributors[user_id]["count"] += 1

    return {
        "name": channel.name,
        "all": all_,
        "contributors": sorted(
            list(contributors.values()), key=lambda x: x["count"], reverse=True
        ),
    }


@app.get("/channels/{id_}/images")
async def get_images(id_: int):
    images = await ToonData.filter(channel_id=id_).order_by("created_at").values("url")
    return list(map(lambda i: i["url"], images))


register_tortoise(
    app,
    db_url=os.environ.get("DB_URL"),
    modules={"models": ["models"]},
    generate_schemas=True,
)

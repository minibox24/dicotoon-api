from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import os

app = FastAPI()


@app.get("/")
def main():
    return {"hello": "world"}


register_tortoise(
    app,
    db_url=os.environ.get("DB_URL"),
    modules={"models": ["models"]},
    generate_schemas=True,
)

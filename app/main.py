# coding=utf-8

from fastapi import FastAPI


app = FastAPI(
    title="EasyCheck API",
    description="EasyCheck is an API built with FastAPI to handle sales receipts.",
    version="1.0.0",
)


# Defined base rout
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}




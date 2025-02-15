# coding=utf-8

from fastapi import FastAPI
from app.routes.user.funcs import user_router
from app.routes.receipt.funcs import receipt_router

app = FastAPI(
    title="EasyCheck API",
    description="EasyCheck is an API built with FastAPI to handle sales receipts.",
    version="1.0.0",
)


# Defined base rout
app.include_router(user_router)
app.include_router(receipt_router)

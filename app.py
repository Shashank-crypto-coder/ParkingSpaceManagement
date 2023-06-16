import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()


@app.get("/")
async def root():
   return {"message": "hello world"}



# To run locally
if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)



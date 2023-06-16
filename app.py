import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")


# @app.get("/")
# async def root():
#    return {"message": "hello world"}

@app.get("/")
def read_root():
    with open("templates/base.html", 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

# @app.route("/get_value")
# def get_value():
#     # Retrieve the value from your Python code
#     value = counter

#     # Return the value as JSON response
#     return jsonify(value=value)

@app.get("/video")
async def get_video():
    return FileResponse("static/Video_1.mp4", media_type="video/mp4")
@app.get("/video")
async def get_video():
    return FileResponse("static/Video_2.mp4", media_type="video/mp4")

# To run locally
if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)



from fastapi import FastAPI, Request, Body
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
import random
import asyncio
import string
from database.db_handlers import DBhandler

#Инициализация бд
db = DBhandler()

app =  FastAPI()


#Весь словарь
ABC = string.ascii_letters

#Словарь ссылок
url_mapping = {} # {abcd : https://pornhub.com}

@app.get("/")
def show_main_page():
    return FileResponse(r"Static/index.html")

@app.get("/style.css")
def show_main_page():
    return FileResponse(r"Static/style.css")

dataOriginal = db.chek_URL()
for i in dataOriginal:
    url_mapping[f"{db.get_URL(i)}"] = f"{i}" 

async def check_in_db(value):
    data = db.chek_URL()
    if value in data:
        return True
    return False
    
    
    '''
    data = db.chek_Short_URL()
    result = "http://127.0.0.1:8000"+value
    if result in data:
        return True
    return False
    '''

async def generate_short_url(oldURL):
    if await check_in_db(oldURL):
        return str(db.get_URL(oldURL)), True
    else:
        generate_part = random.sample(ABC, 4)
        result = "".join(generate_part)
        
        while result in url_mapping :
            generate_part = random.sample(ABC, 4)
            result = "".join(generate_part)

        return result, False
    
async def check_input(value):
    try:
        value = str(value)
        if value[:4] == "http":
            return True
    except Exception as e:
        return False

@app.post("/old")
async def get_old_URL(data=Body()):
    oldURL = data["URLOld"]
    if await check_input(oldURL) == False:
        pass
    else:
        endpointgenerate, flag = (await generate_short_url(oldURL))[0], (await generate_short_url(oldURL))[1]
        print(endpointgenerate)
        if flag == True:
            pass
        else:
            db.add_URL(oldURL, endpointgenerate)
        url_mapping[endpointgenerate] = oldURL

@app.get("/{short_url}")
async def redirictshotr(short_url: str):
    oldURL = url_mapping[short_url]
    return RedirectResponse(f"{oldURL}")
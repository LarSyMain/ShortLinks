from fastapi import FastAPI, Request, Body, Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
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

#app.mount("/", StaticFiles(directory="Static", html=True))


@app.get("/")
def show_main_page():
    return FileResponse(r"Static/index.html")

@app.get("/style.css")
def show_style_page():
    return FileResponse(r"Static/style.css")

@app.get("/Scripts.js")
def show_script_page():
    return FileResponse(r"Static/Scripts.js")



dataOriginal = db.chek_URL()
for i in dataOriginal:
    url_mapping[f"{db.get_URL(i)}"] = f"{i}" 

async def check_in_db(value):
    data = db.chek_URL()
    if value in data:
        return True
    return False
    

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
async def post_old_URL(data=Body()):
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
            await get_new_url()
        url_mapping[endpointgenerate] = oldURL


@app.get("/dbdata")
async def get_new_url():
    ShortURLdata =(db.chek_Short_URL())
    URLdata = db.chek_URL()

    #result = {"URL" : f"{URLdata}",  
    #          "ShortURL" : f"{ShortURLdata}"}
    result = {}

    for i in range(len(URLdata)):
        result[f"{URLdata[i]}"] = f"{ShortURLdata[i]}"

    return JSONResponse(content=result)


@app.get("/{short_url}")
async def redirictshotr(short_url: str):
    oldURL = url_mapping[short_url]
    return RedirectResponse(f"{oldURL}")
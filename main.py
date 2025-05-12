from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")
FILE_PATH = "my_data.txt"

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    Serves the main webpage with the form and file content.
    """
    try:
        with open(FILE_PATH, "r") as f:
            contents = f.read()
    except FileNotFoundError:
        contents = ""
    return templates.TemplateResponse("index.html", {"request": request, "file_contents": contents})

@app.post("/write/", response_class=HTMLResponse)
async def write_to_file(request: Request, line: Annotated[str, Form()]):
    """
    Appends a new line to the file and reloads the webpage.
    """
    try:
        with open(FILE_PATH, "a") as f:
            f.write(line + "\n")
        success_message = "Line appended successfully!"
    except Exception as e:
        success_message = f"Error writing to file: {e}"

    try:
        with open(FILE_PATH, "r") as f:
            contents = f.read()
    except FileNotFoundError:
        contents = ""

    return templates.TemplateResponse("index.html", {"request": request, "file_contents": contents, "message": success_message})

@app.get("/read/", response_class=PlainTextResponse)
async def read_file():
    """
    Returns the raw content of the file as plain text (still useful for debugging or other tools).
    """
    try:
        with open(FILE_PATH, "r") as f:
            contents = f.read()
        return contents
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
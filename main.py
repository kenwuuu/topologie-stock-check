from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Annotated

app = FastAPI()
FILE_PATH = "my_data.txt"

@app.post("/write/")
async def write_to_file(line: Annotated[str, Form()]):
    """
    Appends a new line to the specified file.
    """
    try:
        with open(FILE_PATH, "a") as f:
            f.write(line + "\n")
        return {"message": f"Line appended to {FILE_PATH}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to file: {e}")

@app.get("/read/", response_class=PlainTextResponse)
async def read_file():
    """
    Returns the entire content of the specified file.
    """
    try:
        with open(FILE_PATH, "r") as f:
            contents = f.read()
        return contents
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
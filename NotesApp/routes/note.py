from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schemas.note import NoteEntity, NotesEntity
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc.get("_id", "")),  # Convert ObjectId to string if necessary
            "title": doc.get("title", "No note provided"),
            "desc": doc.get("desc", "No description provided"),
            "important": doc.get("important", False)
        })
    return templates.TemplateResponse(
        "index.html", {"request": request, "newDocs": newDocs}
    )

@note.post("/")
async def add_note(request: Request):
    form = await request.form()
    formDict = dict(form)
    
    # Convert 'important' to boolean for consistency
    formDict["important"] = str(formDict.get("important") == 'on')
    
    # Ensure required fields are provided
    required_fields = ["title", "desc"]
    for field in required_fields:
        if field not in formDict:
            return {"Success": False, "Error": f"Missing required field: {field}"}
    
    # Insert the note into the database
    conn.notes.notes.insert_one(formDict)
    return {"Success": True}

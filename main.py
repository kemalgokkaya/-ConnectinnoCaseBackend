from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import db

app = FastAPI(title="Notes API")

# Pydantic modelleri
class NoteCreate(BaseModel):
    title: str
    note: str
    user_id: str

class NoteResponse(BaseModel):
    id: int
    title: str
    note: str
    user_id: str

@app.on_event("startup")
def startup_event():
    db.init_db()
    print("Veritabanı hazır!")

@app.get("/")
def read_root():
    return {"message": "Notes API'ye hoş geldiniz!"}

@app.post("/note", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate):
    try:
        # use the user_id from the request body
        note_id = db.create_note(note.title, note.note, note.user_id)
        return {
            "id": note_id,
            "title": note.title,
            "note": note.note,
            "user_id": note.user_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/{user_id}", response_model=List[NoteResponse])
def get_notes(user_id: str):
    try:
        notes = db.get_all_notes(user_id)
        return notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/note/{user_id}/{note_id}", response_model=NoteResponse)
def get_note(user_id: str, note_id: int):
    try:
        note = db.get_note_by_id(note_id, user_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Not bulunamadı")
        return note
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/note/{user_id}/{note_id}")
def delete_note(user_id: str, note_id: int):
    try:
        success = db.delete_note(note_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Not bulunamadı")
        return {"message": "Not başarıyla silindi"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/note/{user_id}/{note_id}", response_model=NoteResponse)
def update_note(user_id: str, note_id: int, note: NoteCreate):
    try:
        existing_note = db.get_note_by_id(note_id, user_id)
        if existing_note is None:
            raise HTTPException(status_code=404, detail="Not bulunamadı")
        
        db.delete_note(note_id, user_id)
        new_note_id = db.create_note(note.title, note.note, user_id)
        
        return {
            "id": new_note_id,
            "title": note.title,
            "note": note.note,
            "user_id": user_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
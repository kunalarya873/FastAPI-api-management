def NoteEntity(item)-> dict:

    return {
        "id": str(item["_id"]),
        "title": str(item["title"]),
        "desc": str(item["desc"]),
        "important": bool(item["important"])
    }

def NotesEntity(items)-> list:
    return [
        NoteEntity(item) for item in items
    ]
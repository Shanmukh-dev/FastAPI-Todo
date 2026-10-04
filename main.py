from fastapi import FastAPI, Depends, HTTPException, status
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, update
from database import SessionLocal, Base, engine
from models import Todo

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get-todos")
def get_todos(db: Session = Depends(get_db)):
    query = select(Todo)
    data = db.execute(query)

    return {"todos": data.scalars().all()}


@app.post("/create-todo", response_model=TodoSchema)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.model_dump())
    print(db_todo)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

@app.delete("/delete-todo/{item_id}")
def delete_todo(item_id: int, db: Session = Depends(get_db)):
    query = delete(Todo).where(Todo.id == item_id)

    db.execute(query)
    db.commit()

    return {"message": f"Successfully deleted todo {item_id}"}

@app.delete("/clear-todos")
def clear(db: Session = Depends(get_db)):
    query = delete(Todo)
    db.execute(query)
    db.commit()

    return {"message": "The Todo list has been cleared"}

@app.patch("/complete-todo")
def complete(item_id: int, db: Session = Depends(get_db)):
    query = update(Todo).where(Todo.id == item_id).values(completed = True)
    db.execute(query)
    db.commit()

    return {"message": f"Todo {item_id} marked as completed"}

# if __name__ == "__main__":
#     # app.
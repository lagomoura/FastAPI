from sql_app.database import SessionLocal

#. Manera de recuperar el db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

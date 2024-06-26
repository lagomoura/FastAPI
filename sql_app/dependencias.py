from sql_app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        return db #! yield se utiliza para devolver la instancia de la base de datos db cuando sea llamada.
    finally: 
        db.close()

#! La función es un generador, lo que permite que se utilice como un generador de contexto.
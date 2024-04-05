from sql_app.database import SessionLocal

#. Manera de recuperar el db

def get_db():
    db = SessionLocal()
    try:
        yield db #! yield se utiliza para devolver la instancia de la base de datos db cuando sea llamada.
    finally: 
        db.close()

#! La función es un generador, lo que permite que se utilice como un generador de contexto.
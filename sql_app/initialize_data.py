from database import SessionLocal
from models import Tags

#Para correr ese scritp necesitamos que en models.py Base este siendo importado desde database y no .database

# Lista de tags iniciales
initial_tags = [
    "Address_phone_detected", "Email_detected", "BG_removed",
    "Human_&_NSFW_detected", "Human_detected", "QR_detected",
    "Text_waterMark_detected", "URL_detected"
]

session = SessionLocal()

#! Cargando tags
# Itera sobre la lista de datos y crea objetos Tags
for tag_name in initial_tags:
    tag = Tags(tag_service=tag_name)
    session.add(tag)

# Guarda los cambios en la base de datos
session.commit()

# Cierra la sesión para liberar recursos
session.close()

print("Tags cargados exitosamente.")
#! Cargando tags

#!Eliminando un ID en especifico
# Obtén el objeto Tag con ID 1
# tag_to_delete = session.query(Tags).filter_by(id=1).first()

# if tag_to_delete:
#     # Elimina el objeto de la sesión
#     session.delete(tag_to_delete)
#     # Guarda los cambios en la base de datos
#     session.commit()
#     print("Tag eliminado exitosamente.")
# else:
#     print("No se encontró el tag con ID 1.")
    
#     # Reorganiza los IDs después de la eliminación
# session.execute("UPDATE tags SET id = id - 1 WHERE id > 1")
# # Guarda los cambios en la base de datos
# session.commit()
# print("IDs reorganizados correctamente.")
# session.close()
#!Eliminando un ID en especifico


#! Reordenar los IDs para el caso de modificacion en la tabla.
# try:
#     # Obtén todos los tags de la base de datos
#     all_tags = session.query(Tags).order_by(Tags.id).all()

#     # Actualiza los IDs utilizando un contador
#     new_id = 1
#     for tag in all_tags:
#         tag.id = new_id
#         new_id += 1

#     # Guarda los cambios en la base de datos
#     session.commit()
#     print("IDs reorganizados correctamente.")

# except Exception as e:
#     # En caso de error, realiza un rollback para deshacer los cambios
#     session.rollback()
#     print(f"Error: {e}")

# finally:
#     # Cierra la sesión para liberar recursos
#     session.close()
#! Reordenar los IDs para el caso de modificacion en la tabla.
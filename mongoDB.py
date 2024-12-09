import pymongo
import time
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pymongo.errors import *
from datetime import datetime

MONGO_URI = 'mongodb://localhost:27017'
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
database = client['Elaina']
collection = database['usuarios']
collection_dos = database['keys']
collection_tres = database['groups']
collection_cuatro = database['gates']
collection_cinco = database['alerts']
# Reemplaza con el ID del chat donde quieres enviar el registro
LOG_CHAT_ID = -1002014870445


@Client.on_message(filters.command('renovacion', prefixes=['/', ',', '.', '!', '$', '-']))
async def uwu(client, message):
    buscar_permisos = collection.find_one({"_id": message.from_user.id})
    if buscar_permisos["role"] == "Owner":
        for usuario in collection.find():
            if usuario["key"] != "None":
                if usuario["key"] < datetime.now():
                    # Actualizar la clave a "None"
                    collection.update_one({"_id": usuario["_id"]}, {
                        "$set": {"key": "None", "plan": "Free User", "antispam": 60, "apodo": "Free User"}})
                    chat_id = usuario["_id"]
                    mensaje = f"""<b><i>Your key has expired. contact @ShylphietteGreyrat to purchase a new one.</i></b>"""
                    mensaje_admin = f"""<b><i>El usuario con el id <code>{chat_id}</code> dejo de ser premium, revisar si esta en grupo de usuarios premium pagados</i></b>"""
                    try:
                        chat_id = usuario["_id"]
                        await client.send_message(chat_id, mensaje)
                        await client.send_message(LOG_CHAT_ID, mensaje_admin)
                        await message.reply(text='<b>El anuncio ha sido enviado a todos los usuarios registrados.</b>', quote=True)
                    except:
                        pass
                else:
                    pass
            else:
                pass
    else:
        return

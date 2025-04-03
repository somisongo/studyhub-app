import motor.motor_asyncio
from fastapi import Depends
from bson.objectid import ObjectId
from typing import Any, Annotated

from app.core.config import settings

# Client MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB]

class PyObjectId(ObjectId):
    """
    Classe personnalisée pour la gestion des ObjectId MongoDB avec Pydantic.
    Compatible avec Pydantic v1 et v2.
    """
    # Pour Pydantic v1
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    # Pour Pydantic v2 JSON Schema
    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _field_schema):
        return {"type": "string"}

    # Pour Pydantic v1 (rétrocompatibilité)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Pour Pydantic v2
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

def object_id_schema(field_name: str) -> CoreSchema:
    return core_schema.no_info_after_validator_function(
        validate_object_id,
        core_schema.str_schema()
    )

# Alias pour l'utilisation avec Annotated
ObjectIdField = Annotated[ObjectId, object_id_schema]


async def get_database():
    """
    Dépendance pour obtenir une connexion à la base de données MongoDB.
    """
    return db


async def init_mongodb():
    """
    Initialise les index et collections MongoDB.
    """
    # Collection utilisateurs
    await db.users.create_index("email", unique=True)
    
    # Collection notes
    await db.notes.create_index("creator_id")
    await db.notes.create_index("course_id")
    await db.notes.create_index("tags")
    await db.notes.create_index([("title", "text"), ("content", "text")])
    
    # Collection cours
    await db.courses.create_index("user_id")
    await db.courses.create_index("tags")
    
    # Collection éléments multimédias
    await db.media.create_index("note_id")
    
    # Collection révisions
    await db.revisions.create_index("user_id")
    await db.revisions.create_index("note_id")
    await db.revisions.create_index("scheduled_date")
    
    # Collection partages
    await db.shares.create_index("note_id")
    await db.shares.create_index("source_user_id")
    await db.shares.create_index("target_user_id")
    
    print("MongoDB initialized with indexes")

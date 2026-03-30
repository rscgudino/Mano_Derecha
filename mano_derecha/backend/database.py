"""
Base de datos - MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    async def connect(self):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["mi_negocio"]
        return self
    
    async def guardar_turno(self, datos):
        result = await self.db.turnos.insert_one({
            "cliente": datos.get("nombre"),
            "telefono": datos.get("telefono"),
            "servicio": datos.get("servicio"),
            "fecha": datos.get("fecha"),
            "hora": datos.get("hora"),
            "estado": "pendiente"
        })
        return str(result.inserted_id)

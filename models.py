#           Modelacion de campos

#Aqui genererare mi modelo para definir los campos que tendras mis objetos compra, compradores y frutas #

from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal   #Librerias que ocuparemos

class Comprador(BaseModel):
    id: int
    nombre_comprador: str

class Fruta(BaseModel):
    id: int
    nombre_fruta: str
    precio: Decimal

#El modelo que ocupe para mi clase compra es similar al que tengo en mi init.sql
class Compra(BaseModel):
    id_compra: int
    id_comprador: int
    id_fruta: int

    #algunos campos adicionales que pueden ser obtenidos con JOINS
    nombre_fruta: Optional[str] = None
    nombre_comprador: Optional[str] = None
    precio_fruta: Optional[Decimal] = None

class ReporteComprador(BaseModel):
    comprador: Comprador
    compras: List[Compra] = []
    total_frutas: int = 0
    precio_total: Decimal = Decimal('0.00')

    class Config:
        arbitrary_types_allowed = True









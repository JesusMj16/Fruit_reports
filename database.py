import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models import Comprador, Fruta, Compra, ReporteComprador
from decimal import Decimal
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseFruta:
    def __init__(self):

        self.connection_params = {
            "host": "localhost",
            "port": 5432,
            "database": "fruteria",
            "user": "jesus",
            "password": "b1e2i3s4"
        }

    def get_connection(self):
        # Metodo get que ocupo para realizar la coneccion lo usare en consultas posteriores
        try:
            #el doble apuntador me retorna lo que se encuentra dentor de coneccion params por separado
            # psycogpg me servira para hacer el conectado a mi base en postgres
            conn = psycopg2.connect(**self.connection_params)
            # Si nada falla se devuelve
            logger.info("La conexión ha sido exitosa ✅")
            return conn
        except Exception as e:
            #Sino se logra hacer la coneccion
            logger.error(f"La conexión ha fallado ❌: {e}")
            raise

    def get_comprador_by_id(self, comprador_id: int) -> Optional[Comprador]:
        # Hago la consulta que me devolvera el id y el nombre del comprador
        # el %s se modifica cuando a query le pase el parametro del id
        query = """SELECT id, nombre_comprador
                   FROM compradores
                   WHERE id = %s"""

        #ocupo mi metodo get
        with self.get_connection() as conn:
            #ocupare el RealDictCursor ya que deseo obtener una tupla y no un dicccionario
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (comprador_id,)) #el %s se modifica con el id que reciba
                row = cur.fetchone() #como solo deseo regresar un comprador regreso el fetchone
                if row:
                    return Comprador(**dict(row)) #retorno al id y el nombre
                return None # si no se encontro no retorno nada

    def get_compras_by_comprador(self, comprador_id: int) -> List[Compra]:  # 🔧 CORRECCIÓN: List[Compra]
        query = """ SELECT c.id_compra, 
                          c.id_fruta, 
                          c.id_comprador,
                          f.nombre_fruta, 
                          f.precio as precio_fruta
                    FROM compras c
                    JOIN frutas f ON c.id_fruta = f.id
                    WHERE c.id_comprador = %s
                    ORDER BY c.id_compra"""

        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (comprador_id,))
                rows = cur.fetchall()  # en este caso como deseo regresar la  lista de compras que se hicieron por el comprador ocupo fetchall

                compras = []
                for row in rows:
                    compra_dict = dict(row)
                    compras.append(Compra(**compra_dict)) #inserto la compra en mi vector compras

                logger.info(f"📊 Encontradas {len(compras)} compras para comprador {comprador_id}")
                return compras #retorno mi lista

    def generar_reporte_completo(self, comprador_id: int) -> Optional[ReporteComprador]:
        comprador = self.get_comprador_by_id(comprador_id)
        if not comprador:
            logger.error(f"El comprador {comprador_id} no existe")
            return None

        compras = self.get_compras_by_comprador(comprador_id)

        total_frutas = len(compras)
        precio_total = sum(compra.precio_fruta for compra in compras if compra.precio_fruta)

        reporte = ReporteComprador(
            comprador = comprador,
            compras = compras,
            total_frutas = total_frutas,
            precio_total = precio_total,
        )

        logger.info(f"📋 Reporte generado: {comprador.nombre_comprador}, {total_frutas} frutas, ${precio_total}")
        return reporte













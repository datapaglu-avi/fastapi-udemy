import sqlite3
from typing import Any
from .schemas import ShipmentCreate, ShipmentUpdate

class Database:
    def __init__(self):
        self.con = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_table()

    def create_table(self):
        # # 1. Create a table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY, 
                content TEXT, 
                weight REAL, 
                status TEXT
            )
        '''
        )


    def create(self, shipment: ShipmentCreate) -> int:
        self.cursor.execute('SELECT MAX(id) FROM shipment')
        result = self.cursor.fetchone()[0]

        new_id = result + 1

        self.cursor.execute('''
            INSERT INTO shipment
            VALUES (:id, :content, :weight, :status)
        ''', {
            "id": new_id,
            **shipment.model_dump(),
            "status": 'placed'
        })

        self.con.commit()
        return new_id
    

    def get(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute('''
            SELECT id, content, weight, status
            FROM shipment
            WHERE id = ?
        ''', (id, ))

        row = self.cursor.fetchone()

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        } if row else None
    

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cursor.execute('''
            UPDATE shipment
            SET status = :status
            WHERE id = :id
        ''', {
            "id": id, 
            **shipment.model_dump()
            }
        )

        self.con.commit()

        return self.get(id)
    

    def delete(self, id: int):
        self.cursor.execute('''
            DELETE FROM shipment
            WHERE id = ?
        ''', (id, ))

        self.con.commit()

    def close(self):
        self.con.close()
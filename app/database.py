import sqlite3
from typing import Any
from .schemas import ShipmentCreate, ShipmentUpdate
from contextlib import contextmanager

class Database:
    def connect_to_db(self):
        self.con = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cursor = self.con.cursor()


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

    # to create context manager
    # either this or Usage - function based
    # def __enter__(self):
    #     self.connect_to_db()
    #     self.create_table()

    #     return self
    

    # def __exit__(self, *args):
    #     self.close()

## usage
# with Database() as db:
#     x = db.get(12701)
#     print(x) # {'id': 12701, 'content': 'tree', 'weight': 19.0, 'status': 'out_for_delivery'}

# Usage - function based | in case we are not able to add __enter__ and __exit__ function to db class
@contextmanager
def managed_db():
    db = Database()
    # setup
    db.connect_to_db()
    db.create_table()

    yield db
    # Dispose
    db.close()

with managed_db() as db:
    print(db.get(12701))
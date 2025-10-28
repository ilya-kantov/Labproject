import sqlite3
db=sqlite3.connect("cafe.db")
c=db.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    )""")
c.execute("""
   CREATE TABLE IF NOT EXISTS staff (
       staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       role TEXT,
       phone TEXT,
       email TEXT
   )""")
c.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        table_id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_seats INTEGER
    )""")
c.execute("""
    CREATE TABLE IF NOT EXISTS order_details (
    order_details_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    order_id INTEGER, 
    status TEXT,
    dish TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)""")
c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        table_id INTEGER NOT NULL,
        staff_id INTEGER NOT NULL,
        order_date TEXT,
        order_number INTEGER,
        price REAL,
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (table_id) REFERENCES tables(table_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )""")

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
sqlite_database = "sqlite:///metanit.db"
engine = create_engine(sqlite_database, echo=True)
Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    phone = Column(String)
    email = Column(String)

    orders = relationship('Order', back_populates='client')

class Staff(Base):
    __tablename__ = 'staff'

    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    role = Column(String)
    phone = Column(String)
    email = Column(String)

    orders = relationship('Order', back_populates='staff')

class Table(Base):
    __tablename__ = 'tables'

    table_id = Column(Integer, primary_key=True, autoincrement=True)
    table_seats = Column(Integer)

    orders = relationship('Order', back_populates='table')

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    table_id = Column(Integer, ForeignKey('tables.table_id'))
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))
    order_number = Column(Integer)
    price = Column(Float)
    client = relationship('Client', back_populates='orders')
    table = relationship('Table', back_populates='orders')
    staff = relationship('Staff', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_details_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    status = Column(String)
    dish = Column(String)

    order = relationship('Order', back_populates='order_details')

c.execute("SELECT * from clients where client_id in (SELECT client_id from orders client_id)")

Base.metadata.create_all(bind=engine)
with Session(autoflush=False, bind=engine) as db:
    Artem = Client(name="Artem",phone="555-5555")
    Sam = Client(name="Sam",phone="4267-5269")
    db.add(Artem)
    db.add(Sam)
    db.commit()
with Session(autoflush=False, bind=engine) as db:
    Artem = db.query(Client).filter(Client.client_id == 1).first()
    Artem.name="Nastya"
    Artem.phone="324-422342"
    db.commit()
with Session(autoflush=False, bind=engine) as db:
    clients = db.query(Client).all()
    for p in clients:
        print(f"{p.client_id}.{p.name} ({p.phone})")
"""with Session(autoflush=False, bind=engine) as db:
    Sam = db.query(Client).filter(Client.client_id==2).first()
    db.delete(Sam)
    db.commit()"""

c.execute("INSERT INTO clients (name, phone, email) VALUES ('dmitriy','89646457446','ngtunn@gmail.com')")
c.execute("INSERT INTO staff (name, role, phone,email) VALUES ('ivan','povar','89646457346','cafe241@gmail.com')")
c.execute("INSERT INTO tables (table_seats) VALUES (23)")
c.execute("INSERT INTO order_details (order_id,status,dish) VALUES (1,'comleted','meat with mashed potatoes')")
c.execute("INSERT INTO orders (client_id,table_id,staff_id,order_date,order_number,price) VALUES (1,1,1,'third october',322,1349.99)")
#Получение всех заказов клиента
client_id=1
c.execute("""
    SELECT order_id, order_number, order_date, price, client_id, table_id, staff_id
    FROM orders
    WHERE client_id = ?
    ORDER BY order_id
""", (client_id,))
orders = c.fetchall()
print("Заказы клиента:", orders)
#Получение информации о блюде заказа
order_id = 1
c.execute("""
    SELECT order_details_id, dish, status
    FROM order_details
    WHERE order_id = ?
    ORDER BY order_details_id
""", (order_id,))
dishes = c.fetchall()
print("Блюда в заказе:", dishes)
db.commit()
db.close()

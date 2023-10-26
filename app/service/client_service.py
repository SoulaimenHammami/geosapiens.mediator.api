from uuid import UUID
from .database.db_connector import Connection
from .database.db_tables import Client
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import insert , select , delete , update

class ClientService:
  def __init__(self, session:Session) -> None:
    self.session = session
  
  def add_client(self, client:Dict)-> UUID:
    statement = insert(Client).returning(Client.uuid).values(dict(client))
    inserted_client_uuid = self.session.execute(statement=statement)
    self.session.commit()
    return inserted_client_uuid
  def delete_by_name(self ,name: str )-> UUID:    
    statement = delete(Client).where(Client.name==name).returning(Client.uuid)
    client_uuid =self.session.execute(statement=statement)
    self.session.commit()
    return client_uuid
  def update_request_limit(self, name:str , values: dict)->None:
    statement = update(Client).where(Client.name == name).values(**values)
    self.session.execute(statement=statement)
    self.session.commit()
    
  def find_by_name(self, name:str)-> dict:
    statement = select(Client).where(Client.name == name)
    clients = self.session.execute(statement=statement).all()
    clients = [client[0].__dict__ for client in clients]
    return clients
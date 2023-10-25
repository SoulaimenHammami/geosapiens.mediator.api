from fastapi import APIRouter, HTTPException
from app.service.client_service import ClientService
from fastapi import Depends , Response
from sqlalchemy.orm import Session
from app.service.database.db_connector import Connection
from pydantic import BaseModel
router = APIRouter()
class ClientSchema(BaseModel) :
    name:str
    expiration:int
    request_limit:int
    
@router.post("/create")
async def create_client(client:ClientSchema , session:Session=Depends(Connection().get_session)):
    client_service =ClientService(session=session)
    id = client_service.add_client(client=client)
    if id:
        return Response(content="done")
    else:
        return HTTPException(status_code=500, detail="error has occured")


@router.get("/getClient/{name}")
async def get_client(name:str , session:Session=Depends(Connection().get_session)):
    client_service =ClientService(session=session)
    clients = client_service.find_by_name(name=name)
    print(clients)
    return clients


@router.delete("/delete/{name}")
async def delete_client(name:str , session:Session=Depends(Connection().get_session)):
    client_service =ClientService(session=session)
    id = client_service.delete_by_name(name=name)
    if id :
        return "Client deleted successfully!"


@router.put("/update/{name}&{value}")
async def get_client(name:str , value: int , session:Session=Depends(Connection().get_session)):
    client_service =ClientService(session=session)
    client_service.update_request_limit(name=name , values=dict(request_limit =value))
    
    return "Client updated successfully!"


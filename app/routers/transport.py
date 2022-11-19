from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..modules.dependencies import get_token_header
from ..modules.transportation_problem import transportationProblem
from ..modules.modi_method import MODI, calculate_cost

router = APIRouter(
    prefix="/transport",
    tags=["transport"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not Found"}},
)

class Transport(BaseModel):
    supply: list = []
    demand: list = []
    cost_matrix: list = []

@router.post("/modi-method")
async def submit_modi_method(transport: Transport):
    TP = transportationProblem(transport.supply, transport.demand, transport.cost_matrix)
    bfs = TP.vam()
    ops = MODI(transport.supply, transport.demand, transport.cost_matrix, bfs)
    if ops == None:
        return { "result": calculate_cost(bfs) }
    else:
        return { "result": calculate_cost(ops) }

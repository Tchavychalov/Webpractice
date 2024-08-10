from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
from .models import MLRequest
from .services.task_service import TaskAddService, TaskResultService, NotEnoughBalanceError, TaskNotDoneError, TaskNotFoundError
from .services.nn_service import NNService
from .services.balance_service import FileBalance
from .services.file_service import FileService
from .dependencies import get_file_service, get_nn_service, get_balance_service

router = APIRouter()

# Проверка сервиса
@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse(status_code=200, content={"status":"OK"})

# Проверка работы нейронной сети
@router.get("/healthcheck/ml")
async def healthcheck_ml(nn_service: NNService = Depends(get_nn_service)):
    if await nn_service.healthcheck_ml_service():
        return JSONResponse(status_code=200, content={"status":"ANN ready"})
    else:
        raise HTTPException(status_code=503, detail="ANN error")
        

# Обработка добавления запроса к нейронной сети
@router.post('/task/add')
async def add_req(
                request: MLRequest, 
                backgroud: BackgroundTasks, 
                balance_service: FileBalance = Depends(get_balance_service), 
                nn_service: NNService = Depends(get_nn_service),
                file_service: FileService = Depends(get_file_service),
                ) -> dict:
    try:
        task_service = TaskAddService(balance_service, nn_service, file_service)
        req_id = await task_service.add_task(request, backgroud)
        return {'req_id': req_id}
    except NotEnoughBalanceError as neb:
        raise HTTPException(status_code=402, detail=str(neb))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Результаты
@router.get("/task/result")
async def get_result(token: str, id: str, file_service: FileService = Depends(get_file_service), nn_service: NNService = Depends(get_nn_service),) -> dict:
    try:
        task_result_service = TaskResultService(file_service, nn_service)
        result = await task_result_service.get_result(token, id)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Задача с такими ID не найдена")
    except TaskNotDoneError:
        raise HTTPException(status_code=204, detail="Задача еще не выполнена")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
from .models import MLRequest, new_token
from .services import FileService, NNService
from .dependencies import get_fileservice, get_nnservice

router = APIRouter()

# Проверка сервиса
@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse(status_code=200, content={"status":"OK"})

# Проверка работы нейронной сети
@router.get("/healthcheck/ml")
async def healthcheck_ml(nnservice: NNService = Depends(get_nnservice)):
    try:
        await nnservice.run_nn("test")
        return JSONResponse(status_code=200, content={"status":"ANN ready"})
    except Exception:
        raise HTTPException(status_code=503, detail="ANN error")

# Обработка добавления запроса к нейронной сети
@router.post('/task/add')
async def add_req(
                request: MLRequest, 
                backgroud: BackgroundTasks, 
                fileservice: FileService = Depends(get_fileservice), 
                nnservice: NNService = Depends(get_nnservice),
                ):
    # Имя файла с балансом
    balance_filename = f'{request.token}_balance.txt'
    # Проверка существования файла и запись начального баланса
    if not fileservice.file_exists(balance_filename):
        await fileservice.set_file_content(balance_filename, "100")
    # Проверка текущего значение баланса
    current_balance = int(await fileservice.get_file_content(balance_filename))
    if current_balance <= 10:
        raise HTTPException(status_code=402, detail="Balance error")
    # Создание id задачи
    req_id = new_token(4)
    wait_filename = f"{request.token}_{req_id}_wait.txt"
    # Запись файла с суффиксом wait
    await fileservice.set_file_content(wait_filename, request.query)
    # Добавление задачи
    backgroud.add_task(req_process, request.token, req_id, request.query, fileservice, nnservice)
    # Уменьшение баланса
    await fileservice.balance_dec(balance_filename)
    # Вернуть id задачи
    return JSONResponse(status_code=200, content={"id": req_id})
#Обработка запроса в нейронной сети
async def req_process(token: str, id: str, query: str, fileservice: FileService = Depends(get_fileservice), nnservice: NNService = Depends(get_nnservice)):
    result = await nnservice.run_nn(query)
    wait_filename = f"{token}_{id}_wait.txt"
    done_filename = f"{token}_{id}_ready.txt"
    await fileservice.set_file_content(done_filename, result)
    if fileservice.file_exists(wait_filename):
        fileservice.delete_file(wait_filename)

# Результаты
@router.get("/task/result")
async def get_result(token: str, id: str, fileservice: FileService = Depends(get_fileservice)):
    wait_filename = f"{token}_{id}_wait.txt"
    done_filename = f"{token}_{id}_ready.txt"

    if fileservice.file_exists(done_filename):
        result = await fileservice.get_file_content(done_filename)
        return JSONResponse(status_code=200, content={"result":result})
    elif fileservice.file_exists(wait_filename):
        return JSONResponse(status_code=204, content={"message":"Process not complete"})
    else:
        return HTTPException(status_code=404, delail="ID not found")
from ..nn_model import predict

class NNService:
    async def run_nn(self, query: str) -> str:
        res_dict = {0: "Neutral", 1: "Positive", 2: "Negative"}
        res = predict(query)  # результат предсказания
        return f'Запрос: {query}\nРезультат:{res_dict[res[0]]}'
    
    async def healthcheck_ml_service(self) -> bool:
        try:
            _ = await self.run_nn("test")
            return True
        except Exception as ex:
            return False
    
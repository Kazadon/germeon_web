import httpx
import logging

logger = logging.getLogger("uvicorn.error")

class BaseDL:
    def __init__(self, token: str, login: str, password: str):
        self.client = httpx.AsyncClient(base_url='https://api.dellin.ru', timeout=10)
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
            }
        self.login = login
        self.password = password
        self.token = token
        self.sessionID = None
        
    async def get_valid_session_id(self) -> str:
        """Возвращает живой sessionID (используется в Depends). Если его нет, пробует авторизоваться."""
        if not self.sessionID:
            logger.info("Сессия отсутствует. Попытка авторизации...")
            await self.auth()
                        
        if not self.sessionID:
            raise RuntimeError("Не удалось получить валидный sessionID от Деловых Линий")
        
        return self.sessionID
    
    # Аутентификация, получение sessionID для дальнейшей работы
    async def auth(self) -> None:
        endpoint = 'v3/auth/login.json'
        data = {
            "appkey": self.token,
            "login": self.login,
            "password": self.password
            }
        
        try:
            response: httpx.Response = await self.client.post(url=endpoint, headers=self.headers, json=data)

            if response.status_code == 200:
                logger.info("AUTH - successful request")
                self.sessionID = response.json()['data']['sessionID']
            else:
                logger.error(f"AUTH ERROR. Code: {response.status_code}, Body: {response.text}")
                self.sessionID = None
                
        except Exception as e:
            logger.error(f"AUTH NETWORK ERROR: {e}")
            self.sessionID = None

    async def make_request(self, endpoint: str, data: dict) -> dict:
            """
            Универсальный метод для выполнения бизнес-запросов.
            Автоматически подставляет sessionID и перевыпускает сессию при ошибке.
            """
            # Гарантируем, что у нас есть хоть какой-то sessionID перед стартом
            session_id = await self.get_valid_session_id()
            
            # Подмешиваем авторизационные данные в тело запроса
            data["appKey"] = self.token
            data["sessionID"] = session_id

            try:
                # Делаем первую попытку запроса
                response = await self.client.post(endpoint, headers=self.headers, json=data)
                
                # Проверяем, не сбросилась ли сессия на стороне Деловых Линий.
                # Обычно они возвращают 401 Unauthorized, ЛИБО код ошибки внутри JSON (например, "session_expired") в случае,
                # если запрос по какой-то причине вернет статус 200, вместо 401, а внутри будет поле ошибки.
                # Оба варианта:
                is_unauthorized = response.status_code == 401
                
                # Проверка тела ответа на маркеры протухшей сессии (если ответ — JSON)
                is_session_error = False
                if response.status_code == 200 and "application/json" in response.headers.get("content-type", ""):
                    res_data = response.json()
                    # Если в ответе есть поле с ошибками и там сказано про сессию
                    if "errors" in res_data or "error" in res_data:
                        err_text = str(res_data).lower()
                        if "session" in err_text or "expired" in err_text or "сессия" in err_text or "сессия" in err_text:
                            is_session_error = True

                if is_unauthorized or is_session_error:
                    logger.warning("Ошибка запроса! Сессия истекла или неверный sessionID. Обновление сессии...")
                    
                    # 1. Сбрасываем старую сессию
                    self.sessionID = None
                    # 2. Запрашиваем новую авторизацию
                    await self.auth()
                    
                    if not self.sessionID:
                        raise httpx.HTTPStatusError("Авторизация не удалась", request=response.request, response=response)

                    logger.info("Сессия успешно обновлена. Выполняется запрос...")
                    
                    # 3. Обновляем sessionID в данных и делаем ВТОРУЮ (повторную) попытку запроса
                    data["sessionID"] = self.sessionID
                    response = await self.client.post(endpoint, headers=self.headers, json=data)

                # Если и вторая попытка выдала ошибку (не связанную с сессией), генерируем исключение
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                logger.error(f"API HTTP Error на эндпоинте {endpoint}: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Сбой сети при запросе к {endpoint}: {e}")
                raise

    # # Проверка и обновление активности сессии
    # async def check_session(self) -> None:
    #     url = '/v3/auth/session_info.json'
    #     data = {
    #         "appKey": self.token,
    #         "sessionID": self.sessionID
    #             }
    #     try:
    #         response = await self.client.post(url, headers=self.headers, json=data)
    #         if response.status_code == 200:
    #             logger.info(f"Check session - successful request.")
    #         else:
    #             logger.warning("CHECK SESSION ERROR. Session expired or invalid. Reauthorizing...")
    #             await self.auth()
    #     except Exception as e:
    #         logger.error(f"CHECK SESSION NETWORK ERROR: {e}. Keeping current sessionID as fallback.")

    # Закрытие активной сессии
    async def close_session(self) -> None:
        """Метод закрывает сессию API DL и очищает HTTPX клиент"""
        if not self.sessionID:
            return
        endpoint = '/v3/auth/logout.json'
        data = {
            "appKey": self.token,
            "sessionID": self.sessionID
        }
        try:
            await self.client.post(url=endpoint, headers=self.headers, json=data)
            logger.info("LOGOUT - successful. SESSION CLOSED")
        except Exception as e:
            logger.error(f"CLOSE SESSION NETWORK ERROR: {e}")
        finally:
            self.sessionID = None
            await self.client.aclose()
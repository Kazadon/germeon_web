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
        
        await self.check_session()
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


    # Проверка и обновление активности сессии
    async def check_session(self) -> None:
        url = '/v3/auth/session_info.json'
        data = {
            "appKey": self.token,
            "sessionID": self.sessionID
                }
        try:
            response = await self.client.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                logger.info(f"Check session - successful request.")
                # Переавторизация, если сессия истекла
                if response.json()['data']['session']['expired'] == True:
                    self.auth()
            else:
                logger.warning("CHECK SESSION ERROR. Something went wrong")
                await self.auth()
        except Exception as e:
            logger.error(f"CHECK SESSION NETWORK ERROR: {e}. Keeping current sessionID as fallback.")

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
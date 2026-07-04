import requests
import httpx
import json

class BaseDL:
    def __init__(self, token: str, login: str, password: str):
        self.client = httpx.AsyncClient(base_url='https://api.dellin.ru')
        self.headers = {'accept': 'application/json',
                        'Content-Type': 'application/json'}
        self.login = login
        self.password = password
        self.token = token
        self.sessionID = None
    
    # Аутентификация, получение sessionID для дальнейшей работы
    def auth(self) -> None:
        url = 'https://api.dellin.ru/v3/auth/login.json'
        data = {"appkey": self.token,
                "login": self.login,
                "password": self.password}
        json_string = json.dumps(data)
        # ПЕРЕПИСАТЬ ВСЕ РЕКВЕСТЫ НА HTTPX
        response = requests.post(url, headers=self.headers, data=json_string) 
        if response.status_code == 200:
            print(f"\nAUTH - succesful request\n")
            self.sessionID = json.loads(response.content)['data']['sessionID']

        else:
            print(f"\nAUTH ERROR\n{response}")

    # Проверка и обновление активности сессии
    def check_session(self) -> None:
        url = 'https://api.dellin.ru/v3/auth/session_info.json'
        data = {"appKey": self.token,
                "sessionID": self.sessionID}
        json_string = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=json_string)

        if response.status_code == 200:
            print(f"Check session - succesful request.\nSessionID: {data['sessionID']}\n")
        else:
            print(f"\nCHECK SESSION ERROR \nWrong ApiToken or session expired\nReauth...\n{response}")
            self.auth()

    # Закрытие активной сессии
    def close_session(self) -> None:
        url = 'https://api.dellin.ru/v3/auth/logout.json'
        data = {"appKey": self.token,
                "sessionID": self.sessionID}
        json_string = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=json_string)

        if response.status_code == 200:
            print(f"\nLOGOUT - succesful.\nSESSION CLOSED\n")
        else:
            print(f"\nCLOSE SESSION ERROR\nWrong ApiToken/sessionID expired or already closed\n{response}")
import requests
import json
import os
import base64
from core.features.dellin_api.printdocs import PrintDocument
from datetime import datetime
from core.features.dellin_api.base_dl import BaseDL

class PreorderPages():
    def __init__(self, base_client: BaseDL):
        self.base = base_client

    # Метод возвращает список номеров предварительных заявок от ООО Гермеон на указанную дату оформления заказов
    def get_germeon_orders(self):
        
        url = 'https://api.dellin.ru/v3/orders.json'
        date_str = input('Введите дату оформления заказа в формате ДД.ММ.ГГГГ:\n').replace('.', '-').replace(',', '-').replace('/','-').strip().strip('-')
        date = datetime.strptime(date_str, "%d-%m-%Y")
        date = date.strftime('%Y-%m-%d')
        data = {"appkey": self.token, 
                "sessionID":self.sessionID,
                "dateStart": f'{date} 00:00', # Форматы даты ГГГГ-ММ-ДД
                "dateEnd": f'{date} 23:59'
                }
        json_string = json.dumps(data)
        print('\nПолучение списка заявок от ООО Гермеон\nЗагрузка...\n\n')
        response = requests.post(url, headers=self.headers, data=json_string)

        if response.status_code == 200:
            json_dict = json.loads(response.content)
            totalPages = int(json_dict['metadata']['totalPages'])
            if totalPages > 1:
                for page in range(2, totalPages + 1):
                    data = {"appkey": self.token, 
                            "sessionID":self.sessionID,
                            "dateStart": f'{date } 00:00', # Форматы даты ГГГГ-ММ-ДД
                            "dateEnd": f'{date} 23:59',
                            'page': page
                            }
                    json_string = json.dumps(data)
                    response = requests.post(url, headers=self.headers, data=json_string)
                    json_dict['orders'].extend(json.loads(response.content)['orders'])
            orders_list = []

            for order in json_dict['orders']:
                if "гермеон" in order['sender']['name'].lower():
                    # Возможно понадобится возвращать список заказов с полной информацией, а не определенные ключ:значение
                    orders_list.append({"Номер заявки": order['orderId'], "Получатель": order['receiver']['name'],"Количество копий": order['freight']['places'] + 1})   
                    # Количество копий маркировок равняется количеству грузовых мест + 1
            if orders_list:
                print(f"\nGET ORDER LIST - succesful request.\n\n")
                return orders_list
            else: 
                print('На выбранную дату нет заявок от ООО Гермеон. Проверьте дату')
                # self.close_session()
        else:
            print(f"\nGET ORDER LIST ERROR\nWrong ApiToken/sessionID or something went wrong\nTry again\n{response}")
        pass
    
    # Сохранение печатных форм предварительных заявок в файл в папку docsForPrint для дальнейшей печати или редактирования
    def print_preorderPages(self, list: list) -> None:
        url = 'https://api.dellin.ru/v1/customers/request/pdf.json'
        print(f'\n\nСохранение печатных форм предварительных заявок в папку {os.getcwd()}/docsForPrint\n\nЗагрузка...\n\n')
        for item in list:
            data = {"appkey": self.token,
                    "sessionID": self.sessionID,
                    "requestID": item['Номер заявки']}
            json_string = json.dumps(data)
            # Запрос возвращает JSON с документом в формате base64
            response = requests.post(url, headers=self.headers, data=json_string)

            if response.status_code == 200:
                filename = f'{item['Номер заявки']} - {item['Получатель'].replace('"', '')}'
                try:
                    with open(fr'.\docsForPrint\{filename}.pdf',"wb") as f:
                            f.write(base64.b64decode(json.loads(response.content)['base64']))
                            print(f"Файл {filename}.pdf сохранен.")
                            f.close()
                    # Печать файла сразу после сохранения с последующим удалением из директории.
                    try:        
                        PrintDocument.print_document(fr'.\docsForPrint\{filename}.pdf' , item['Количество копий'] )
                        os.remove(fr'.\docsForPrint\{filename}.pdf')
                        print(fr'Файл {filename}.pdf удален')
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(f'Ошибка - {e}')
            else:
                print(f"\nSAVE DOC ERROR\nWrong ApiToken/sessionID or something went wrong\nTry again\n{response}")

    def print_order(self, order_number, copies_number):
        url = 'https://api.dellin.ru/v1/customers/request/pdf.json'
        data = {"appkey": self.token,
                "sessionID": self.sessionID,
                "requestID": order_number}
        json_string = json.dumps(data)
        # Запрос возвращает JSON с документом в формате base64
        response = requests.post(url, headers=self.headers, data=json_string)

        if response.status_code == 200:
            filename = f'{order_number}'
            try:
                with open(fr'.\docsForPrint\{filename}.pdf',"wb") as f:
                        f.write(base64.b64decode(json.loads(response.content)['base64']))
                        print(f"Файл {filename}.pdf сохранен.")
                        f.close()
                # Печать файла сразу после сохранения с последующим удалением из директории.
                try:        
                    PrintDocument.print_document(fr'.\docsForPrint\{filename}.pdf' , copies_number)
                    os.remove(fr'.\docsForPrint\{filename}.pdf')
                    print(fr'Файл {filename}.pdf удален')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(f'Ошибка - {e}')
                os.remove(fr'.\docsForPrint\{filename}.pdf')
        else:
            print(f"\nPRINT ORDER ERR\НОМЕР ЗАЯВКИ {order_number} НЕ СУЩЕСТВУЕТ ИЛИ что-то пошло не так\nTry again\n{response}")

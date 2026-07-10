import os
import base64
from core.features.dellin_api.printdocs import PrintDocument
from datetime import datetime, timedelta
from core.features.dellin_api.base_dl import BaseDL

class PreorderPages():
    """Конструктор принимающий BaseDL класс при инициализации, копируя его методы и свойства"""
    def __init__(self, base_client: BaseDL):
        self.base_client = base_client
        self.httpxclient = base_client.client

    # Метод возвращает список номеров предварительных заявок от ООО Гермеон на указанную дату оформления заказов
    async def get_germeon_orders(self, search_date):
        
        url = '/v3/orders.json'
        # date_str = input('Введите дату оформления заказа в формате ДД.ММ.ГГГГ:\n').replace('.', '-').replace(',', '-').replace('/','-').strip().strip('-')
        search_date = datetime.strptime(search_date, '%Y-%m-%d')
        end_date = search_date + timedelta(days=1)
        # search_date = datetime.strftime('%Y-%m-%d')
        data = {"appkey": self.base_client.token, 
                "sessionID":self.base_client.sessionID,
                "dateStart": f'{search_date}', # Форматы даты ГГГГ-ММ-ДД
                "dateEnd": f'{end_date}'
                }
        print('\nПолучение списка заявок от ООО Гермеон\nЗагрузка...\n\n')
        response = await self.httpxclient.post(url, headers=self.base_client.headers, json=data)

        if response.status_code == 200:
            content = response.json()
            totalPages = int(content['metadata']['totalPages'])
            return content['orders']
            
        #     if totalPages > 1:
        #         for page in range(2, totalPages + 1):
        #             data = {"appkey": self.base_client.token, 
        #                     "sessionID":self.base_client.sessionID,
        #                     "dateStart": f'{search_date } 00:00', # Форматы даты ГГГГ-ММ-ДД
        #                     "dateEnd": f'{search_date} 23:59',
        #                     'page': page
        #                     }
        #             response = requests.post(url, headers=self.base_client.headers, json=data)
        #             orders_list.extend(response.content)['orders']
        #     orders_result = []

        #     for order in orders_list:
        #         if "гермеон" in order['sender']['name'].lower():
        #             # Возможно понадобится возвращать список заказов с полной информацией, а не определенные ключ:значение
        #             # orders_result.append({"Номер заявки": order['orderId'], "Получатель": order['receiver']['name'],"Количество копий": order['freight']['places'] + 1})   
        #             orders_result.append(order)   
        #             # Количество копий маркировок равняется количеству грузовых мест + 1
        #     if orders_list:
        #         print(f"\nGET ORDER LIST - succesful request.\n\n")
        #         return orders_result
        #     else: 
        #         print('На выбранную дату нет заявок от ООО Гермеон. Проверьте дату')
        #         # self.close_session()
        # else:
        #     print(f"\nGET ORDER LIST ERROR\nWrong ApiToken/sessionID or something went wrong\nTry again\n{response}")
        # pass
    
    # # Сохранение печатных форм предварительных заявок в файл в папку docsForPrint для дальнейшей печати или редактирования
    # def print_preorderPages(self, list: list) -> None:
    #     url = '/v1/customers/request/pdf.json'
    #     print(f'\n\nСохранение печатных форм предварительных заявок в папку {os.getcwd()}/docsForPrint\n\nЗагрузка...\n\n')
    #     for item in list:
    #         data = {"appkey": self.token,
    #                 "sessionID": self.sessionID,
    #                 "requestID": item['Номер заявки']}
    #         json_string = json.dumps(data)
    #         # Запрос возвращает JSON с документом в формате base64
    #         response = requests.post(url, headers=self.headers, data=json_string)

    #         if response.status_code == 200:
    #             filename = f'{item['Номер заявки']} - {item['Получатель'].replace('"', '')}'
    #             try:
    #                 with open(fr'.\docsForPrint\{filename}.pdf',"wb") as f:
    #                         f.write(base64.b64decode(json.loads(response.content)['base64']))
    #                         print(f"Файл {filename}.pdf сохранен.")
    #                         f.close()
    #                 # Печать файла сразу после сохранения с последующим удалением из директории.
    #                 try:        
    #                     PrintDocument.print_document(fr'.\docsForPrint\{filename}.pdf' , item['Количество копий'] )
    #                     os.remove(fr'.\docsForPrint\{filename}.pdf')
    #                     print(fr'Файл {filename}.pdf удален')
    #                 except Exception as e:
    #                     print(e)
    #             except Exception as e:
    #                 print(f'Ошибка - {e}')
    #         else:
    #             print(f"\nSAVE DOC ERROR\nWrong ApiToken/sessionID or something went wrong\nTry again\n{response}")

    # def print_order(self, order_number, copies_number):
    #     url = '/v1/customers/request/pdf.json'
    #     data = {"appkey": self.token,
    #             "sessionID": self.sessionID,
    #             "requestID": order_number}
    #     # Запрос возвращает JSON с документом в формате base64
    #     response = self.base_client.client.post(url, headers=self.headers, json=data)

    #     if response.status_code == 200:
    #         filename = f'{order_number}'
    #         try:
    #             with open(fr'.\docsForPrint\{filename}.pdf',"wb") as f:
    #                     f.write(base64.b64decode(json.loads(response.content)['base64']))
    #                     print(f"Файл {filename}.pdf сохранен.")
    #                     f.close()
    #             # Печать файла сразу после сохранения с последующим удалением из директории.
    #             try:        
    #                 PrintDocument.print_document(fr'.\docsForPrint\{filename}.pdf' , copies_number)
    #                 os.remove(fr'.\docsForPrint\{filename}.pdf')
    #                 print(fr'Файл {filename}.pdf удален')
    #             except Exception as e:
    #                 print(e)
    #         except Exception as e:
    #             print(f'Ошибка - {e}')
    #             os.remove(fr'.\docsForPrint\{filename}.pdf')
    #     else:
    #         print(f"\nPRINT ORDER ERR\НОМЕР ЗАЯВКИ {order_number} НЕ СУЩЕСТВУЕТ ИЛИ что-то пошло не так\nTry again\n{response}")

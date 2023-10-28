import json

import aiohttp
import requests


async def send_json_request_async(url, payload):
    import main
    import app
    """
    Асинхронный метод для отправки JSON-запроса на указанный URL.
    :param url: URL, на который будет отправлен запрос.
    :param payload: JSON-данные, которые будут отправлены.

    :return: None
    """
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Content-Type': 'application/json'}
            async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                main.listdataQ.clear()  # Очистить список данных, если это необходимо
    except Exception as e:
        # Обработка исключений здесь
        app.update_log_text(f"Произошла ошибка при отправке запроса: {e}", "red")


def get_last_word_before_slash(input_string):
    # Разбиваем строку по символу '/'
    parts = input_string.split('/')

    # Извлекаем последнее слово
    last_word = parts[-1]

    return last_word


def send_json_request_sync(url, payload):
    import main
    import app
    """
    Синхронный метод для отправки JSON-запроса на указанный URL.
    :param url: URL, на который будет отправлен запрос.
    :param payload: JSON-данные, которые будут отправлены.

    :return: None
    """
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Поднимет исключение, если ответ сервера не успешен

        main.listdataQ.clear()  # Очистить список данных, если это необходимо
    except Exception as e:
        # Обработка исключений здесь
        app.update_log_text(f"Произошла ошибка при отправке запроса: {e}", "red")


async def send_image_to_server(sugar_name, image_path, chat_id, caption, timer_del=None):
    """
    Метод отправки картинки по пути. пример: {'cp': 'client/54745', 'chat_id': '-1001732045128', 'img': 'C:\\13.jpg'}
    :param timer_del:
    :param sugar_name:
    :param image_path:
    :param chat_id:
    :param caption:
    :return:
    """
    import main
    # Установите тайм-аут, например, 10 секунд
    timeout = aiohttp.ClientTimeout(total=3)
    url = f"http://{main.ipWebServ}:8000/screen/{sugar_name}"

    # Укажите нужный chat_id в параметрах запроса (необязательно, так как установлено значение по умолчанию)
    params = {'chat_id': chat_id, 'caption': caption, "timer_del": timer_del}

    try:
        # Откройте файл скриншота и отправьте его на сервер с использованием aiohttp
        async with aiohttp.ClientSession() as session:
            # Создайте FormData для отправки файла
            data = aiohttp.FormData()
            data.add_field('image', open(image_path, 'rb'))

            async with session.post(url, params=params, data=data) as response:
                response_data = await response.json()
                print(response_data)
    except aiohttp.ClientError as e:
        print(f"Произошла ошибка при отправке запроса: {str(e)}")
        pass

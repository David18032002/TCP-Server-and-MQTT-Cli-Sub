import asyncio
import datetime
import inspect
import json

from PIL import Image


async def handle_client(reader, writer):
    import app
    import main
    import other
    try:
        while True:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")  # Дата и время
            data = await reader.read(16000)  # Чтение данных от TCP клиента
            if not data:
                break
            message = data.decode('utf-8')
            app.update_log_text(f"Сообщение от клиента: {message}", "black")
            try:
                jsonMess = json.loads(message)
            except SyntaxError as e:
                print(f"Синтаксическая ошибка при разборе JSON: {e} (строка {inspect.currentframe().f_lineno})")
                continue
            # Отладочное сообщение для отображения полученного JSON
            print(f"Полученный JSON: {jsonMess} (строка {inspect.currentframe().f_lineno})")
            if "getData" in jsonMess:  # Ответы скаде при запросе
                if len(main.listdata) != 0:  # Если буфер не пуст
                    mess = main.listdata.pop()  # Удалил отправленное сообщение из буфера
                    writer.write(mess.encode())
                    await writer.drain()
                    print(f"Отправлено клиенту тсп: {mess}")
                    app.update_log_text(f"Отправлено клиенту тсп: {mess}", "green")
                else:  # Если буфер пуст, отправляем {"getData":"None"}
                    resp = '{"getData":"None"}'
                    writer.write(resp.encode())
                    await writer.drain()
                    # app.update_log_text(f"Ответ клиенту TCP: {resp}", "green")
            elif "q" in jsonMess and "p" in jsonMess:
                if int(jsonMess["q"].split("-")[0]) < int(jsonMess["q"].split("-")[1]):
                    main.listdataQ.append(str(jsonMess["p"]))
                else:
                    main.listdataQ.append(str(jsonMess["p"]))
                    res = ''.join(map(str, main.listdataQ))
                    res = res.replace('$', '"')
                    res = json.loads(res)
                    print(res)
                    # # Отладочное сообщение для отображения результата склейки
                    # print(f"Склейка: {res} (строка {inspect.currentframe().f_lineno})")
                    if "btns" in res:  # Условие не получение кнопок и отправка
                        if len(main.button_list) == 0:
                            main.button_list.append(res)
                            await other.send_json_request_async(f"http://{main.ipWebServ}:8000"
                                                                f"/buttons/{main.factory}",
                                                                res)
                            app.update_log_text("Список кнопок отправлен! (TCP-Server)", "blue")
                        else:
                            pass
                    elif "cp" in res and "img" in res:  # Условие не получение пути скрина и отправка
                        app.update_log_text(f"Перед отправкой скрина: {res}", "black")
                        timer_Del_Img = main.config.get('OTHER', 'imgTimeDel')  # Для корректной отправки в WEB
                        way = res["img"]
                        file2 = f"{way[:-3]}jpg"
                        image = Image.open(way)
                        image.save(file2)
                        await asyncio.create_task(
                            other.send_image_to_server(main.factory, file2, res['chat_id'], res['cp'],
                                                       timer_del=int(timer_Del_Img)))
                        print(main.listdataQ)
                        main.listdataQ.clear()
                    else:
                        pass
    except ConnectionResetError:  # Обработка исключения разрыва связи клиента (подкл - отправил - откл)
        pass
    except ValueError as e:
        print(f"Ошибка при разборе JSON: {e} (строка {inspect.currentframe().f_lineno})")

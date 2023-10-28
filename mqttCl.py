# Функция обратного вызова при успешном подключении MQTT
import datetime
import json
import threading

listdata_lock = threading.Lock()


def on_connect(client, userdata, flags, rc):
    import main
    import app
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Дата и время
    MQTT_TOPIC = main.config.get('MQTT', 'topicIMG')
    if rc == 0:
        app.update_log_text(f"Connected to MQTT broker: {MQTT_TOPIC}, {formatted_datetime}", "green")
        client.subscribe(MQTT_TOPIC)
    else:
        app.update_log_text(f"Connection failed with result code {rc}, {formatted_datetime}", "red")


# Функция обратного вызова при потере соединения MQTT
def on_disconnect(client, userdata, rc):
    import app
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Дата и время
    if rc != 0:
        app.update_log_text(f"Disconnected from MQTT broker with result code {rc}, {formatted_datetime}", "red")
        # Устанавливаем задержку перед попыткой переподключения
        client.reconnect_delay_set(min_delay=1, max_delay=30)


def on_message(client, userdata, message):
    import app
    from other import send_json_request_sync, get_last_word_before_slash
    from main import listdata, button_list, ipWebServ, factory
    global listdata  # Буфер хранения сообщений из MQTT для отправки по очереди в ТСП
    payload = message.payload.decode()
    # log_message = f"Received message from MQTT topic {message.topic}: {payload}\n"
    # update_log_text(log_message)
    if "getScreen" in payload and "req" in payload:
        tIdPayload = json.loads(payload)
        app.update_log_text(f"Получено в топик: {payload}", "blue")
        if len(button_list) == 0:
            # Захватываем блокировку перед доступом к списку listdata
            with listdata_lock:
                listdata.append(payload)
                # app.update_log_text(f"Список после добавления: {listdata}", "black")
                # app.update_log_text(f"Получено в топик: {payload}", "blue")
        else:
            button_list[0]["chat_id"] = tIdPayload["tID"]
            button_list[0]["fID"] = get_last_word_before_slash(tIdPayload["fID"])
            print(button_list)
            res = button_list[0]
            send_json_request_sync(f"http://{ipWebServ}:8000/buttons/{factory}", res)
            app.update_log_text(f"Отправлено из памяти: {res}", "blue")

    if "getScreen" in payload and "mnem" in payload:
        # Захватываем блокировку перед доступом к списку listdata
        with listdata_lock:
            # app.update_log_text(f"Список до добавления: {listdata}", "black")
            listdata.append(payload)
            app.update_log_text(f"Получено в топик: {payload}", "blue")
            # app.update_log_text(f"Список после добавления: {listdata}", "black")
    else:
        pass

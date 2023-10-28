import asyncio
import os
import time

import aiosqlite


async def create_database(name_db: str, name_table: str):
    # Указываем имя файла базы данных
    db_name = name_db

    # Удаляем существующий файл базы данных (если он существует)
    if os.path.exists(db_name):
        os.remove(db_name)

    # Открываем подключение к базе данных (файл базы данных будет создан заново)
    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор для выполнения SQL-запросов
        cursor = await db.cursor()

        # Создаем таблицу с автоинкрементным первичным ключом
        await cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {name_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataMqtt TEXT,
                buttonData TEXT
            )
        ''')

        # Выполняем коммит, чтобы сохранить изменения
        await db.commit()


async def insert_data(name_db: str, name_table: str, column_name: str, data: str):
    # Указываем имя файла базы данных
    db_name = name_db

    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор для выполнения SQL-запросов
        cursor = await db.cursor()

        # Вставляем данные в таблицу и указываем имя столбца
        await cursor.execute(f'''
            INSERT INTO {name_table} ({column_name}) VALUES (?)
        ''', (data,))

        # Получаем ID последней добавленной записи
        last_inserted_id = cursor.lastrowid

        # Выполняем коммит, чтобы сохранить изменения
        await db.commit()

        # Выполняем SELECT, чтобы получить добавленную запись
        await cursor.execute(f'''
            SELECT * FROM {name_table} WHERE id = ?
        ''', (last_inserted_id,))

        # Получаем добавленную запись
        added_record = await cursor.fetchone()

        return added_record


async def delete_last_row(name_db: str, name_table: str):
    # Указываем имя файла базы данных
    db_name = name_db

    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор для выполнения SQL-запросов
        cursor = await db.cursor()

        # Получаем ID последней записи в таблице
        await cursor.execute(f'SELECT MAX(id) FROM {name_table}')
        last_id = await cursor.fetchone()

        if last_id is not None and last_id[0] is not None:
            # Удаляем последнюю запись
            await cursor.execute(f'DELETE FROM {name_table} WHERE id = ?', (last_id[0],))
            # Выполняем коммит, чтобы сохранить изменения
            await db.commit()


async def get_and_delete_first_row(name_db: str, name_table: str, column_name: str):
    # Указываем имя файла базы данных
    db_name = name_db

    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор для выполнения SQL-запросов
        cursor = await db.cursor()

        # Получаем первую запись из таблицы в указанной колонке
        await cursor.execute(f'SELECT {column_name} FROM {name_table} LIMIT 1')
        first_row = await cursor.fetchone()

        if first_row is not None:
            # Получаем ID первой записи
            await cursor.execute(f'SELECT id FROM {name_table} WHERE {column_name} = ?', (first_row[0],))
            first_row_id = await cursor.fetchone()

            if first_row_id is not None:
                first_row_id = first_row_id[0]

                # Удаляем первую запись
                await cursor.execute(f'DELETE FROM {name_table} WHERE id = ?', (first_row_id,))

                # Выполняем коммит, чтобы сохранить изменения
                await db.commit()

        return first_row


async def get_first_row(name_db: str, name_table: str, column_name: str):
    # Указываем имя файла базы данных
    db_name = name_db

    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор для выполнения SQL-запросов
        cursor = await db.cursor()

        # Получаем первую запись из таблицы в указанной колонке
        await cursor.execute(f'SELECT {column_name} FROM {name_table} LIMIT 1')
        first_row = await cursor.fetchone()

        return first_row


async def main():
    # await create_database("tcpServer_data.db", "dataMqtt")
    # await insert_data("tcpServer_data.db", "dataMqtt", "dataMqtt", "Новая запись3")
    # await delete_last_row("tcpServer_data.db", "dataMqtt")

    # deleted_row = await get_and_delete_first_row("tcpServer_data.db", "dataMqtt", "dataMqtt")
    # if deleted_row is not None:
    #     print("Удаленная строка:", deleted_row)
    pass


# Запускаем добавление данных
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

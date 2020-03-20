import sqlite3 as sql


def DBFullRead(source='data/testRN.db'):
    """ Чтение списка таблиц из БД. Возвращает список в котором кортеж из имен таблиц """

    # подключиться к БД
    con = sql.connect('data/testRN.db')
    # чтение таблиц
    with con:
        cur = con.cursor()
        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        cur.close()
        format_tables = []
        for name_table in tables:
            format_tables.append(name_table[0])
        print(format_tables)
        # вернуть список таблиц
        return format_tables


def DBCreateProjectsTable(table, time_of_create):
    """ Добавление в таблицу сведений об именах проектов и времени их создания """

    # подключиться к БД
    con = sql.connect('data/testRN.db')
    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO projects_manager VALUES (?, ?)", [table, time_of_create])
        cur.close()


def DBTableCreate(name, source='data/testRN.db'):
    """ Создание таблицы в базе """

    # подключиться к БД
    con = sql.connect('data/testRN.db')
    with con:
        cur = con.cursor()
        # создать таблицу с колонками если нет
        cur.execute('CREATE TABLE IF NOT EXISTS '+name+' ('  # создать таблицу, если не существует
            'type_po TEXT, ' # направление хода str(прямой/обратный)
            'name_stantion TEXT, '  # имя станции
            'sp FLOAT, '    # переднее плечо
            'sz FLOAT, '    # заднее плечо
            'zo1 FLOAT, '   # задний отсчет 1 по основной шкале
            'zo2 FLOAT, '   # задний отсчет 2 по основной шкале
            'po1 FLOAT, '   # передний отсчет 1 по основной шкале
            'po2 FLOAT, '   # передний отсчет 2 по основной шкале
            'pd1 FLOAT, '   # передний отсчет 1 по дополнительной шкале
            'pd2 FLOAT, '   # передний отсчет 2 по дополнительной шкале
            'zd1 FLOAT, '   # задний отсчет 1 по дополнительной шкале
            'zd2 FLOAT, '   # задний отсчет 2 по дополнительной шкале
            'zo FLOAT, '    # среднее от заднего отсчета по основной шкале
            'po FLOAT, '    # среднее от переднего отсчета по основной шкале
            'pd FLOAT, '    # среднее от переднего отсчета по дополнительной шкале
            'zd FLOAT, '    # среднее от заднего отсчета по дополнительной шкале
            'razn_o FLOAT, '# разность средних отсчетов по основной шкале (max-min)
            'razn_d FLOAT, '# разность средних отсчетов по дополнительной шкале (max-min)
            'd FLOAT, '     # допуск на отсчеты
            'd_res TEXT, '  # степень допуска (%)
            'sr_razn FLOAT, '# среднее от разностей средних отсчетов по шкалам
            'k_h INTEGER, ' # направление превышения
            'h FLOAT, '     # превышение
            's FLOAT)')     # сумма плеч
        cur.close()


def DBDropTable(table, source='data/testRN.db'):
    """ Удаление таблицы из БД """

    # подключаемся к БД
    con = sql.connect(source)
    with con:
        cur = con.cursor()
        # читаем таблицу
        cur.execute("DROP TABLE "+table)
        cur.close()
    # проверка
    if table not in DBFullRead():
        print('Таблица удалена')
    else:
        print('Ошибка удаления таблицы из БД')


def DBRead(table, source='data/testRN.db'):
    """ Чтение строк таблицы из БД. Возвращает список в котором кортеж из строк """

    # подключаемся к БД
    con = sql.connect(source)
    with con:
        cur = con.cursor()
        # читаем таблицу
        rows = cur.execute("SELECT * FROM "+table).fetchall()
        cur.close()
        # возвращаем список строк
        return rows


def DBAdd(row, source='data/testRN.db'):
    """ Добавление строки в таблицу БД. Выводит результат операции в print """

    table = row[0]
    row = row[1:]

    # подключаемся к БД
    con = sql.connect(source)
    with con:
        cur = con.cursor()
        # записать в таблицу строку
        cur.execute(f"INSERT INTO "+table+" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
        cur.close()
        # если строка не в таблице то
        if [table]+row not in DBRead(table):
            # print('Строка', row, 'записана в табицу', table)
            print('Строка', row, 'записана в табицу', table)
        # иначе print('Строка не записана')
        else: print('Строка не записана')


def DBDelete(row, source='data/testRN.db'):
    """ Удаление строки (с такими же направлением и станцией как в принимаемой строке) из таблицы БД. Выводит результат операции в print"""

    table = row[0]
    row = row[1:]

    # подключаемся к БД
    con = sql.connect(source)
    with con:
        cur = con.cursor()
        # если кол-во строк в таблице не равно нулю то
        if len(DBRead(table)) != 0:
            # удалить строку из таблицы row[0] по значениями станции и направления хода
            cur.execute(
                'DELETE FROM '+table+' WHERE '
                'type_po = "'+row[0]+'" AND '
                'name_stantion = "'+row[1]+'"'
                )
            # если строка не в таблице то
            if [table]+row not in DBRead(table):
                # print('Строка', row, 'удалена из табицы', table)
                print('Строка', row, 'удалена из табицы', table)
            # иначе print('Строка не удалена')
            else: print('Строка не удалена')
        # иначе print('Пустая таблица')
        else: print('Пустая таблица')
        cur.close()


def DBTest(row, source='data/testRN.db'):
    """ Проверка наличия строки в таблице. Возвращает True или False """

    table = row[0]
    row = row[1:]

    # подключиться к БД
    con = sql.connect(source)
    with con:
        cur = con.cursor()
        # если кол-во строк не равно нулю то
        if len(DBRead(table)) != 0:
            # если строка есть в таблице то вернуть True
            if [table]+row in DBRead(table):
                print('В таблице есть такая же строка')
                return True
            # иначе вернуть False
            else:
                print('В таблице нет такой же строки')
                return False
        # иначе print('Таблица пуста')
        else: print('Таблица пуста')
        cur.close()


def DBTestCastom(row, source='data/testRN.db'):
    """ Проверка наличия строки в таблице. Возвращает True или False """

    # для каждой строки из прочитанной таблицы
    for old_row in DBRead(row[0]):
        # если напр хода и имя станции полученной строки равно напр хода и имени станции из проверяемой строки
        if old_row[0] == row[1] and old_row[1] == row[2]:
            print('В таблице есть строка с таким напр хода и именем станции')
            # то вернуть True
            return True
        # иначе продолжить цикл
        else:
            continue
    # вернуть False
    else:
        print('В таблице нет строки с таким напр хода и именем станции')
        return False
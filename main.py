import sqlite3
import pandas as pd

con = sqlite3.connect("FitClub.sqlite")
f_damp = open('FitClub.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()
cursor = con.cursor()

con.commit()

# Расписание тренерского состава. Сортировка по именам и дате
def TrRasp ():
    df = pd.read_sql(''' 
        SELECT fio_tr as ФИО, t.data_tr as Дата, t.nach_tr as Начало, t.kon_tr as Конец
        FROM Trainer JOIN TrainerRasp t USING (idTrainer)
        ORDER BY ФИО, Дата ASC
         ''', con)
    print(df)

#Специализация тренерского состава. Сортировка по именам
def TrSpec():
    df = pd.read_sql(''' 
        SELECT idTrainer as Номер , fio_tr as ФИО, t.spec as Специальность
        FROM Trainer JOIN TrainerSpec t using (idTrainerSpec)
        ORDER BY ФИО ASC
         ''', con)
    print(df)

# Вывести тренеров, которые работают >= 4 ч.
def RabBolFour():
    df = pd.read_sql(''' 
        SELECT fio_tr as ФИО, idTrainer as Номер
        FROM Trainer
        LEFT JOIN TrainerRasp USING (idTrainer) 
        GROUP BY Номер HAVING (time(kon_tr) - time(nach_tr)) >= 4 
        ''',con)
    print(df)

# Вывести кол-во тренеров каждой специализации
def ColSpec():
    df = pd.read_sql('''
        SELECT spec as Специализация, count(t.spec ) as Кол_во
        FROM Trainer 
        JOIN TrainerSpec t USING (idTrainerSpec)
        GROUP BY Специализация 
         ''',con)
    print(df)

# Запись клиента на посещение
def inPos():
    cursor.executescript('''
    UPDATE Poseshenie 
    SET idClients = 1, oplata = true
    WHERE idPoseshenie=1
    ''')



def inCli():
    cursor.executescript('''
    INSERT INTO Clients (idClients, fio, age, gender, pass)
    VALUES (11,'Тест', 99, 'Тест', '000000');
    ''')
# Удаление клиента
def delPos(passnum):
    cursor.executescript(f'''
    DELETE
    FROM Clients 
    WHERE pass = {passnum};
''')



# Тренер с наибольшим числом тренировок в расписании
def GigTr():
   df = pd.read_sql(''' 
       SELECT fio_tr as ФИО, count(*) as Количество FROM Trainer
       JOIN TrainerRasp USING (idTrainer)
       GROUP BY fio_tr 
       HAVING count(fio_tr) = (SELECT count(idTrainer) FROM TrainerRasp
       GROUP BY idTrainer ORDER BY count(idTrainer) DESC )
        ''', con)
   print(df)

#Свободные записи для ОФП с Отображением тренера
def OFPTr():
    df = pd.read_sql('''
     WITH temp as (SELECT idTrainer, idTrainerRasp, t.fio_tr
     FROM TrainerRasp JOIN Trainer t USING (idTrainer)
     WHERE idTrainerRasp = 1 )
     SELECT idPoseshenie as Номер_записи, 
     pos_data as Дата_посещения, 
     pos_time as Время_посещения, 
     fio_tr as ФИО 
     FROM temp 
     JOIN Poseshenie USING (idTrainerRasp)  WHERE idClients is NULL
     ''', con)
    print(df)

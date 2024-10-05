from bs4 import BeautifulSoup
import pyodbc
import numpy

    
def WellcomeMasage():
    print("""            Hasan hoca Accsses database ödev yapıcıya hoş geldin 
                Bu program html ve txt dosyasındaki Zarar veren hadiseler
                ve depremleri otomatik bir şekilde accsses veritabanına aktarır

                gerekli html ve txt dosyalarına sahip olduğundan emin ol
                (DOSYALAR İLE PROGRAM AYNI DOSYA İÇERİSİNDE OLMALIDIR)
      
                2024 Neptün Kırçiçek  V1.0""")


def HarmfullEventHandler(fileName, tableName, column1, column2, column3, column4, column5):

        
    conn_str = (f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={Data_BasePath};')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    with open(f'{fileName}', 'r', encoding='utf-8') as file:
        html_cont = file.read()
        soup = BeautifulSoup(html_cont, 'html.parser')

    list_NO = []
    list_Date = []
    list_Location = []
    list_Event = []
    list_Damage = []
    list_RAWDATA = []

    for i in soup.find_all('td'):
        list_RAWDATA.append(i.string)

    dataSetLenght = len(list_RAWDATA)
    for INDEX in range(9,dataSetLenght,5):
        list_NO.append(list_RAWDATA[INDEX])
        list_Date.append(list_RAWDATA[INDEX+1])
        list_Location.append(list_RAWDATA[INDEX+2])
        list_Event.append(list_RAWDATA[INDEX+3])
        list_Damage.append(list_RAWDATA[INDEX+4])
    
    for i in range(len(list_Date)):
        cursor.execute(f"INSERT INTO {tableName} ({column1}, {column2}, {column3}, {column4},{column5}) VALUES (?, ?, ?, ?, ?)", 
                    (list_NO[i],list_Date[i], list_Location[i], list_Event[i], list_Damage[i]))

        cursor.commit()
    
def EarthquakeEventHandler(fileName, tableName,columnID, column1, column2, column3, column4, column5, column6, column7,column8,column9,column10):
    conn_str = (f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={Data_BasePath};')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    with open(f'{fileName}', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    list_Date=[]
    list_Clock=[]
    list_Lat=[]
    list_Long=[]
    list_Depth=[]
    list_MD=[]
    list_ML=[]
    list_MW = []
    list_Loc = []
    list_Solve = []
    
    for line in lines:
        parts = line.split()  # Boşluklara göre ayırma
        
        list_Date.append(parts[0])
        list_Clock.append(parts[1])
        list_Lat.append(parts[2])
        list_Long.append(parts[3])
        list_Depth.append(parts[4])
        list_MD.append(parts[5])
        list_ML.append(parts[6])
        list_MW.append(parts[7])
        list_Loc.append(" ".join(parts[8:-1]))  
        list_Solve.append(parts[-1])

    for i in range(len(list_Date)):
        cursor.execute(f"INSERT INTO {tableName} ({columnID},{column1},{column2},{column3},{column4},{column5}, {column6}, {column7}, {column8}, {column9},{column10}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (i,list_Date[i], list_Clock[i], list_Lat[i], list_Long[i], list_Depth[i], list_MD[i], list_ML[i], list_MW[i], list_Loc[i],list_Solve[i]))
    cursor.commit()

def Main(dataBasePath):

    conn_str = (f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={dataBasePath};')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()


    translate_type_select_question = input("HTML'den mi yoksa txt dosyasından mı veri aktaracaksın (H / T)")
    translate_type_select_question = translate_type_select_question.upper()
    if translate_type_select_question == "H":
        print("Veritabanındaki tabloların")

        for i in cursor.tables(tableType='TABLE'):
            print(i.table_name)
            
        new_table_question = input("Yeni bir tablo eklemek ister misin? (Y/N)")
        new_table_question = new_table_question.upper()

        if new_table_question == "Y":

            new_table_name = input("Yeni oluşturulacak tablonun ismini gir :")
            new_table_no = input("Yeni tablodaki NO alanının ismini gir :")
            new_table_date = input("Yeni tablodaki TARİH alanının ismini gir :")
            new_table_location = input("Yeni tablodaki YER alanının ismini gir :")
            new_table_event = input("Yeni tablodaki OLAY alanının ismini gir :")
            new_table_damage = input("Yeni tablodaki HASAR alanının ismini Bgir :")

            cursor.execute(f'create table {new_table_name} ({new_table_no} Text,{new_table_date} Text,{new_table_location} Text,{new_table_event} Text,{new_table_damage} Text)')
            cursor.commit()

            auto_insert_question = input("Bu tabloyu verecğin dosyaya göre otomatik doldurmamı ister misin (Y/N)")
            auto_insert_question = auto_insert_question.upper()

            if auto_insert_question == "Y":
            
                file_name = input("Bu program ile aynı dizinde olan html dosyasının ismini uzantısı ile beraber yaz :")

                HarmfullEventHandler(file_name,new_table_name,new_table_no,new_table_date,new_table_location,new_table_event,new_table_damage)
                print("Tamamdır")
            elif auto_insert_question == "N":
                print("Tek tek yazmaya başlasan iyi edersin o zaman")
            else:
                print("Anlayacağım şekilde konuş")
        elif new_table_question == "N":
            table_name = input("İşlem yapmak istediğin tablonun ismini gir  :")
            file_name = input("Aktarılacak HTML dosayını uzantısı ile beraber gir  :")
            column_no = input("NO alanının ismini gir  :")
            column_date = input("Tarih alanının ismini gir  :")
            column_loc = input("Yer alanının ismini gir  :")
            column_event = input("Olay alanının ismini gir  :")
            column_damage = input("Zarar alanının ismini gir  :")

            HarmfullEventHandler(file_name,table_name,column_no,column_date,column_loc,column_event,column_damage)

        else:
            print("Sorulara lütfen doğru bir şekilde cevap ver")
        

    if translate_type_select_question == "T":
        print("Veritabanındaki tabloların")

        for i in cursor.tables(tableType='TABLE'):
            print(i.table_name)
            
        new_table_question = input("Yeni bir tablo eklemek ister misin? (Y/N)")
        new_table_question = new_table_question.upper()

        if new_table_question == "Y":

            new_table_name  = input("Yeni oluşturulacak tablonun ismini gir :")
            new_table_date  = input("Yeni tarih alanının ismi ne olsun ?")
            new_table_clock = input("Yeni saat alanının ismi ne olsun ?")
            new_table_lat   = input("Yeni enlem alanının ismi ne olsun ?")
            new_table_long  = input("Yeni boylam alanının ismi ne olsun ?")
            new_table_depth = input("Yeni derinlik alanının ismi ne olsun ?")
            new_table_MD    = input("Yeni MD alanının ismi ne olsun ?")
            new_table_ML    = input("Yeni ML alanının ismi ne olsun ?")
            new_table_MW    = input("Yeni MW alanının ismi ne olsun ?")
            new_table_loc   = input("Yeni Yer alanının ismi ne olsun ?")
            new_table_solve = input("Yeni  Çözüm niteliği alanının ismi ne olsun ?")
            
            cursor.execute(f'create table {new_table_name} (ID Number,{new_table_date} Text,{new_table_clock} Text,{new_table_lat} Text,{new_table_long} Text,{new_table_depth} Text,{new_table_MD} Text,{new_table_ML} Text,{new_table_MW} Text,{new_table_loc} Text, {new_table_solve} Text)')
            cursor.commit()

            auto_insert_question = input("Bu tabloyu verecğin dosyaya göre otomatik doldurmamı ister misin (Y/N)")
            auto_insert_question = auto_insert_question.upper()

            if auto_insert_question == "Y":
            
                file_name = input("Bu program ile aynı dizinde olan txt dosyasının ismini uzantısı ile beraber yaz :")

                EarthquakeEventHandler(file_name,new_table_name,"ID",new_table_date,new_table_clock,new_table_lat,new_table_long,new_table_depth,new_table_MD,new_table_ML,new_table_MW,new_table_loc,new_table_solve)
                print("Tamamdır")
            elif auto_insert_question == "N":
                print("Tek tek yazmaya başlasan iyi edersin o zaman")
            else:
                print("Anlayacağım şekilde konuş")





WellcomeMasage()
Data_BasePath =  input("Başlamak için lütfen veritabanı dosya yolunu gir    : ")
Main(Data_BasePath)   
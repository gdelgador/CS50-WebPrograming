import os,json
import pyodbc as podbc
import pandas as pd

# import pandas as pd
# import numpy as np

# def tuple_comp(df): return [tuple(x) for x in df.to_numpy()]
# def iter_namedtuples(df): return list(df.itertuples(index=False))
# def iter_tuples(df): return list(df.itertuples(index=False, name=None))
# def records(df): return df.to_records(index=False).tolist()
# def zipmap(df): return list(zip(*map(df.get, df)))
# https://i.stack.imgur.com/1x7vK.png

def leyendo_data(ruta_sql):
    try:
        F=open(ruta_sql, 'r',encoding='utf-8')
        data = F.read().replace('\n', ' ').replace('\t',' ')
        data=" ".join(data.split()) 
        F.close()
        return data
    except:
        print('Hubo un error abriendo el archivo, revisar ruta:{}!!'.format(ruta_sql))
    pass

class SQL_CONECT_PANDAS:
    def __init__(self,driver,server,database,username,password):
        #inicializando variables de conexión
        self.driver=driver
        self.server=server
        self.database=database
        self.username=username
        self.password=password
        #comprobando valores
        if(self.server==None or self.database==None or self.username==None or self.password==None):
            print('Ingrese los elementos de conexion')
    
    def conexion_sql_server(self):
        print("realizando conexion SQL")
        try:
            self.connection = podbc.connect('DRIVER='+self.driver+
                                        ';SERVER='+self.server+
                                        ';DATABASE='+self.database+
                                        ';UID='+self.username+
                                        ';PWD='+ self.password)
            print("exito!!")
            return self.connection
        except Exception as e:
            print(e)
    
    #función select to DF
    def select_to_df(self,sql_query):
       #conectando a la base de datos
        connection=self.conexion_sql_server()
        try:
            #pasanod info a df
            df = pd.read_sql(sql_query, connection)
        except Exception as e:
            print(e)
        #cerrando conexion
        connection.close()
        return df
    
    def delete_sql(self,sql_query):
        print('eliminando elementos según query')
        #conectando a la base de datos
        connection=self.conexion_sql_server()
        try:
            #ejecutando
            cursor = connection.cursor()
            cursor.execute(sql_query)
            connection.commit()
        except Exception as e:
            print(e)
        #close conexiones
        cursor.close()
        connection.close()
    
    def insert_sql(self,df,table_name,*columnas):
        #start conexion sql
        connection=self.conexion_sql_server()
        #generate sql insert
        valores=', '.join(map(str, columnas))
        incognita=', '.join(map(lambda x: '?',columnas))
        sql_insert="INSERT INTO {} ({}) VALUES ({})".format(table_name,valores,incognita)
        #generate data records
        data_record=df[list(columnas)].to_records(index=False).tolist()
        try:
            #execute comands
            cursor = connection.cursor()
            cursor.executemany(sql_insert,data_record)
            cursor.commit() 
        except Exception as e:
            print(e)
        #close conexiones
        cursor.close()
        connection.close()

    pass


if __name__ == "__main__":
    
    #credenciales
    input_credenciales_sql={'driver':'{SQL Server Native Client 11.0}',
                    'server':r'LIM-CG8H0Z2\GONZALOSQL',
                    'database':'db_pruebas',
                    'username':'gdelgado',
                    'password':'gdelgado'}
    #ruta files
    consulta='./consultas/clientes_SF.txt'

    #########################
    #iniciando clase sql PANDAS
    ########################

    # sql_class = SQL_SERVER(server,database,username,password)
    sql_class = SQL_CONECT_PANDAS(**input_credenciales_sql)
    sql_query='select * from db_pruebas..Consumer_Complaints_2'

    df=sql_class.select_to_df(sql_query)

    print(df.head())
    print(df.columns)
    


    ###USING SPARK
    from pyspark import SparkContext, SparkConf, SQLContext
    
    ruta_json='spark_entornos.json'
    spark_version='spark-2.4.4'
    set_enviroment(ruta_json,spark_version)
    import findspark
    findspark.init()
    findspark.find()
    import pyspark
    print(findspark.find())

    appName = "PySpark SQL Server Example - via ODBC"
    master = "local"
    conf = SparkConf() \
        .setAppName(appName) \
        .setMaster(master) 
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    spark = sqlContext.sparkSession

    sparkDF =  spark.createDataFrame(df)
    sparkDF.show()

    pass



import mysql.connector
from dotenv import load_dotenv
from flask import request  # Importando request
import os

class MySQLDatabase:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexão ao banco de dados MySQL estabelecida com sucesso!")
        except mysql.connector.Error as error:
            print("Erro ao conectar ao banco de dados MySQL:", error)

    def execute_query(self, query):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
            except mysql.connector.Error as error:
                print("Erro ao executar a consulta:", error)
            finally:
                cursor.close()

    def execute_stored_procedure(self, procedure_name, params=None):
        """
        Executa uma Stored Procedure no banco de dados MySQL.
        
        :param procedure_name: Nome da Stored Procedure.
        :param params: Parâmetros da Stored Procedure, se houver.
        :return: Resultados da execução da Stored Procedure.
        """
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                if params:
                    cursor.callproc(procedure_name, params)
                else:
                    cursor.callproc(procedure_name)
                
                # Coletando resultados da Stored Procedure
                results = []
                for result in cursor.stored_results():
                    results.append(result.fetchall())
                
                return results
            except mysql.connector.Error as error:
                print(f"Erro ao executar a Stored Procedure {procedure_name}:", error)
            finally:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexão ao banco de dados MySQL foi encerrada.")

    def get_argument(self, key):
        return request.args.get(key)  # Obtendo o valor do argumento da URL usando request.args.get()

    @property
    def args(self):
        return request.args  # Retornando os argumentos da URL diretamente usando request.args

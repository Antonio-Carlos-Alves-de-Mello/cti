from db.MySQLDatabase import MySQLDatabase
from flask import Flask , render_template, session, request, url_for
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    session.clear
    db = MySQLDatabase()
    db.connect()
    lojas = db.execute_query("SELECT CNPJ, FANTASIA FROM Lojas order by FANTASIA")
    cnpj = request.args.get('cnpj')

    detalhes_loja = None
    if cnpj:
        loja = db.execute_query(f"SELECT RAZAO, cnpj, ie, ENDERECO, CEP FROM Lojas where cnpj = '{cnpj}'")
        ips = db.execute_query(f"SELECT SETOR, IP, MAQUINA FROM Ips WHERE CNPJ = '{cnpj}' order by SETOR")
        contatos = db.execute_query(f"SELECT idsetor ,setores.SETOR, Contatos.TELEFONE, Contatos.TIPO, Contatos.CONTATO FROM Contatos inner join setores on Contatos.idsetor = setores.id where CNPJ = '{cnpj}' order by setor")
        detalhes_loja = {'loja' : loja, 'ips': ips, 'contatos': contatos}
        
    return render_template('index.html', lojas=lojas, detalhes_loja=detalhes_loja)
@app.route('/sistema/acesso')
def acesso():
    return render_template('/sistema/acesso/acesso.html')

@app.route('/sistema/cadastro') 
def cadUsuario():
    return render_template('/sistema/cadastro.html')

@app.route('/sistema/tecnicos')
def tecnicos():
    return render_template('/sistema/tecnicos/tecnicos.html')

@app.route('/sistema/estoque')
def estoque():
    session.clear
    db = MySQLDatabase()
    db.connect()
    
    estoque = db.execute_query(f"Call Consulta_Estoque_01")
    dados_estoque = {'produtos': estoque}
              
    return render_template('/sistema/estoque/estoque.html', dados_estoque=dados_estoque)       
      
@app.route('/sistema/requisicoes')
def material():
    return render_template('/sistema/requisicoes/material.html')
    
if __name__ == '__main__':
    app.run(debug=True)
    
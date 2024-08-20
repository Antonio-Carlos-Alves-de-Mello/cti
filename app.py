from db.MySQLDatabase import MySQLDatabase
from flask import Flask, render_template, session, request, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.bigbox.com.br'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

@app.route('/')
def index():
    session.clear()
    db = MySQLDatabase()
    db.connect()
    lojas = db.execute_query("SELECT CNPJ, FANTASIA FROM Lojas ORDER BY FANTASIA")
    cnpj = request.args.get('cnpj')

    detalhes_loja = None
    if cnpj:
        loja = db.execute_query("SELECT RAZAO, CNPJ, IE, ENDERECO, CEP FROM Lojas WHERE CNPJ = %s", (cnpj,))
        ips = db.execute_query("SELECT SETOR, IP, MAQUINA FROM Ips WHERE CNPJ = %s ORDER BY SETOR", (cnpj,))
        contatos = db.execute_query("""
            SELECT idsetor, setores.SETOR, Contatos.TELEFONE, Contatos.TIPO, Contatos.CONTATO
            FROM Contatos
            INNER JOIN setores ON Contatos.idsetor = setores.id
            WHERE CNPJ = %s ORDER BY setores.SETOR
        """, (cnpj,))
        detalhes_loja = {'loja': loja, 'ips': ips, 'contatos': contatos}
        
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
    session.clear()
    db = MySQLDatabase()
    db.connect()
    produto = db.execute_query("SELECT id, nome FROM Produtos ORDER BY nome")
    id_produto = request.args.get('id')
    
    if id_produto:
        id_produto = int(id_produto)
        estoque = db.execute_query("CALL Consulta_Estoque_01")
        cProduto = db.execute_query("CALL bd_CTI.Consulta_Estoque_produto(%s)", (id_produto,))
    else:
        estoque = db.execute_query("CALL Consulta_Estoque_01")
        cProduto = None
    
    produtos = {'produto': produto}
    material = {'estoque': estoque}
    consultaPorProduto = {'cProduto': cProduto}
        
    return render_template('/sistema/estoque/estoque.html', produtos=produtos, material=material, consultaPorProduto=consultaPorProduto)       
      
@app.route('/sistema/requisicoes', methods=['GET', 'POST'])
def material():
    if request.method == 'POST':
        loja = request.form['nomeLoja']
        numero_chamado = request.form['numeroChamado']
        material = request.form['material']
        quantidade = request.form['qnt']
        observacao = request.form['observacao']

        # Salvar no banco de dados MySQL
        session.clear()
        db = MySQLDatabase()
        db.connect()
        query = """
        INSERT INTO requisicoes (loja, numero_chamado, material, quantidade, observacao)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_query(query, (loja, numero_chamado, material, quantidade, observacao))
        
        # Enviar e-mail
        msg = Message('Nova Requisição Registrada',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['suporte@bigbox.com.br'])
        msg.body = f'''
        Loja: {loja}
        Número do Chamado: {numero_chamado}
        Material: {material}
        Quantidade: {quantidade}
        Observação: {observacao}
        '''
        mail.send(msg)

    return render_template('/sistema/requisicoes/material.html')

if __name__ == '__main__':
    app.run(debug=True)

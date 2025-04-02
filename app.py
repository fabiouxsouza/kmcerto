from flask import Flask, render_template, request, jsonify  # Importe 'request' e 'jsonify'
import sqlite3  # Importe a biblioteca sqlite3
from datetime import datetime # Importe a biblioteca datetime

app = Flask(__name__)

# --- Funções auxiliares para o banco de dados ---

def get_db_connection():
    """
    Função para estabelecer uma conexão com o banco de dados SQLite.
    Cria o banco de dados 'diarias.db' se ele não existir.
    """
    conn = sqlite3.connect('diarias.db')
    conn.row_factory = sqlite3.Row  # Define a fábrica de linhas para acessar colunas por nome
    return conn

def init_db():
    """
    Função para inicializar o banco de dados (criar a tabela se ela não existir).
    """
    conn = get_db_connection()  # Obtém uma conexão com o banco de dados
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS diarias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia TEXT NOT NULL,
                km_rodados REAL NOT NULL,
                horas_trabalhadas REAL NOT NULL,
                ganhos REAL,
                combustivel REAL,
                almoco REAL,
                manutencao REAL,
                seguro REAL,
                financ REAL,
                pro_labore REAL,
                despesas_totais REAL,
                lucro REAL
            )
        ''')  # Executa o comando SQL para criar a tabela 'diarias'
        conn.commit()  # Salva as alterações no banco de dados
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")  # Imprime erros no console
    finally:
        conn.close()  # Fecha a conexão com o banco de dados

# Inicializa o banco de dados quando o aplicativo é iniciado
init_db()

# --- Rotas do Flask ---

@app.route('/')
def index():
    """
    Rota para a página inicial, que renderiza o template 'index.html'.
    """
    return render_template('index.html')

@app.route('/diarias', methods=['GET', 'POST'])
def diarias():
    """
    Rota para lidar com a criação e recuperação de dados de diárias.

    - POST: Recebe os dados do formulário, calcula ganhos, despesas e lucro,
            e salva os dados no banco de dados. Retorna os dados salvos em JSON.
    - GET: Recupera todos os dados de diárias do banco de dados e retorna em JSON.
    """
    conn = get_db_connection()  # Obtém uma conexão com o banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

    if request.method == 'POST':
        try:
            # Obter dados do formulário
            dia = request.form['dia']
            km_rodados = float(request.form['km_rodados'])
            horas_trabalhadas = float(request.form['horas_trabalhadas'])
            combustivel = float(request.form['combustivel'])
            almoco = float(request.form['almoco'])
            manutencao = float(request.form['manutencao'])
            seguro = float(request.form['seguro'])
            financ = float(request.form['financ'])
            pro_labore = float(request.form['pro_labore'])

            # Calcular ganhos
            ganhos = (horas_trabalhadas == 0) ? 0 : km_rodados * 1.89 / horas_trabalhadas

            # Calcular despesas totais
            despesas_totais = combustivel + almoco + manutencao + seguro + financ + pro_labore

            # Calcular lucro
            lucro = ganhos - despesas_totais

            # Inserir dados no banco de dados
            cursor.execute('''
                INSERT INTO diarias (
                    dia, km_rodados, horas_trabalhadas, ganhos, combustivel, almoco,
                    manutencao, seguro, financ, pro_labore, despesas_totais, lucro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dia, km_rodados, horas_trabalhadas, ganhos, combustivel, almoco,
                  manutencao, seguro, financ, pro_labore, despesas_totais, lucro))

            conn.commit()  # Salva as alterações no banco de dados

            # Recuperar os dados inseridos para retornar como JSON
            cursor.execute("SELECT * FROM diarias WHERE id = last_insert_rowid()")
            data = dict(cursor.fetchone())  # Obtenha os dados como um dicionário

            return jsonify(data), 201  # Retorna os dados inseridos com código 201 (Created)

        except Exception as e:
            conn.rollback()  # Em caso de erro, desfaz as alterações
            return jsonify({"error": str(e)}), 400  # Retorna mensagem de erro com código 400 (Bad Request)

        finally:
            conn.close()  # Fecha a conexão com o banco de dados

    elif request.method == 'GET':
        try:
            # Recuperar todos os dados do banco de dados
            cursor.execute("SELECT * FROM diarias")
            rows = cursor.fetchall()  # Obtenha todos os dados

            # Converter as linhas em uma lista de dicionários
            diarias = [dict(row) for row in rows]

            return jsonify(diarias), 200  # Retorna os dados com código 200 (OK)

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Retorna mensagem de erro com código 500 (Internal Server Error)

        finally:
            conn.close()  # Fecha a conexão com o banco de dados

if __name__ == '__main__':
    app.run(debug=True)
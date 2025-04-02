from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('diarias.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diarias', methods=['GET', 'POST'])
def diarias():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            dia = request.form['dia']
            km_rodados = float(request.form['km_rodados'])
            horas_trabalhadas = float(request.form['horas_trabalhadas'])
            combustivel = float(request.form['combustivel'])
            almoco = float(request.form['almoco'])
            manutencao = float(request.form['manutencao'])
            seguro = float(request.form['seguro'])
            financ = float(request.form['financ'])
            pro_labore = float(request.form['pro_labore'])

            # Calcular ganhos (corrigido)
            if horas_trabalhadas == 0:
                ganhos = 0
            else:
                ganhos = km_rodados * 1.89 / horas_trabalhadas

            despesas_totais = combustivel + almoco + manutencao + seguro + financ + pro_labore

            lucro = ganhos - despesas_totais

            cursor.execute('''
                INSERT INTO diarias (
                    dia, km_rodados, horas_trabalhadas, ganhos, combustivel, almoco,
                    manutencao, seguro, financ, pro_labore, despesas_totais, lucro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dia, km_rodados, horas_trabalhadas, ganhos, combustivel, almoco,
                  manutencao, seguro, financ, pro_labore, despesas_totais, lucro))

            conn.commit()

            cursor.execute("SELECT * FROM diarias WHERE id = last_insert_rowid()")
            data = dict(cursor.fetchone())

            return jsonify(data), 201

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

        finally:
            conn.close()

    elif request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM diarias")
            rows = cursor.fetchall()

            diarias = [dict(row) for row in rows]

            return jsonify(diarias), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
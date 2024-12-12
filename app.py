from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://example_sum_postgres_3qkn_user:nSkwUR0ygS2dEEWA09qgGV9jBApRe8To@dpg-ctd3aijqf0us73bk5080-a.oregon-postgres.render.com/example_sum_postgres_3qkn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def add_numbers(a, b):
    return a + b


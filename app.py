from flask import Flask, request, jsonify

app = Flask(__name__)

def add_numbers(a, b):
    return a + b


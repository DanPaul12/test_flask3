from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://example_sum_postgres_3qkn_user:nSkwUR0ygS2dEEWA09qgGV9jBApRe8To@dpg-ctd3aijqf0us73bk5080-a.oregon-postgres.render.com/example_sum_postgres_3qkn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Sum(db.Model):  # Use `db.Model` as the base class for SQLAlchemy models
    __tablename__ = "Sum"
    id = db.Column(db.Integer, primary_key=True)  # Use `db.Column` to define columns
    num1 = db.Column(db.Integer, nullable=False)
    num2 = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sum {self.id}: {self.num1} + {self.num2} = {self.result}>'
    
class SumSchema(ma.Schema):
    id = fields.Integer()
    num1 = fields.Integer()
    num2 = fields.Integer()
    result = fields.Integer()

sum_schema = SumSchema()
sums_schema = SumSchema(many=True)

@app.route('/sum', methods=['GET'])
def find_all():
    sums = db.session.execute(db.select(Sum)).scalars()
    return sums_schema.jsonify(sums), 200

@app.route('/sum/<int:result>', methods=['GET'])
def find_by_result(result):
    sums = db.session.execute(db.select(Sum).where(Sum.result == result)).scalars()
    if not sums:
        return jsonify({'error': 'No sums found with the specified result'}), 404
    return sums_schema.jsonify(sums), 200

@app.route('/sum', methods = ['POST'])
def sum():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2

    with Session(db.engine) as session:
        with session.begin():
            sum_entry = Sum(num1 = num1, num2=num2, result=result)
            session.add(sum_entry)

    return jsonify({'result': result})

with app.app_context():
    db.drop_all()
    db.create_all()


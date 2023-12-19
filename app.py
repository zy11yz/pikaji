# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 15:27
# @Author  : Zhaoyang
# @FileName: app.py
# @Software: PyCharm


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pikaji.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BeyondTheSun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    subcategory = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    english_content = db.Column(db.String, nullable=True)
    chinese_content = db.Column(db.String, nullable=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_content', methods=['GET'])
def get_content():
    category = request.args.get('category', type=str)
    subcategory = request.args.get('subcategory', type=str)
    name = request.args.get('name', type=str)

    query = BeyondTheSun.query

    if category:
        query = query.filter(BeyondTheSun.category == category)
    if subcategory:
        query = query.filter(BeyondTheSun.subcategory == subcategory)
    if name:
        query = query.filter(BeyondTheSun.name == name)

    results = query.all()
    return jsonify([{'id': item.id, 'category': item.category, 'subcategory': item.subcategory,
                     'name': item.name, 'english_content': item.english_content,
                     'chinese_content': item.chinese_content} for item in results])


@app.route('/get_dropdown_option')
def get_dropdown_option():
    field = request.args.get('field', type=str)

    if field not in ['category', 'subcategory', 'name']:
        return jsonify({'error': 'Invalid field'}), 400

    query = BeyondTheSun.query

    category = request.args.get('category', type=str)
    subcategory = request.args.get('subcategory', type=str)
    if category:
        query = query.filter(BeyondTheSun.category == category)
    if subcategory:
        query = query.filter(BeyondTheSun.subcategory == subcategory)
    # 动态选择列
    field_column = getattr(BeyondTheSun, field, None)

    if field_column is None:
        return jsonify({'error': 'Invalid field'}), 400

    distinct_values = query.with_entities(field_column).distinct().all()
    values = [value[0] for value in distinct_values]

    return jsonify(values)


if __name__ == '__main__':
    app.run(debug=True)

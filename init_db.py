# -*- coding: utf-8 -*-
# @Time    : 2023/10/20 15:27
# @Author  : Zhaoyang
# @FileName: test_talos.py
# @Software: PyCharm

from app import db, app
from app import BeyondTheSun


def import_data(filename):
    with app.app_context():
        db.create_all()
        db.session.query(BeyondTheSun).delete()
        db.session.commit()
        with open(filename, 'r') as file:
            for line in file:
                category, subcategory, name, english_content, chinese_content = line.strip().split(',')
                print(f'{category} {subcategory} {name} {english_content} {chinese_content}')
                new_entry = BeyondTheSun(
                    category=category,
                    subcategory=subcategory,
                    name=name,
                    english_content=english_content,
                    chinese_content=chinese_content
                )
                db.session.add(new_entry)
            print(BeyondTheSun.query.all())
            db.session.commit()


if __name__ == '__main__':
    import_data('data.txt')

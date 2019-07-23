
from flask import Flask, jsonify, make_response, request
import mysql.connector as mysql

mydb = mysql.connect(
  host="172.17.0.2",
  user="root",
  passwd="password",
  database="test"
)

app = Flask(__name__)

items = [ ]

@app.route('/items', methods=['POST'])
def create_item():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    items.append(item)
    return jsonify({'item': item}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/items', methods=['GET'])
def get_items():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM `sample`")

    myresult = mycursor.fetchall()
    return jsonify({'items': myresult})

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

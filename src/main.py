"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todolist
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/get_task', methods=['GET'])
def get_task_td():
    gt_task = Todolist.query.all()
    all_task = list(map(lambda x: x.serialize(), gt_task))
    return jsonify(all_task), 200

@app.route('/post_task', methods=['POST'])
def post_task_td():
    request_body = request.get_json()
    insert_task = Todolist(td_task=request_body["label"], is_done=request_body["done"])
    db.session.add(insert_task)
    db.session.commit()
    return jsonify({"Todo ok" : request_body }), 200


@app.route('/del_task/<int:numb>', methods=['DELETE'])
def del_task_td(numb):
    task = Todolist.query.filter_by(id = numb).first()
    if task is None:
        raise APIException('Lo que buscas no existe', status_code=404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"Elementos elimando numero de ID:": numb}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

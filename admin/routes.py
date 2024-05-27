from flask import Blueprint, request, jsonify
from models import db, Dog

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/add_dog', methods=['POST'])
def add_dog():
    data = request.get_json()
    name = data.get('name')
    dog_type = data.get('type')
    number_available = data.get('number_available', True)

    if not name or not dog_type:
        return jsonify({"error": "Name and type are required"}), 400

    new_dog = Dog(name=name, type=dog_type, number_available = number_available)
    db.session.add(new_dog)
    db.session.commit()
    return jsonify({"message": "Dog added successfully"}), 201

from flask import Blueprint, request, jsonify
from models import db, Dog

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/category/number', methods=['POST'])
def add_dogs():
    data = request.get_json()
    name = data.get('name')
    dog_type = data.get('type')
    number = data.get('number')

    if not name or not dog_type or not number:
        return jsonify({"error": "Name, type, and number are required"}), 400

    current_dogs_count = db.session.query(db.func.sum(Dog.number_available)).filter_by(type=dog_type).scalar() or 0
    if current_dogs_count + number > 20:
        return jsonify({"error": "Cannot exceed maximum of 20 dogs per type"}), 400

    existing_dog = Dog.query.filter_by(name=name, type=dog_type).first()
    if existing_dog:
        existing_dog.number_available += number
    else:
        new_dog = Dog(name=name, type=dog_type, number_available=number)
        db.session.add(new_dog)

    db.session.commit()
    return jsonify({"message": f'{number} dogs of type {dog_type} added successfully'}), 200

@admin_bp.route('/show_category', methods=['GET'])
def show_category():
    dog_types = db.session.query(Dog.type).distinct().all()
    return jsonify({"categories": [type_[0] for type_ in dog_types]}), 200

@admin_bp.route('/list_dog', methods=['GET'])
def list_dogs():
    dogs = Dog.query.all()
    return jsonify([{
        "id": dog.id,
        "name": dog.name,
        "type": dog.type,
        "number_available": dog.number_available
    } for dog in dogs]), 200

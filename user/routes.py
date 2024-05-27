from flask import Blueprint, request, jsonify
from models import db, Dog

user_bp = Blueprint('user', __name__)

@user_bp.route('/view_categories', methods=['GET'])
def view_categories():
    dog_types = db.session.query(Dog.type).distinct().all()
    return jsonify({"categories": [type_[0] for type_ in dog_types]}), 200

@user_bp.route('/buy_dogs', methods=['POST'])
def buy_dogs():
    data = request.get_json()
    dog_name = data.get('name')
    number = data.get('number')

    if not dog_name or not number:
        return jsonify({"error": "Dog name and number are required"}), 400

    if number > 2:
        return jsonify({"error": "Cannot buy more than 2 dogs"}), 400

    dog = Dog.query.filter_by(name=dog_name, is_available=True).first()
    if not dog or dog.number_available < number:
        return jsonify({"error": "Not enough dogs available"}), 400

    dog.number_available -= number
    if dog.number_available == 0:
        dog.is_available = False

    db.session.commit()
    return jsonify({"message": "Dogs bought successfully"}), 200

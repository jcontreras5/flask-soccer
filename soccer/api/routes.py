import re
from flask import Blueprint, request, jsonify
from soccer.helpers import token_required
from soccer.models import User, Player, player_schema,player_schemas, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 73}

#CREATE player ENDPOINT
@api.route('/players', methods = ['POST'])
@token_required
def create_player(current_user_token): #coming from token_required decorator
    name = request.json['name']
    age = request.json['age']
    price = request.json['price']
    position = request.json['position']
    height = request.json['height']
    weight = request.json['weight']
    club = request.json['club']
    user_token = current_user_token.token

    player = Player(name,age,price,position,height,weight,club,user_token=user_token)

    db.session.add(player)
    db.session.commit()

    response = player_schema.dump(player)
    return jsonify(response)

# RETRIEVE ALL playerS
@api.route('/players', methods = ['GET'])
@token_required
def get_players(current_user_token):
    owner = current_user_token.token
    players = Player.query.filter_by(user_token = owner).all()
    response = player_schemas.dump(players)
    return jsonify(response)

# RETRIEVE ONE player ENDPOINT
@api.route('/players/<id>', methods = ['GET'])
@token_required
def get_player(current_user_token, id):
    player = Player.query.get(id)
    response = player_schema.dump(player)
    return jsonify(response)

#UPDATE player BY ID
@api.route('/players/<id>', methods = ['POST', 'PUT'])
@token_required
def update_player(current_user_token, id):
    player = Player.query.get(id)
    print(player)
    player.name = request.json['name']
    player.age = request.json['age']
    player.price = request.json['price']
    player.position = request.json['position']
    player.height = request.json['height']
    player.weight = request.json['weight']
    player.club = request.json['club']
    player.user_token = current_user_token.token
    print(player.name)
    db.session.commit()
    response = player_schema.dump(player)
    return jsonify(response)

# DELETE player BY ID
@api.route('/players/<id>', methods = ['DELETE'])
@token_required
def delete_player(current_user_token, id):
    player = Player.query.get(id)
    if player:
        db.session.delete(player)
        db.session.commit()
        
        response = player_schema.dump(player)
        return jsonify(response)
    else:
        return jsonify({'Error':'This player does not exist'})
from flask import Blueprint, jsonify, request, abort
from .models import Client, Parking, ClientParking, db
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify(([{'id': c.id, 'name': c.name, 'surname': c.surname} for c in clients]))

@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({'id': client.id, 'name': client.name, 'surname': client.surname, 'credit_card': client.credit_card, 'car_number': client.car_number})

@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'id': client.id}), 201

@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.json
    parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=data['count_places'],
        count_available_places=data['count_places']
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify({'id': parking.id}), 201

@bp.route('/client_parkings', methods=['POST'])
def enter_parking():
    data = request.json
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    if not parking.opened or parking.count_available_places < 1:
        return abort(400, 'Parking unavailable')

    cp = ClientParking.query.filter_by(client_id=client.id, parking_id=parking.id).first()
    if cp and cp.time_out is None:
        return abort(400, 'Client already parked here')

    if cp is None:
        cp = ClientParking(client_id=client.id, parking_id=parking.id)
    cp.time_in = datetime.now()
    cp.time_out = None

    parking.count_available_places -= 1
    db.session.add(cp)
    db.session.commit()
    return jsonify({'message': 'Entered parking'}), 201

@bp.route('/client_parkings', methods=['DELETE'])
def exit_parking():
    data = request.json
    client = Client.query.get_or_404(data['client_id'])
    parking = Parking.query.get_or_404(data['parking_id'])

    cp = ClientParking.query.filter_by(client_id=client.id, parking_id=parking.id, time_out=None).first()
    if cp is None:
        return abort(400, 'Client not parked currently')

    if not client.credit_card:
        return abort(400, 'No credit card on file')

    cp.time_out = datetime.now()
    if cp.time_out < cp.time_in:
        return abort(400, 'Invalid time_out earlier than time_in')

    parking.count_available_places += 1
    db.session.commit()
    return jsonify({'message': 'Exited parking and paid'}), 200

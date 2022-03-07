import json

from flask import Blueprint, Flask, request, jsonify, session

import queries.insert_queries as insert_queries
import queries.select_queries as select_queries
import queries.update_queries as update_queries
import queries.delete_queries as delete_queries

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api/players')
def send_players():
    players = select_queries.get_players()
    return jsonify(players)


@api.route('/api/users/logged-in')
def send_logged_in_user():
    uid = session['UID']
    logged_in_user = select_queries.get_logged_in_user(uid)
    return jsonify(logged_in_user)


@api.route('/api/images/league-cards')
def send_league_images():
    league_images = select_queries.get_images('leagues')
    return jsonify(league_images)


@api.route('/api/leagues', methods=['POST'])
def create_league():
    data = json.loads(request.data)
    league_id = insert_queries.add_new_league(data)
    new_league_id = {'league_id': league_id}
    return jsonify(new_league_id)

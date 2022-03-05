from psycopg2.sql import SQL, Literal, Identifier

from data_manager import execute_select


def get_milestones():
    query = """
    SELECT 
        milestone_name 
    FROM 
        milestones
    ORDER BY
        milestones.milestone_name;
    """
    return execute_select(SQL(query))


def get_user_id(token):
    query = """
    SELECT id
    FROM players
    WHERE username LIKE {token} OR email LIKE {token}
    """
    return execute_select(SQL(query).format(
        token=Literal(token)
    ), fetchall=False)


def get_players():
    query = """
    SELECT 
        players.id AS id,
        players.username AS username,
        players.first_name || ' ' || players.last_name AS name,
        images.source AS image_source
    FROM 
        players
    LEFT JOIN images ON players.image_id = images.id
    """
    return execute_select(SQL(query))


def get_round_by_id(round_id):
    query = """
    SELECT 
        league_id, started, finished, sequence
    FROM 
        rounds
    WHERE id = {round_id};
    """
    return execute_select(SQL(query).format(round_id=Literal(round_id)), fetchall=False)


def get_boards():
    query = """
    SELECT
        *
    FROM 
        boards
    ORDER BY 
        boards.board_name;
    """
    return execute_select(SQL(query))


def get_expansions():
    query = """
    SELECT
        *
    FROM 
        expansions
    ORDER BY 
        expansions.expansion_name;
    """
    return execute_select(SQL(query))


def get_corporations():
    query = """
    SELECT
        *
    FROM 
        corporations
    ORDER BY 
        corporations.name;
    """
    return execute_select(SQL(query))


def get_round_points(round_id):
    query = """
    SELECT 
        players.username                    AS  "Player",
        corporations.name                   AS  "Corporation",
        points.tr_number                    AS  "TR",
        points.milestones_points            AS  "Milestone Points",
        points.award_points                 AS  "Award Points",
        points.number_of_own_greeneries     AS  "Greens",
        points.number_of_cities             AS  "Cities",
        points.greeneries_around_cities     AS  "Greens around Cities",
        points.vp_on_cards                  AS  "Win Points",
        points.sum_points                   AS  "Total"
        
    FROM
        points
    LEFT JOIN players           ON  points.player_id = players.id
    LEFT JOIN round_players     ON  players.id = round_players.player_id
    LEFT JOIN corporations      ON  round_players.corporation_id = corporations.id
    WHERE
        points.round_id = {round_id}
        AND round_players.round_id = {round_id}
    ORDER BY
        points.sum_points DESC
    """
    return execute_select(SQL(query).format(round_id=Literal(round_id)))


def get_round_players(league_id):
    query = """
    SELECT
        players.id                                      AS  id,
        players.username                                AS  username
    FROM players
    LEFT JOIN league_players ON players.id = league_players.player_id
    WHERE
        league_players.league_id = {league_id}
    ORDER BY 
        players.username;
    """
    return execute_select(SQL(query).format(league_id=Literal(league_id)))


def get_players_in_round(round_id):
    query = """
    SELECT 
        round_players.player_id     AS  player_id,
        players.username            AS  username,
        corporations.name           AS  corporation_name,
        images.source               AS  corporation_image_source
    FROM
        round_players
    LEFT JOIN corporations  ON  round_players.corporation_id =  corporations.id
    LEFT JOIN players       ON  round_players.player_id      =  players.id
    LEFT JOIN images        ON  corporations.image_id        =  images.id
    WHERE
        round_players.round_id = {round_id};
    """
    return execute_select(SQL(query).format(round_id=Literal(round_id)))


def get_images(type):
    image_type = ''
    if type == 'leagues':
        image_type = 'league_card'
    query = """
    SELECT 
        images.id as id,
        images.source as image_source 
    FROM 
        images
    WHERE images.{image_type} IS TRUE;
    """
    return execute_select(SQL(query).format(image_type=Identifier(image_type)))


def get_logged_in_user(user_id):
    query = """
    SELECT 
        players.id AS id,
        players.username AS username,
        players.first_name || ' ' || players.last_name AS name,
        images.source AS image_source
    FROM 
        players
    LEFT JOIN images ON players.image_id = images.id
    WHERE players.id = {user_id} 
    """
    return execute_select(SQL(query).format(user_id=Literal(user_id)), fetchall=False)


def get_logged_in_user_leagues(user_id):
    query = """
    SELECT
            leagues.id                                                          AS  id,
            leagues.league_name                                                 AS  league_name,
            leagues.league_admin                                                AS  league_admin,
            leagues.round_number                                                AS  round_number,
            COUNT(DISTINCT league_players.player_id)                            AS  player_number,
            COUNT(DISTINCT rounds.id) FILTER ( WHERE rounds.finished IS TRUE )  AS  finished_rounds,
            images.source                                                       AS  league_image_source
    
        FROM
            leagues
        LEFT JOIN league_players ON leagues.id = league_players.league_id
        LEFT JOIN images ON leagues.image_id = images.id
        LEFT JOIN rounds ON leagues.id = rounds.league_id
        WHERE
            leagues.league_admin = {user_id}
        OR
            league_players.player_id = {user_id}
        GROUP BY
            leagues.id, images.source
        ORDER BY
            leagues.id DESC;
    """
    return execute_select(SQL(query).format(user_id=Literal(user_id)))


def get_password(token):
    query = """
    SELECT id, password
    FROM players
    WHERE username LIKE {token} OR email LIKE {token}
    """
    return execute_select(SQL(query).format(
        token=Literal(token)
    ), fetchall=False)


def get_user_email(user_id):
    query = """
    SELECT email
    FROM players
    WHERE id = {user_id}
    """
    return execute_select(SQL(query).format(
        user_id=Literal(user_id)
    ), fetchall=False)


def get_pictures():
    query = """
    SELECT id, source
    FROM images
    WHERE user_image IS TRUE
    """
    return execute_select(SQL(query))


def get_user_data(uid):
    query = """
    SELECT username, first_name, last_name, email, source 
    FROM players
    JOIN images
        ON players.image_id = images.id::varchar
    WHERE players.id = {uid}
    """
    return dict(execute_select(SQL(query).format(
        uid=Literal(uid)
    ), fetchall=False))

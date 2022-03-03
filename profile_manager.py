import bcrypt
import re
from queries import insert_queries
from queries import select_queries


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def update_password_on_form(form, password):
    """Replaces the unhashed password with hashed one
    in dictionary"""
    form = dict(form)
    form['password'] = password
    return form


def validate_registration(form):
    """If every input matches the requirements
    returns an empty error message"""
    nickname, email, email2, pwd, pwd2 = unpack_registration_form_for_validation(form)
    if is_unique_data_exist(nickname):
        return 'nickname already exist'
    if is_unique_data_exist(email):
        return 'email already registered'
    if email != email2:
        return 'email not matching'
    if pwd != pwd2:
        return 'password not matching'
    if is_password_format_correct(pwd) is None:
        return 'your password must contains minimum 8 characters, at least one letter and one number and one big letter'
    return ''


def validate_login(form):
    """If every input matches the requirements
    returns True"""
    pass


def submit_registration(form):
    """This submits !valid! data to database
    If process successful returns user id"""
    hashed_pwd = hash_password(form['password'])
    data = update_password_on_form(form, hashed_pwd)
    insert_queries.insert_new_user(data)
    user_id = select_queries.get_user_id(form['nickname'])
    return 99 # user_id


def is_password_format_correct(password):
    """If password formatted like, 'format_template'
    returns True"""
    return re.match("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password)

def is_registration_major_data_equal(str1, str2):
    """If data field one and data field two
    the same string, returns True"""
    return bool

def is_unique_data_exist(unique_value):
    """If unique already exist in database
    returns True"""
    return False # bool(select_queries.is_unique_data_exist(unique_value))


def unpack_registration_form_for_validation(data):
    """Unpacks registration from coming from html
    returns username, email, password, pp_id = (profile_picture_id)"""
    data = dict(data)
    return data['nickname'], data['email'], data['email2'], data['password'], data['password2']


def unpack_login_form(form):
    """Unpacks login form coming from html
    returns login_token, password"""
    return [login_token, password]

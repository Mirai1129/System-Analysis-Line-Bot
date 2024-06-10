from flask import render_template, Blueprint, request, session, redirect, flash

from database import MongoAdapter

members_blueprint = Blueprint('members', __name__, template_folder='templates', static_folder='static')
db = MongoAdapter()


@members_blueprint.route('/main')
def index():
    if 'user' not in session:
        return redirect('/members/login')

    patient_id = session['user']['patient_id']
    profile_data = db.get_profile_by_patient_id(patient_id)
    status_data = db.get_status_by_patient_id(patient_id)
    exercise_data = db.get_exercise_by_patient_id(patient_id)
    observe_list_data = db.get_observe_list_by_patient_id(patient_id)
    body_health_data = db.get_body_health_by_patient_id(patient_id)

    if profile_data is None:
        flash('Profile not found')
        return redirect('/members/login')

    return render_template('main.html',
                           profile=profile_data,
                           status=status_data,
                           exercise=exercise_data,
                           observe_list=observe_list_data,
                           body_health=body_health_data)


@members_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/members/main')

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        print(user_id, password)

        if db.is_user_correct(user_id, password):
            session['user'] = {
                'patient_id': user_id,
            }
            return redirect('/members/main')
        else:
            flash('Invalid user id, or password')
            return redirect('/members/login')

    return render_template('login.html')


@members_blueprint.route('/checkLogin', methods=['POST'])
def checkLogin():
    if 'user' in session:
        return redirect('/members/main')

    user_id = request.form['user_id']
    password = request.form['password']

    if db.is_user_correct(user_id, password):
        session['user'] = {
            'patient_id': user_id,
        }
        return redirect('/members/main')
    else:
        flash('Invalid user id, or password')
        return redirect('/members/login')


@members_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/members/login')

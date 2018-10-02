from flask import Flask, jsonify, abort, request, make_response, current_app
from functools import update_wrapper
from flask_cors import CORS
import mysql.connector as mariadb
from datetime import datetime, timedelta
from threading import Thread
import traceback
import json
import re

# Attributes
mon_thu_times = [
    '10-11',
    '11-12',
    '12-01',
    '01-02',
    '02-03',
    '03-04',
    '04-05',
    '05-06',
    '06-07',
    '07-08',
    '08-09'
]
fri_times = [
    '10-11',
    '11-12',
    '12-01',
    '01-02',
    '02-03',
    '03-04',
    '04-05'
]
sun_times = [
    '02-03',
    '03-04',
    '04-05',
    '05-06'
]
days = [
    'sun',
    'mon',
    'tue',
    'wed',
    'thu',
    'fri'
]
days_w_num = {
    0: 'mon',
    1: 'tue',
    2: 'wed',
    3: 'thu',
    4: 'fri',
    6: 'sun'
}
schedule_ids = []
for day in days:
    if day != 'fri' and day != 'sun':
        for time in mon_thu_times:
            schedule_ids.append('{}_{}'.format(day, time))
    elif day == 'fri':
        for time in fri_times:
            schedule_ids.append('{}_{}'.format(day, time))
    elif day == 'sun':
        for time in sun_times:
            schedule_ids.append('{}_{}'.format(day, time))

# Connect to DB
con = mariadb.connect(
    host='localhost',
    database='tutor_schedule',
    user='<REMOVED>',
    password='<REMOVED>'
)
cur = con.cursor(buffered=True)
cur2 = con.cursor(buffered=True)

# Functions
def get_tutor_shift_time():
    dt_now = datetime.now()

    # Get day
    day = ''
    if 0<= dt_now.weekday() <= 4 or dt_now.weekday() == 6:
        day = days_w_num[dt_now.weekday()]
    else:
        return 'CLOSED'
    
    # Get hour & return
    cur_hour = datetime.now().hour
    if cur_hour is 10:
        return '{}_10-11'.format(day)
    elif cur_hour is 11:
        return '{}_11-12'.format(day)
    elif cur_hour is 12:
        return '{}_12-01'.format(day)
    elif cur_hour is 13:
        return '{}_01-02'.format(day)
    elif cur_hour is 14:
        return '{}_02-03'.format(day)
    elif cur_hour is 15:
        return '{}_03-04'.format(day)
    elif cur_hour is 16:
        return '{}_04-05'.format(day)
    elif cur_hour is 17:
        return '{}_05-06'.format(day)
    elif cur_hour is 18:
        return '{}_06-07'.format(day)
    elif cur_hour is 19:
        return '{}_07-08'.format(day)
    elif cur_hour is 20:
        return '{}_08-09'.format(day)
    else:
        return 'CLOSED'

def is_lab_open():
    time = datetime.now()
    if 0 <= time.weekday() <= 3: # Monday to Thursday
        if 10 <= time.hour <= 20: # 10 - 9pm
            return True
    elif time.weekday() == 4: # Friday
        if 10 <= time.hour <= 17: # 10 - 5pm
            return True
    elif time.weekday() == 6: # Sunday
        if 14 <= time.hour <= 17: # 2 - 6pm
            return True
    else:
        return False

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# Flask
external_app = Flask(__name__)
#CORS(external_app, resources={r"/*": {"origins": "*"}})
internal_app = Flask(__name__)
#CORS(internal_app)

@external_app.route('/weekly_schedule', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def weekly_schedule():
    data = {
        'status': 'success',
        'data': {}
    }

    try:
        cur.execute('''SELECT
                            day_time,
                            tutor_1,
                            tutor_2
                       FROM week_schedule;''')
        for row in cur.fetchall():
            num_tutors = 0
            if row[1]:
                num_tutors = 1
                cur2.execute('SELECT color FROM tutors WHERE full_name = %s;', (row[1], ))
                db_data = cur2.fetchone()
                tutor_1_name = row[1]
                tutor_1_color = db_data[0]
            else:
                tutor_1_name = ''
                tutor_1_color = 'blank'
            if row[2]:
                num_tutors = 2
                cur2.execute('SELECT color FROM tutors WHERE full_name = %s;', (row[2], ))
                db_data = cur2.fetchone()
                tutor_2_name = row[2]
                tutor_2_color = db_data[0]
            else:
                tutor_2_name = ''
                tutor_2_color = 'blank'
            
            data['data'][row[0]] = {
                'num_tutors': num_tutors,
                'tutor_1': {
                    'name': tutor_1_name,
                    'color': tutor_1_color
                },
                'tutor_2': {
                    'name': tutor_2_name,
                    'color': tutor_2_color
                }
            }
    except:
        return jsonify({
            'status': 'error',
            'reason': 'Unable to access data from db!'
        })
    
    return jsonify(data)

@external_app.route('/lab_open', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def lab_open():
    return jsonify({
        'status': 'success',
        'data': {
            'open': is_lab_open()
        }
    })

@external_app.route('/get_current_tutors', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_current_tutors():
    tutor_shift_time = get_tutor_shift_time()
    if tutor_shift_time != 'CLOSED':
        try:
            data = {
                'status': 'success',
                'data': {
                    'open': True,
                    'tutor_1': {
                        'name': 'NONE',
                        'color': '',
                        'major': '',
                        'email': '',
                        'position': '',
                        'skills': []
                    },
                    'tutor_2': {
                        'name': 'NONE',
                        'color': '',
                        'major': '',
                        'email': '',
                        'position': '',
                        'skills': []
                    }
                }
            }

            cur.execute('SELECT tutor_1, tutor_2 FROM week_schedule WHERE day_time = %s;', (tutor_shift_time, ))
            db_data = cur.fetchone()
            if db_data[0]:
                cur2.execute('SELECT color, major, email, position FROM tutors WHERE full_name = %s;', (db_data[0], ))
                db_data2 = cur2.fetchone()
                data['data']['tutor_1']['name'] = db_data[0].replace('_', ' ')
                data['data']['tutor_1']['color'] = db_data2[0]
                data['data']['tutor_1']['major'] = db_data2[1]
                data['data']['tutor_1']['email'] = db_data2[2]
                data['data']['tutor_1']['position'] = db_data2[3]
                cur2.execute('SELECT skill FROM tutor_skills WHERE full_name = %s;', (db_data[0], ))
                skills = []
                for row in cur2.fetchall():
                    skills.append(row[0])
                data['data']['tutor_1']['skills'] = skills
            if db_data[1]:
                cur2.execute('SELECT color, major, email, position FROM tutors WHERE full_name = %s;', (db_data[1], ))
                db_data2 = cur2.fetchone()
                data['data']['tutor_2']['name'] = db_data[1].replace('_', ' ')
                data['data']['tutor_2']['color'] = db_data2[0]
                data['data']['tutor_2']['major'] = db_data2[1]
                data['data']['tutor_2']['email'] = db_data2[2]
                data['data']['tutor_2']['position'] = db_data2[3]
                cur2.execute('SELECT skill FROM tutor_skills WHERE full_name = %s;', (db_data[1], ))
                skills = []
                for row in cur2.fetchall():
                    skills.append(row[0])
                data['data']['tutor_2']['skills'] = skills
            return jsonify(data)
        except:
            return jsonify({
                'status': 'error',
                'reason': 'Unable to access data from db!'
            })
    else:
        return jsonify({
            'status': 'success',
            'data': {
                'open': 'false'
            }
        })

@external_app.route('/all_skills', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def all_skills():
    try:
        data = {
            'status': 'success',
            'data': []
        }
        cur.execute('SELECT skill FROM skills;')
        skills = []
        for row in cur.fetchall():
            skills.append(row[0])
        data['data'] = skills
        
        return jsonify(data)
    except:
        print(traceback.print_exc())
        return jsonify({
            'status': 'error',
            'reason': 'Unable to retrieve data from db!'
        })

@external_app.route('/all_tutors', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def all_tutors():
    data = {
        'status': 'success',
        'data': []
    }

    try:
        cur.execute('SELECT full_name, color, major, position, email FROM tutors;')
        for row in cur.fetchall():
            skills = []
            cur2.execute('SELECT skill FROM tutor_skills WHERE full_name = %s;', (row[0], ))
            for row2 in cur2.fetchall():
                skills.append(row2[0])
            data['data'].append({
                'name': row[0],
                'color': row[1],
                'major': row[2],
                'position': row[3],
                'email': row[4],
                'skills': skills
            })
        
        return jsonify(data)
    except:
        print(traceback.print_exc())
        return jsonify({
            'status': 'error',
            'reason': 'Unable to retrieve data from db!'
        })

@external_app.route('/all_tutors_name', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def all_tutors_name():
    data = {
        'status': 'success',
        'data': []
    }

    try:
        cur.execute('SELECT full_name FROM tutors;')
        for row in cur.fetchall():
            data['data'].append(row[0])
        
        return jsonify(data)
    except:
        return jsonify({
            'status': 'error',
            'reason': 'Unable to retrieve data from db!'
        })

@external_app.route('/get_tutor/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_tutor(name):
    data = {
        'status': 'success',
        'data': {}
    }

    try:
        cur.execute('SELECT color, position, email, major FROM tutors WHERE full_name = %s;', (name, ))
        if cur.rowcount > 0:
            db_data = cur.fetchone()
            data['data']['found'] = True
            data['data']['name'] = name.replace('_', ' ')
            data['data']['color'] = db_data[0]
            data['data']['position'] = db_data[1]
            data['data']['email'] = db_data[2]
            data['data']['major'] = db_data[3]
            data['data']['skills'] = []

            cur.execute('SELECT skill FROM tutor_skills WHERE full_name = %s;', (name, ))
            skills = []
            for row in cur.fetchall():
                skills.append(row[0])
            data['data']['skills'] = skills
        else:
            data['data']['found'] = False

        return jsonify(data)
    except:
        return jsonify({
            'status': 'error',
            'reason': 'Unable to retrieve data from db!'
        })

@internal_app.route('/add_tutor')
def add_tutor():
    if request.args.get('name') and request.args.get('color') and request.args.get('position') and request.args.get('email') and request.args.get('major'):
        name = request.args.get('name')
        color = request.args.get('color')
        position = request.args.get('position')
        email = request.args.get('email')
        major = request.args.get('major')

        if re.match('^[a-zA-Z]+_[a-zA-Z]+$', name):
            skills = []
            if request.args.get('skills'):
                skills = request.args.get('skills').split(',')

            try:
                cur.execute('INSERT INTO tutors VALUES (%s, %s, %s, %s, %s);', (name, color, position, email, major))
                con.commit()
                if cur.rowcount > 0:
                    for skill in skills:
                        cur.execute('INSERT INTO tutor_skills VALUES (%s, %s);', (name, skill))
                    con.commit()

                    return jsonify({
                        'status': 'success'
                    })
                return jsonify({
                    'status': 'error',
                    'reason': 'Unable to insert data to db!'
                })
            except:
                return jsonify({
                    'status': 'error',
                    'reason': 'Unable to insert data to db!'
                })
        else:
            return jsonify({
                'status': 'error',
                'reason': 'Invalid format! Please put down proper information!'
            })
    else:
        return jsonify({
            'status': 'error',
            'reason': 'Information missing! Need the following: name, color, position, email and major. Skills is optional.'
        })

@internal_app.route('/remove_tutor')
def remove_tutor():
    if request.args.get('name'):
        name = request.args.get('name')

        if re.match('^[a-zA-Z]+_[a-zA-Z]+$', name):
            try:
                cur.execute('DELETE FROM tutors WHERE full_name = %s;', (name, ))
                con.commit()
                if cur.rowcount > 0:
                    cur.execute('DELETE FROM tutor_skills WHERE full_name = %s;', (name, ))
                    con.commit()
                    return jsonify({
                        'status': 'success'
                    })
                return jsonify({
                    'status': 'error',
                    'reason': 'Tutor {} doesn\'t exist!'.format(name)
                })
            except:
                return jsonify({
                    'status': 'error',
                    'reason': 'Unable to access data from db!'
                })
        else:
            return jsonify({
                'status': 'error',
                'reason': 'Invalid input! Must use FIRSTNAME_LASTNAME format.'
            })
    else:
        return jsonify({
            'status': 'error',
            'reason': 'name variable is needed!'
        })

@internal_app.route('/modify_tutor')
def modify_tutor():
    if request.args.get('name') and request.args.get('color') and request.args.get('position') and request.args.get('email') and request.args.get('major'):
        name = request.args.get('name')
        color = request.args.get('color')
        position = request.args.get('position')
        email = request.args.get('email')
        major = request.args.get('major')

        if re.match('^[a-zA-Z]+_[a-zA-Z]+$', name):
            skills = []
            if request.args.get('skills'):
                skills = request.args.get('skills').split(',')

            try:
                cur.execute('UPDATE tutors SET color = %s, position = %s, email = %s, major = %s WHERE full_name = %s;', (color, position, email, major, name))
                cur.execute('DELETE FROM tutor_skills WHERE full_name = %s;', (name, ))
                for skill in skills:
                    cur.execute('INSERT INTO tutor_skills VALUES (%s, %s);', (name, skill))
                con.commit()

                return jsonify({
                    'status': 'success'
                })
            except:
                return jsonify({
                    'status': 'error',
                    'reason': 'Unable to update data in db!'
                })
        else:
            return jsonify({
                'status': 'error',
                'reason': 'Invalid input! Must use FIRSTNAME_LASTNAME format.'
            })
    else:
        return jsonify({
            'status': 'error',
            'reason': 'Some information missing! Need the following: name, color, position, & skills'
        })

@internal_app.route('/add_skill')
def add_skill():
    if request.args.get('skill'):
        skill = request.args.get('skill')
        try:
            cur.execute('SELECT * FROM skills WHERE skill = %s;', (skill, ))
            if len(cur.fetchall()) > 0:
                return jsonify({
                    'status': 'error',
                    'reason': '{} already exists!'.format(skill)
                })
            
            cur.execute('INSERT INTO skills VALUES (%s);', (skill, ))
            con.commit()
            return jsonify({
                'status': 'success'
            })
        except:
            return jsonify({
                'status': 'error',
                'reason': 'Unable to insert data to db!'
            })
    else:
        return jsonify({
            'status': 'error',
            'reason': 'skill variable is needed!'
        })

@internal_app.route('/remove_skill')
def remove_skill():
    if request.args.get('skill'):
        skill = request.args.get('skill')
        try:
            cur.execute('SELECT * FROM skills WHERE skill = %s;', (skill, ))
            if len(cur.fetchall()) == 0:
                return jsonify({
                    'status': 'error',
                    'reason': '{} doesn\'t exist!'.format(skill)
                })
            
            cur.execute('DELETE FROM tutor_skills WHERE skill = %s;', (skill, ))
            con.commit()
            cur.execute('DELETE FROM skills WHERE skill = %s;', (skill, ))
            con.commit()
            return jsonify({
                'status': 'success'
            })
        except:
            return jsonify({
                'status': 'error',
                'reason': 'Unable to remove data from db!'
            })
       
    else:
        return jsonify({
            'status': 'error',
            'reason': 'skill variable is needed!'
        })

@internal_app.route('/update_week_schedule')
def update_week_schedule():
    try:
        # Run transaction
        t_cur = con.cursor()
        for schedule_id in schedule_ids:
            if schedule_id in request.args:
                str_tutors = request.args.get(schedule_id)
                tutors = str_tutors.split(',')
                if len(tutors) > 1:
                    t_cur.execute('UPDATE week_schedule SET tutor_1 = %s, tutor_2 = %s WHERE day_time = %s;', (tutors[0].replace(' ', '_'), tutors[1].replace(' ', '_'), schedule_id))
                else:
                    t_cur.execute('UPDATE week_schedule SET tutor_1 = %s, tutor_2 = NULL WHERE day_time = %s;', (tutors[0].replace(' ', '_'), schedule_id))
            else:
                t_cur.execute('UPDATE week_schedule SET tutor_1 = NULL, tutor_2 = NULL WHERE day_time = %s;', (schedule_id, ))
        con.commit()
        return jsonify({
            'status': 'success'
        })
    except:
        con.rollback()
        return jsonify({
            'status': 'error',
            'reason': 'Unable to update data to db!'
        })

# Threads
def external_app_runner():
    print('Starting external service...')
    external_app.run(host='0.0.0.0', port=9000)

def internal_app_runner():
    print('Starting internal service...')
    internal_app.run(host='0.0.0.0', port=9001)

# Main
if __name__ == '__main__':
    Thread(target=external_app_runner).start()
    Thread(target=internal_app_runner).start()
    print('Program started!')

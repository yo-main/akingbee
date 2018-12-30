# -*- coding: utf-8 -*-

import flask
import helpers
import sqlite3
import flask_session
import tempfile
import werkzeug.security
import os
import datetime
import config

#os.chdir("/var/www/akingbee.com/akb")

app = flask.Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'var/www/html/akingbee/flask_session'

app.secret_key = """iuhAqshdad123_&é"_JIHfduh3i123d!!:"""
flask_session.Session(app)

config.init()



AKB_PATH = '/akingbee'


@app.route("/", methods=['GET', 'POST'])
@helpers.login_required
def home():
    lang = flask.session['language']
    return flask.render_template("index.html", lang=lang, data=helpers.tradDb(flask.session['language']))


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    # We remove the user credentials if any in the cookie
    flask.session.pop('userId', None)
    flask.session.pop('username', None)

    # default language is French
    if 'language' not in flask.session:
        flask.session['language'] = 'fr'

    lang = flask.session['language']

    if flask.request.method == 'GET':
        return flask.render_template("login.html", lang=lang, data=helpers.tradDb(lang))
    
    elif flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        pwd = helpers.SQL("SELECT hash, id FROM users WHERE username=?", (username,))
        
        # Error while processing the SQL request
        if pwd == False:
            return flask.jsonify(helpers.getError('00001'))
        
        # The username has not been found
        if pwd == []:
            return flask.jsonify(helpers.getError('00002'))

        # Wrong password or username
        if len(pwd) != 1 or not werkzeug.security.check_password_hash(pwd[0][0], password):
            return flask.jsonify(helpers.getError('00003'))
        
        # All good ! We can log in the user
        today = datetime.date.today().isoformat()
        flag = helpers.SQL("UPDATE users SET date_last_connexion=? WHERE id=?", (today, pwd[0][1]))
        
        # Error while processing the SQL request
        if flag == False: 
            return flask.jsonify(helpers.getError('00004'))
        else:
            flask.session['userId'] = pwd[0][1]
            flask.session['username'] = username

            return flask.jsonify(helpers.getSuccess('00001'))


@app.route("/logout", methods=['GET'])
def logout():
    flask.session.pop('userId', None)
    flask.session.pop('username', None)

    return flask.redirect("/akingbee/")


@app.route("/language", methods=['POST'])
def updateLanguage():
    """Change the user language"""

    newLanguage = flask.request.form.get('language')
    flask.session['language'] = newLanguage

    return flask.jsonify({'result': 'success'})


@app.route("/register", methods=['GET'])
def register():
    lang = flask.session['language']
    return flask.render_template("register.html", lang=lang, data=helpers.tradDb(lang))


@app.route("/registercheck", methods=['POST'])
def registerCheck():
    username = flask.request.form.get('username')
    email = flask.request.form.get('email')
    pwd = flask.request.form.get('pwd')
    lang = flask.session['language']

    # Check if the username is available
    data = helpers.SQL("SELECT id FROM users WHERE username=?", (username,))

    # Error while processing the SQL request
    if data == False:
        return flask.jsonify(helpers.getError('00007'))
    
    # There is already an entry with that username
    if len(data) > 0:
        return flask.jsonify(helpers.getError('00005'))

    # Check if the email is available
    data = helpers.SQL("SELECT id FROM users WHERE email=?", (email,))

    if data == False:
        return flask.jsonify(helpers.getError('00008'))

    if len(data) > 0:
        return flask.jsonify(helpers.getError('00006'))

    # Creation of the user     
    today = datetime.date.today().isoformat()
    
    hashed_pwd = werkzeug.security.generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)
    addUser = helpers.SQL("INSERT INTO users(username, email, hash, date_creation) VALUES (?, ?, ?, ?)",
                          (username, email, hashed_pwd, today))
    
    if addUser == False:
        return flask.jsonify(helpers.getError('00009'))

    # Creation of all the different data linked to the user
    user_id = helpers.SQL("SELECT id FROM users WHERE email=?", (email,))

    if user_id == False:
        return flask.jsonify(helpers.getError('00010'))

    healthDt = (('Bonne', 'Good'), ('Moyenne', 'Medium'), ('Mauvaise', 'Bad'))
    statusBhDt = (('Active', 'Active'), ('Stock', 'Stock'))
    statusApDt = (('Actif', 'Active'), ('Inactif', 'Inactive'))
    beehouseActionDt = (('Bruler les abeilles', 'Burn the bees'),
                        ('Arroser la ruche', 'Water the beehouse'),
                        ('Trouver une nouvelle ruche', 'Find a new beehouse'),
                        ('Trouver une nouvelle reine', 'Find a new queen'))
    honeyKindDt = (('Toutes fleurs', 'All flowers'),
                   ('Acacia', 'Acacia'),
                   ('Bruyère blanche', 'Briar root'),
                   ('Chataignier', 'Chastnut'),
                   ('Tournesol', 'Sunflower'))

    for args in healthDt:
        helpers.SQL("INSERT INTO health(fr, en, user) VALUES(?,?,?)",
                    (args[0], args[1], int(user_id[0][0])))

    for args in statusBhDt:
        helpers.SQL("INSERT INTO status_beehouse(fr, en, user) VALUES(?,?,?)",
                    (args[0], args[1], int(user_id[0][0])))
    
    for args in statusApDt:
        helpers.SQL("INSERT INTO status_apiary(fr, en, user) VALUES(?,?,?)",
                    (args[0], args[1], int(user_id[0][0])))

    for args in beehouseActionDt:
        helpers.SQL("INSERT INTO beehouse_actions (fr, en, user) VALUES(?,?,?)",
                    (args[0], args[1], int(user_id[0][0])))

    for args in honeyKindDt:
        helpers.SQL("INSERT INTO honey_type (fr, en, user) VALUES(?,?,?)",
                    (args[0], args[1], int(user_id[0][0])))

    helpers.SQL("INSERT INTO owner(name, user) VALUES(?,?)",
                (username, int(user_id[0][0])))

    return flask.jsonify(helpers.getSuccess('00002'))
    

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_pwd():
    if flask.session.get('userId') is not None:
        return flask.redirect("/akingbee/")

    elif flask.request.method == 'GET':
        lang = flask.session['language']
        return flask.render_template("reset_pwd.html", lang=lang, data=helpers.tradDb(lang))

    elif flask.request.method == 'POST':
        pwd = flask.request.form.get('pwd')
        userName = flask.request.form.get('username')
        hashed_pwd = werkzeug.security.generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)

        user = helpers.SQL("SELECT id FROM users WHERE username=?", (userName,))

        if user == False: # Error while processing the SQL request
            return flask.jsonify(helpers.getError('00011'))
        elif user == []: # User does not exist
            return flask.jsonify(helpers.getError('00012'))
        else:
            helpers.SQL("UPDATE users SET hash=? WHERE username=?", (hashed_pwd, userName))
            return flask.jsonify(helpers.getSuccess('00003'))


@app.route("/apiary/index", methods=['GET'])
@helpers.login_required
def apiary():
    lang = flask.session['language']
    
    if lang not in ('fr', 'en'):
        return flask.redirect("/akingbee/")

    data = helpers.SQL(f"SELECT apiary.id, apiary.name, apiary.location, status_apiary.{lang}, honey_type.{lang}\
                         FROM apiary\
                         JOIN status_apiary ON apiary.status = status_apiary.id\
                         JOIN honey_type ON apiary.honey_type = honey_type.id\
                         WHERE apiary.user=?", 
                         (flask.session['userId'],))

    statusList = helpers.SQL(f"SELECT id, {lang} FROM status_apiary WHERE user=?", (flask.session['userId'],))
    honeyList = helpers.SQL(f"SELECT id, {lang} FROM honey_type WHERE user=?", (flask.session['userId'],))
    locationList = helpers.SQL("SELECT DISTINCT id, location FROM apiary WHERE user=?", (flask.session['userId'],))

    return flask.render_template("apiary/index.html", lang=lang, data=helpers.tradDb(lang), apia=data, al=locationList, ap=statusList, ah=honeyList)


@app.route("/apiary/create", methods=['GET', 'POST'])
@helpers.login_required
def apiary_create():
    if flask.request.method == 'GET':
        lang = flask.session['language']
       
        if lang not in ('fr', 'en'):
            return flask.redirect("/akingbee/")

        honey_type = helpers.SQL(f"SELECT id, {lang} FROM honey_type WHERE user=?", (flask.session['userId'],))
        status_apiary = helpers.SQL(f"SELECT id, {lang} FROM status_apiary WHERE user=?", (flask.session['userId'],))

        return flask.render_template("apiary/create.html", lang=lang, data=helpers.tradDb(lang), honey_type=honey_type, status_apiary=status_apiary)

    elif flask.request.method == 'POST':

        name = flask.request.form.get('apiary_name')
        location = flask.request.form.get('apiary_location')
        honey_type = flask.request.form.get('apiary_honey_type')
        status = flask.request.form.get('apiary_status')
        birthday = helpers.convertToDate(flask.request.form.get('apiary_birthday'))

        flag = helpers.SQL("INSERT INTO apiary(name, location, birthday, status, honey_type, user) VALUES(?,?,?,?,?,?)",
                            (name, location, birthday, status, honey_type, flask.session['userId']))
        
        return flask.redirect("/akingbee/apiary/index")


@app.route("/apiary/create/new_honey_type", methods=['POST'])
@helpers.login_required
def apiary_create_honey():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO honey_type(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))
   
    if flag == False:
        return flask.jsonify(helpers.getError('00013'))

    return flask.jsonify(helpers.getSuccess('00004'))


@app.route("/apiary/create/new_apiary_status", methods=['POST'])
@helpers.login_required
def apiary_status_create():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO status_apiary(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))
   
    if flag == False:
        return flask.jsonify(helpers.getError('00014'))

    return flask.jsonify(helpers.getSuccess('00005'))


@app.route("/beehouse/index", methods=['GET'])
@helpers.login_required
def beehouse():
    lang = flask.session['language']
    
    if lang not in ('fr', 'en'):
        return flask.redirect("/akingbee/")

    bh_data = helpers.SQL(f"SELECT beehouse.id, beehouse.name, apiary.name, apiary.location, status_beehouse.{lang}, health.{lang}, owner.name\
                            FROM beehouse\
                            JOIN health ON beehouse.health = health.id\
                            JOIN owner ON beehouse.owner = owner.id\
                            JOIN apiary ON beehouse.apiary = apiary.id\
                            JOIN status_beehouse ON beehouse.status = status_beehouse.id\
                            WHERE beehouse.user=?",
                            (flask.session['userId'],))

    health_filter = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?",
                                 (flask.session['userId'],))

    status_beehouse = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?",
                             (flask.session['userId'],))

    actions_beehouse = helpers.SQL(f"SELECT id, {lang} FROM beehouse_actions WHERE user=?",
                             (flask.session['userId'],))

    apiary_filter = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?",
                             (flask.session['userId'],))

    owner_filter = helpers.SQL("SELECT id, name FROM owner WHERE user=?",
                                 (flask.session['userId'],))

    return flask.render_template("beehouse/index.html", lang=lang, data=helpers.tradDb(lang),
                                 bh=bh_data, af=apiary_filter, hf=health_filter, of=owner_filter, sf=status_beehouse, ab=actions_beehouse)


@app.route("/beehouse/create", methods=['GET', 'POST'])
@helpers.login_required
def beehouse_create():
    if flask.request.method == 'GET':

        lang = flask.session['language']
        owners = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))
        apiaries = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?", (flask.session['userId'],))
        
        if lang not in ('fr', 'en'):
            return flask.redirect("/")

        health = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?", (flask.session['userId'],))
        status_beehouse = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?", (flask.session['userId'],))
        
        return flask.render_template("beehouse/create.html", lang=lang, data=helpers.tradDb(lang), owners=owners, 
                                     apiaries=apiaries, health=health, status_beehouse=status_beehouse)

    elif flask.request.method == 'POST':
        name = flask.request.form.get('name')
        birthday = helpers.convertToDate(flask.request.form.get('date'))
        status = flask.request.form.get('status')
        apiary = flask.request.form.get('apiary')
        owner = flask.request.form.get('owner')
        health = flask.request.form.get('health')
        
        flag = helpers.SQL("INSERT INTO beehouse(name, birthday, apiary, status, health, owner, user) VALUES(?,?,?,?,?,?,?)",
                           (name, birthday, apiary, status, health, owner, flask.session['userId']))

        if flag == False:
            return flask.jsonify(helpers.getError('00016'))
            
        return flask.jsonify(helpers.getSuccess('00007'))


@app.route("/beehouse/create/new_owner", methods=['POST'])
@helpers.login_required
def beehouse_create_owner():

    owner = flask.request.form.get('owner')

    flag = helpers.SQL("INSERT INTO owner(name, user) VALUES(?,?)",
                       (owner, flask.session['userId']))
    
    if flag == False:
        return flask.jsonify(helpers.getError('00015'))

    return flask.jsonify(helpers.getSuccess('00006'))


@app.route("/beehouse/create/new_health", methods=['POST'])
@helpers.login_required
def beehouse_create_health():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO health(fr, en, user) VALUES(?,?,?)",
                       (name_fr, name_en, flask.session['userId']))
    
    if flag == False:
        return flask.jsonify(helpers.getError('00017'))

    return flask.jsonify(helpers.getSuccess('00008'))


@app.route("/beehouse/create/new_beehouse_status", methods=['POST'])
@helpers.login_required
def beehouse_create_status():

    name_fr = flask.request.form.get('name_fr')
    name_en = flask.request.form.get('name_en')

    flag = helpers.SQL("INSERT INTO status_beehouse(fr, en, user) VALUES(?,?,?)",
                (name_fr, name_en, flask.session['userId']))
    
    if flag == False:
        return flask.jsonify(helpers.getError('00018'))

    return flask.jsonify(helpers.getSuccess('00009'))


@app.route("/beehouse/index/get_beehouse_info", methods=['POST'])
@helpers.login_required
def beehouse_details():
    bh_id = flask.request.form.get('bh_id')

    data = helpers.SQL("SELECT name, apiary, status, health, owner\
                        FROM beehouse\
                        WHERE id=? AND user=?",
                        (bh_id, flask.session['userId']))
    
    return flask.jsonify(data)


@app.route("/beehouse/index/submit_beehouse_info", methods=['POST'])
@helpers.login_required
def submit_beehouse_details():
    bh_id = flask.request.form.get('bh_id')
    apiary = flask.request.form.get('apiary')
    beehouse = flask.request.form.get('beehouse')
    owner = flask.request.form.get('owner')
    status = flask.request.form.get('status')
    user_id = flask.session['userId']

    flags = []

    if apiary != None:
        flags.append(helpers.SQL("UPDATE beehouse SET apiary=? WHERE id=? AND user=?", (apiary, bh_id, user_id)))
    
    if beehouse != None:
        flags.append(helpers.SQL("UPDATE beehouse SET name=? WHERE id=? AND user=?", (beehouse, bh_id, user_id)))

    if owner != None:
        flags.append(helpers.SQL("UPDATE beehouse SET owner=? WHERE id=? AND user=?", (owner, bh_id, user_id)))

    if status != None:
        flags.append(helpers.SQL("UPDATE beehouse SET status=? WHERE id=? AND user=?", (status, bh_id, user_id)))

    if False in flags:
        return flask.jsonify(helpers.getError('00019'))

    return flask.jsonify(helpers.getSuccess('00010'))


@app.route("/beehouse/index/submit_comment_modal", methods=['POST'])
@helpers.login_required
def submit_comment_modal():
    bh_id = flask.request.form.get('bh_id')
    date = helpers.convertToDate(flask.request.form.get('date'))
    comment = flask.request.form.get('comment')
    health = flask.request.form.get('health')
    cType = '1'
    
    apiaryId = helpers.SQL("SELECT apiary FROM beehouse WHERE id=? AND user=?", (bh_id, flask.session['userId']))

    if apiaryId == False:
        return flask.jsonify(helpers.getError('00020'))

    flag = helpers.SQL("INSERT INTO comments(date, comment, beehouse, apiary, health, type, user) VALUES(?,?,?,?,?,?,?)",
                (date, comment, bh_id, apiaryId[0][0], health, cType, flask.session['userId']))

    if flag == False:
        return flask.jsonify(helpers.getError('00021'))

    helpers.updateHealth(bh_id)

    return flask.jsonify(helpers.getSuccess('00011'))


@app.route("/beehouse/index/submit_action_modal", methods=['POST'])
@helpers.login_required
def submit_action_modal():
    bh_id = flask.request.form.get('bh_id')
    date = helpers.convertToDate(flask.request.form.get('date'))
    comment = flask.request.form.get('comment')
    action_type = flask.request.form.get('action_type')
    deadline = helpers.convertToDate(flask.request.form.get('deadline'))
    action_status = 1 # 1 is pending

    flag = helpers.SQL("INSERT INTO actions(beehouse, date, deadline, type, comment, status, user) VALUES(?,?,?,?,?,?,?)",
                       (bh_id, date, deadline, action_type, comment, action_status, flask.session['userId']))

    if flag == False:
        return flask.jsonify(helpers.getError('00022'))

    return flask.jsonify(helpers.getSuccess('00012'))


@app.route("/beehouse", methods=['GET'])
@helpers.login_required
def beehouse_profil():
    lang = flask.session['language']
    bh_id = flask.request.args.get('bh')

    if lang not in ('fr', 'en'):
        return flask.redirect("/")
        
    bh_data = helpers.SQL(f"SELECT beehouse.id, beehouse.name, apiary.name, apiary.location, status_beehouse.{lang}, health.{lang}, owner.name\
                          FROM beehouse\
                          JOIN health ON beehouse.health = health.id\
                          JOIN owner ON beehouse.owner = owner.id\
                          JOIN apiary ON beehouse.apiary = apiary.id\
                          JOIN status_beehouse ON beehouse.status = status_beehouse.id\
                          WHERE beehouse.user=? AND beehouse.id=?",
                          (flask.session['userId'], bh_id))

    cm_data = helpers.SQL(f"SELECT comments.id, strftime('%d/%m/%Y', comments.date), comments_type.{lang}, comments.comment, beehouse.name, apiary.name, apiary.location, coalesce(health.{lang}, '')\
                          FROM comments\
                          JOIN beehouse ON comments.beehouse = beehouse.id\
                          LEFT JOIN health ON comments.health = health.id\
                          JOIN apiary ON comments.apiary = apiary.id\
                          JOIN comments_type ON comments.type = comments_type.id\
                          WHERE comments.user=? AND comments.beehouse=?\
                          ORDER BY comments.date DESC",
                          (flask.session['userId'], bh_id))

    ac_data = helpers.SQL(f"SELECT actions.id, strftime('%d/%m/%Y', actions.date), strftime('%d/%m/%Y', actions.deadline), actions.comment, beehouse_actions.{lang}\
                          FROM actions\
                          JOIN beehouse_actions ON actions.type = beehouse_actions.id\
                          WHERE actions.user=? AND actions.beehouse=? AND actions.status=?\
                          ORDER BY actions.date ASC",
                          (flask.session['userId'], bh_id, 1))       

    health_filter = helpers.SQL(f"SELECT id, {lang} FROM health WHERE user=?",
                                (flask.session['userId'],))    

    type_filter = helpers.SQL(f"SELECT id, {lang} FROM comments_type")
    bh_status_filter = helpers.SQL(f"SELECT id, {lang} FROM status_beehouse WHERE user=?", (flask.session['userId'],))
    actions_beehouse = helpers.SQL(f"SELECT id, {lang} FROM beehouse_actions WHERE user=?", (flask.session['userId'],))
        
    apiary_filter = helpers.SQL("SELECT id, name, location FROM apiary WHERE user=?", (flask.session['userId'],))
    owner_filter = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))

    return flask.render_template("beehouse/beehouse_details.html", lang=lang, data=helpers.tradDb(lang), bh=bh_data, cm=cm_data, ac=ac_data, 
                                  tf=type_filter, af=apiary_filter, hf=health_filter, of=owner_filter, sf=bh_status_filter, ab=actions_beehouse)


@app.route("/beehouse/select", methods=['POST'])
@helpers.login_required
def select_beehouse():
    bh_id = int(flask.request.form.get('bh_id'))
    way = int(flask.request.form.get('way'))

    data = helpers.SQL("SELECT id FROM beehouse WHERE user=?", (flask.session['userId'],))
    bhs = [n[0] for n in data]
    index = bhs.index(bh_id)
    newId = 0

    if way == -1 and index == 0:
        newId = -1
    elif way == 1 and index == (len(bhs) - 1):
        newId = 0
    else:
        newId = index + way

    return flask.jsonify(f"/beehouse?bh={bhs[newId]}")


@app.route("/beehouse/index/submit_solve_action_modal", methods=['POST'])
@helpers.login_required
def solve_action():
    comment = flask.request.form.get('comment')
    action_id = flask.request.form.get('ac_id')
    action_date = helpers.convertToDate(flask.request.form.get('date'))

    bh_data = helpers.SQL("SELECT beehouse.id, beehouse.apiary\
                           FROM actions\
                           JOIN beehouse ON actions.beehouse = beehouse.id\
                           WHERE actions.id=?",
                           (action_id,))
    
    bh_id, ap_id = bh_data[0]

    flag = helpers.SQL("INSERT INTO comments(date, comment, beehouse, apiary, action, type, user) VALUES(?,?,?,?,?,?,?)",
                       (action_date, comment, bh_id, ap_id, action_id, 3, flask.session['userId']))
    if flag == False:
        return flask.jsonify(helpers.getError('00023'))

    flag = helpers.SQL("UPDATE actions SET date_done=?, status=? WHERE id=? AND user=?",
                       (action_date, 2, action_id, flask.session['userId']))
    if flag == False:
        return flask.jsonify(helpers.getError('00024'))

    return flask.jsonify(helpers.getSuccess('00013'))


@app.route("/beehouse/index/submit_edit_comment_modal", methods=['POST'])
@helpers.login_required
def edit_comment():
    comment = flask.request.form.get('comment')
    cm_id = flask.request.form.get('cm_id')
    health = flask.request.form.get('health')
    date = helpers.convertToDate(flask.request.form.get('date'))

    flag = helpers.SQL("UPDATE comments SET comment=?, health=?, date=? WHERE id=? AND user=?",
                       (comment, health, date, cm_id, flask.session['userId']))
    if flag == False:
        return flask.jsonify(helpers.getError('00025'))

    bh_id = helpers.SQL("SELECT beehouse FROM comments WHERE id=? AND user=?", (cm_id, flask.session['userId']))
    helpers.updateHealth(bh_id[0][0])

    return flask.jsonify(helpers.getSuccess('00014'))


@app.route("/beehouse/index/delete_comment", methods=['POST'])
@helpers.login_required
def del_comment():
    cm_id = flask.request.form.get('cm_id')
    bh_id, ac_id, type_com = helpers.SQL("SELECT beehouse, action, type FROM comments WHERE id=?", (cm_id,))[0]
    
    if type_com == 3:
        helpers.SQL("UPDATE actions SET status=?, date_done=? WHERE id=?", (1, None, ac_id))

    helpers.SQL("DELETE FROM comments WHERE id=? AND user=?", (cm_id, flask.session['userId']))
    helpers.updateHealth(bh_id)

    return flask.jsonify(helpers.getSuccess('00015'))


@app.route("/setup", methods=['GET'])
@helpers.login_required
def setupPage():
    if flask.request.method == 'GET':
        lang = flask.session['language']
        return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), t=0, col="")


@app.route("/setup/update", methods = ['POST'])
@helpers.login_required
def submit_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    dataId = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("UPDATE status_beehouse SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("UPDATE owner SET name=? WHERE id=? AND user=?", (fr, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("UPDATE health SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("UPDATE honey_type SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("UPDATE beehouse_actions SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("UPDATE status_apiary SET fr=?, en=? WHERE id=? AND user=?", (fr, en, dataId, flask.session['userId']))

    if flag == False:
        flask.jsonify(helpers.getError('00026'))
        
    return flask.jsonify(helpers.getSuccess('00016'))


@app.route("/setup/delete", methods=['POST'])
@helpers.login_required
def delete_data():
    dataId = flask.request.form.get('dataId')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("DELETE FROM status_beehouse WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("DELETE FROM owner WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("DELETE FROM health WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("DELETE FROM honey_type WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("DELETE FROM beehouse_actions WHERE id=? AND user=?", (dataId, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("DELETE FROM status_apiary WHERE id=? AND user=?", (dataId, flask.session['userId']))

    if flag == False:
        flask.jsonify(helpers.getError('00027'))
        
    return flask.jsonify(helpers.getSuccess('00017'))


@app.route("/setup/submit", methods = ['POST'])
@helpers.login_required
def submit_new_data():
    fr = flask.request.form.get('fr')
    en = flask.request.form.get('en')
    source = flask.request.form.get('source')

    if source == "/setup/beehouse/status":
        flag = helpers.SQL("INSERT INTO status_beehouse(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/owner":
        flag = helpers.SQL("INSERT INTO owner(name, user) VALUES(?,?)", (fr, flask.session['userId']))
    elif source == "/setup/beehouse/health":
        flag = helpers.SQL("INSERT INTO health(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/honey":
        flag = helpers.SQL("INSERT INTO honey_type(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/beehouse/actions":
        flag = helpers.SQL("INSERT INTO beehouse_actions(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))
    elif source == "/setup/apiary/status":
        flag = helpers.SQL("INSERT INTO status_apiary(fr, en, user) VALUES(?,?,?)", (fr, en, flask.session['userId']))

    if flag == False:
        flask.jsonify(helpers.getError('00028'))
        
    return flask.jsonify(helpers.getSuccess('00018'))


@app.route("/setup/beehouse/status", methods=['GET', 'POST'])
@helpers.login_required
def setupStatusBh():
    if flask.request.method == 'GET':
        lang = flask.session['language']
        menu = 0
        id_title = 'status_beehouse'

        tData = helpers.SQL("SELECT id, fr, en FROM status_beehouse WHERE user=?", (flask.session['userId'],))
        
        if lang == 'fr':
            title = "Status des ruches"
            desc = "Les différents status qui peut être affecté à une ruche"
        else:
            title = "Beehouse status"
            desc = "The different status that can be given to a beehouse"
            
        return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@app.route("/setup/beehouse/owner", methods=['GET'])
@helpers.login_required
def setupOwner():
    lang = flask.session['language']
    menu = 1
    id_title = 'owner'

    tData = helpers.SQL("SELECT id, name FROM owner WHERE user=?", (flask.session['userId'],))
    
    if lang == 'fr':
        col = ("Nom",)
        title = "Apiculteur"
        desc = "L'apiculteur d'une ruche (juste au cas où vous gérez les ruches d'une autre personne)"
    else:
        col = ("Name",)
        title = "Beekeper"
        desc = "The beekeper of a beehouse (in case you manage beehouse on behalf of other people ?)"

    return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=col, m=menu, t=title, i=id_title, d=desc)


@app.route("/setup/beehouse/health", methods=['GET'])
@helpers.login_required
def setupHealth():
    lang = flask.session['language']
    menu = 2
    id_title = 'health'

    tData = helpers.SQL("SELECT id, fr, en FROM health WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Status de santé"
        desc = "Les différents status de santés que vous souhaitez affecter à une ruche"
    else:
        title = "Health status"
        desc = "Different health status that you wish to affect to a beehouse"

    return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@app.route("/setup/beehouse/honey", methods=['GET'])
@helpers.login_required
def setupHoneyKind():
    lang = flask.session['language']
    menu = 3
    id_title = 'honey_type'

    tData = helpers.SQL("SELECT id, fr, en FROM honey_type WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Type de miel"
        desc = "Les différents types de miel que vous pouvez être amené à récolter"
    else:
        title = "Honey type"
        desc = "The different kind of honey that you are harvesting"

    return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@app.route("/setup/beehouse/actions", methods=['GET'])
@helpers.login_required
def setupBh_actions():
    lang = flask.session['language']
    menu = 4
    id_title = 'beehouse_actions'

    tData = helpers.SQL("SELECT id, fr, en FROM beehouse_actions WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Actions relatives aux ruches"
        desc = "Les différentes actions que vous pouvez être amené à faire sur une ruche"
    else:
        title = "Beehouse actions"
        desc = "The différent actions that you may have to do on a beehouse"

    return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@app.route("/setup/apiary/status", methods=['GET'])
@helpers.login_required
def setupStatusAp():
    lang = flask.session['language']
    menu = 5
    id_title = 'status_apiary'

    tData = helpers.SQL("SELECT id, fr, en FROM status_apiary WHERE user=?", (flask.session['userId'],))

    if lang == 'fr':
        title = "Status des ruchers"
        desc = "Les différents status que vous pouvez donner à un rucher"
    else:
        title = "Apiary status"
        desc = "The different status that you may have to give to an apiary"

    return flask.render_template("setup/setup.html", lang=lang, data=helpers.tradDb(lang), tData=tData, col=('fr', 'en'), m=menu, t=title, i=id_title, d=desc)


@app.route("/apiary/index/get_apiary_info", methods=['POST'])
@helpers.login_required
def apiary_details():
    ap_id = flask.request.form.get('ap_id')

    data = helpers.SQL("SELECT name, location, status, honey_type\
                        FROM apiary\
                        WHERE id=? AND user=?",
                        (ap_id, flask.session['userId']))
    
    return flask.jsonify(data)


@app.route("/apiary/index/submit_apiary_info", methods=['POST'])
@helpers.login_required
def submit_apiary_details():
    ap_id = flask.request.form.get('ap_id')

    name = flask.request.form.get('name')
    location = flask.request.form.get('location')
    status = flask.request.form.get('status')
    honey = flask.request.form.get('honey')

    user_id = flask.session['userId']

    flags = []

    if name != None:
        flags.append(helpers.SQL("UPDATE apiary SET name=? WHERE id=? AND user=?", (name, ap_id, user_id)))
    
    if location != None:
        flags.append(helpers.SQL("UPDATE apiary SET location=? WHERE id=? AND user=?", (location, ap_id, user_id)))

    if status != None:
        flags.append(helpers.SQL("UPDATE apiary SET status=? WHERE id=? AND user=?", (status, ap_id, user_id)))

    if honey != None:
        flags.append(helpers.SQL("UPDATE apiary SET honey=? WHERE id=? AND user=?", (honey, ap_id, user_id)))

    if False in flags:
        flask.jsonify(helpers.getError('00029'))
        
    return flask.jsonify(helpers.getSuccess('00019'))


@app.route("/apiary/delete", methods=['POST'])
@helpers.login_required
def del_apiary():
    ap_id = flask.request.form.get('ap_id')
    check = helpers.SQL("DELETE FROM apiary WHERE id=? AND user=?", (ap_id, flask.session['userId']))

    if check == False:
        flask.jsonify(helpers.getError('00030'))
        
    return flask.jsonify(helpers.getSuccess('00020'))


if __name__ == "__main__":
    app.run()

from flask_bcrypt import Bcrypt
from flask import Flask, Response
from model import *
from flask import jsonify
import json
from flask import make_response
from flask import request
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
bcrypt = Bcrypt(app)

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)



# ----------------------------------- user ------------------

@app.route('/user', methods=['POST'])
def create_user():
    print("create_user")
    user = users(
        username = request.json.get('username'),
        firstName = request.json.get('firstName'),
        lastName = request.json.get('lastName'),
        email = request.json.get('email'),
        password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8'),
        phone = request.json.get('email'),
        userType = request.json.get('userType')
    )
    check = (Session.query(users).filter_by(username=user.username).all())
    if check != []:
        return make_response(jsonify({'error': 'User with such username already exists'}), 409)
    try:
        Session.add(user)
        Session.commit()
    except IntegrityError:
        print('incorrect data')
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    a = to_json(user, users)
    return Response(response=a,
                status=200,
                mimetype="application/json")


@app.route("/user/<int:id>", methods=['GET'])
def get_user_info(id):
    try:
        a = to_json(Session.query(users).filter_by(id=id).one(), users)
        return Response(response=a,
                    status=200,
                    mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    print("update_user")
    z = Session.query(users).filter_by(id=id).all()
    if not z:
        return make_response(jsonify({'error': 'Not found'}), 404)

    u = Session.query(users).filter_by(id=id).one()
    if request.json.get('username'):
        tvins = (Session.query(users).filter_by(username=request.json.get('username')).all())
        if tvins != []:
            return make_response(jsonify({'error': 'username is busy'}), 409)
        u.username = request.json.get('username')
    if request.json.get('firstName'):
        u.firstName = request.json.get('firstName')
    if request.json.get('lastName'):
        u.lastName = request.json.get('lastName')
    if request.json.get('password'):
        u.password = request.json.get('password')
    if request.json.get('phone'):
        u.password = request.json.get('phone')
    if request.json.get('userType'):
        u.password = request.json.get('userType')
    Session.commit()
    Session.commit()

    return Response(response=to_json(u, users),
                    status=200,
                    mimetype="application/json")

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Session.query(users).filter_by(id=id).first()
        Session.delete(user)
        Session.commit()
        return {
            "msg": "user deleted successfully",
            "id": id
        }
    except:
        return "user not found", 404

# ------------------------------ course -------------------------

@app.route('/course', methods=['POST'])
def create_course():
    print("create_course")
    c = course(
        id = request.json.get('id'),
        courseName = request.json.get('courseName'),
        courseDescription = request.json.get('courseDescription'),
    )
    tvins = (Session.query(course).filter_by(id=c.id).all())
    if tvins != []:
        return make_response(jsonify({'error': 'course with such id already exists'}), 409)
    try:
        Session.add(c)
        Session.commit()
    except IntegrityError:
        print('incorrect data')
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    # tasks.append(task)
    a = to_json(c, course)
    return Response(response=a,
                status=200,
                mimetype="application/json")



@app.route("/course/getAll/<int:id>", methods=['GET'])
def all_courses_for_user(id):
    z = Session.query(users).filter_by(id=id).all()
    if not z:
        return make_response(jsonify({'error': 'Not found'}), 404)

    a = Session.query(requestClass).filter_by(requestFrom=id).all()
    b = []
    for i in a:
        b.append(Session.query(course).filter_by(id=i.requestToCourse).one())

    json_data = []
    for i in b:
        json_data.append(to_json(i, course))
    try:
        Session.commit()
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return Response(response=str(json_data),
                    status=200,
                    mimetype="application/json")

@app.route("/course/get/<int:id>", methods=['GET'])
def get_course_ById(id):
    try:
        a = to_json(Session.query(course).filter_by(id=id).one(), course)
        return Response(response=a,
                    status=200,
                    mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/course/update/<int:id>', methods=['PUT'])
def update_course(id):
    print("update_course")
    z = Session.query(users).filter_by(id=id).all()
    if not z:
        return make_response(jsonify({'error': 'Not found'}), 404)
    c = Session.query(course).filter_by(id=id).one()
    if not c:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if request.json.get('courseName'):
        c.courseName = request.json.get('courseName')
    if request.json.get('courseDescription'):
        c.courseDescription = request.json.get('courseDescription')
    Session.commit()
    return Response(response=to_json(c, course),
                status=200,
                mimetype="application/json")


@app.route('/course/<int:id>', methods=['DELETE'])
def delete_course(id):
    u = Session.query(course).filter_by(id=id).all()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)
    try:
        cu = Session.query(course).filter_by(id=id).first()
        Session.delete(cu)
        Session.commit()
        return {
            "msg": "course deleted successfully",
            "id": id
        }
    except:
        return "course has foreign keys in other table", 405

# ----------------------- request -----------------

@app.route('/request', methods=['POST'])
def create_request():
    req = requestClass(
        requestFrom = request.json.get('requestFrom'),
        requestToCourse = request.json.get('requestToCourse'),
        requestToLector = request.json.get('requestToLector'),
    )

    Check2 = (Session.query(requestClass).filter_by(requestToCourse=req.requestToCourse).all())
    if Check2 != []:
        return make_response(jsonify({'error': 'user is already added'}), 409)

    try:
        Session.add(req)
        Session.commit()
    except IntegrityError:
        print('incorrect data')
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    a = to_json(req, requestClass)
    return Response(response=a,
                status=200,
                mimetype="application/json")




if __name__ == "__main__":
    app.run(debug=True)
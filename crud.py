# Alex Klavens coding exercise for CareDash
# aklavens@conncoll.edu
# (617) 733-1105
#
# Using Python, Flask, SQLAlchemy, and Marshmallow

# Requeired installations
# $ pip install flask_sqlalchemy
# $ pip install flask_marshmallow
# $ pip install marshmallow-sqlalchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Flask          > create instance of web app
# Request        > get request data
# jsonify        > turns json output into response object with application/json mimetype
# SQLAlchemy     > accessing databas
# Marshmallow    > seirialize object

#make instance of web app, set the path to the SQLite URI
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"crud.sqlite")

# Bind SQLAlchemy and Marshmallow into Flask app
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120),unique = True)
    reviews = db.relationship("Review",backref="doctor")#,lazy="dynamic")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))


class DoctorSchema(ma.ModelSchema):
    class Meta:
        model = Doctor
        reviews = ma.HyperlinkRelated("review.description")
        fields = ("id","name","reviews")

class ReviewSchema(ma.ModelSchema):
    class Meta:
        model = Review
        fields = ("id","doctor_id","description","doctor")


doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

# Endpoint to create a doctor
@app.route("/doctors",methods=["POST"])
def add_doctor():
    this_name = request.json["name"]
    new_doctor = Doctor(name = this_name)
    db.session.add(new_doctor)
    db.session.commit()

    return (new_doctor)

# Endpoint to get all doctors and their reviews
@app.route("/doctors",methods=["GET"])
def get_all_doctors():
    all_doctors   = Doctor.query.all()
    result        = doctors_schema.dump(all_doctors)
    return jsonify(result.data)

# Endpoint to get a doctor and their reviews by ID
@app.route("/doctors/<doctor_id>",methods=["GET"])
def get_this_doctor(doctor_id):
    this_doc = Doctor.query.filter_by(id = doctor_id).first()
    result = doctor_schema.dump(this_doc)

    return jsonify(result.data)

# Endpoint to add review to existing doctor
@app.route("/doctors/<doc_id>/reviews",methods=["POST"])
def add_review(doc_id):
    this_doc = Doctor.query.filter_by(id = doc_id).first()

    # might have to account for the {"review": {"description":"he was a good doctor"}}
    new_review = Review(description = request.json["description"],doctor = this_doc)

    db.session.add(new_review)
    db.session.commit()

    return (new_review.description)

@app.route("/doctors/<id>/reviews/<rev_id>",methods=["GET"])
def get_this_review(id,rev_id):
    this_review = Review.query.filter_by(id = rev_id).first()
    # doctor = this_review.doctor
    # result = review_schema.dump(reviews.query.filter_by(id = rev_id))
    # print("ID: "+id)
    # print("DOCID: "+str(this_review.doctor.id))
    try:
        if str(id) == str(this_review.doctor.id):
            result = review_schema.dump(this_review)
            # result = list([result,this_review.doctor])
            return jsonify(result.data)
        else:
            return "Not a valid Doctor-Review combination"
    except AttributeError:
        return "<div style = 'text-align: center;'><h1 style='font-size: 4em;'>Oh no! </h1> <p style='font-size:2em;'>This Doctor or Review might not exist<br>Alternatively, the review might exist, but it's not matched with the right doctor <p><br>If you're in the terminal, sorry for the messy html. Open this at this link: http://localhost:3000/doctors/"+str(id)+"/reviews/"+str(rev_id)+"\n"

# Endpoint to delete a doctor (and their reviews)
@app.route("/doctors/<id>",methods=["DELETE"])
def doctor_delete(id):
    doctor = Doctor.query.get(id)
    db.session.delete(doctor)
    db.session.commit()

    return doctor_schema.jsonify(doctor)

# Endpoint to delete a review froma  doctor's profile
@app.route("/doctor/<id>/reviews/<rev_id>",methods=["DELETE"])
def review_delete(id,rev_id):
    this_review = Review.query.get(rev_id)
    db.session.delete(this_review)
    db.session.commit()
    return review_schema.jsonify(this_review)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

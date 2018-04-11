# basic-python-api

## Requeired installations
pip install flask_sqlalchemy
pip install flask_marshmallow
pip install marshmallow-sqlalchemy

## How to Run
> cd to /basic-python-api

> python crud.py


### Create a doctor at localhost:3000/doctors
> curl -XPOST -H 'Content-Type: application/json' -d '{"name":"doctor_name_here"}' http://localhost:3000/doctors

### Add a review for a doctor at localhost:3000/doctors/<doctor_id>/reviews
> curl -XPOST -H 'Content-Type: application/json' -d '{"description":"My child will never be the same"}' http://localhost:3000/doctors/1/reviews

### Get all doctors at localhost:3000/doctors
> curl -XGET -H 'Content-Type: application/json' http://localhost:3000/doctors

### Get a particular review of a doctor
> curl -XGET -H 'Content-Type: application/json'http://localhost:3000/doctors/1/reviews/1

### Delete a review
> curl -XDELETE -H 'Content-Type: application/json'http://localhost:3000/doctors/1/reviews/1

### Delete a doctor
> curl -XDELETE -H 'Content-Type: application/json'http://localhost:3000/doctors/1

# basic-python-api

## Requeired installations
pip install flask_sqlalchemy
pip install flask_marshmallow
pip install marshmallow-sqlalchemy

## How to Run
> cd to /basic-python-api
> python crud.py


# Create a doctor at localhost:3000/doctors
curl -XPOST -H 'Content-Type: applications/json' -d '{"name":"doctor_name_here"}' http://localhost:3000/doctors

# Add a review for a doctor at localhost:3000/doctors/<doctor_id>/reviews
curl -XPOST -H 'Content-Type: applications/json' -d '{"description":"My child will never be the same"}' http://localhost:3000/doctors/1/reviews



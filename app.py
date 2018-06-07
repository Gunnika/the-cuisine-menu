from flask import Flask, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database1.mysql'

db= SQLAlchemy(app)

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(20))
    origin = db.Column(db.String(50))
    ingredients = db.Column(db.String(600))

@app.route("/addDish", methods=['POST'])
def addDish():
     data= request.get_json()
     c_id = data['id']
     c_name = data['name']
     c_origin = data['origin']
     c_ingredients = data['ingredients']
    
     new_cuisine = Cuisine(id= c_id, name= c_name, origin= c_origin, ingredients= json.dumps(c_ingredients))

     
     db.session.add(new_cuisine)
     db.session.commit() 
     return jsonify({"message":"Dish added"})

@app.route("/All", methods=['GET'])
def All():
    output=[]
    all_cuisines = Cuisine.query.all()
    
    for cuisine in all_cuisines:
        a_cuisine={}
        a_cuisine['id']= cuisine.id
        a_cuisine['name']= cuisine.name
        a_cuisine['origin']= cuisine.origin

        
        a_cuisine['ingredients']= json.loads(cuisine.ingredients)

        output.append(a_cuisine)
    return jsonify({"message":output})

@app.route("/origin/<place>", methods=['GET'])
def origin(place):
    output=[]
    places= Cuisine.query.filter_by(origin=place).all()
    for place1 in places:

        part = {}
        part['id']= place1.id
        part['name']= place1.name
        part['origin']=place1.origin
        part['ingredients']= json.loads(place1.ingredients)
        
        output.append(part)
    
    return jsonify({"message":output})

@app.route("/rename/<id>", methods=['POST'])
def rename(id):

    data=request.get_json()
    place1= Cuisine.query.filter_by(id=id).first()

    place1.name = data['name']
    db.session.add(place1)
    db.session.commit()
    return jsonify({"message":"Cuisine edited"})

@app.route("/addIngredient/<id>", methods=['POST'])
def addIngredient(id):
    data = request.get_json()

    place1= Cuisine.query.filter_by(id=id).first()
    
    Existing = json.loads(place1.ingredients)

    Addition= data['ingredients']

    Existing.extend(Addition)
    
    place1.ingredients=json.dumps(Existing)

    
    db.session.add(place1)
    db.session.commit()

    return jsonify({"message":"Ingredients added"})



if __name__=='__main__':
    app.run(host='0.0.0.0', debug= True)
    

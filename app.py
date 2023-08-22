from flask import Flask,jsonify, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:sql23@localhost/books'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.app_context().push()

class Book(db.Model):

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    author = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text(), nullable = False)

    def __repr__(self):
        return self.name
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class BookSchema(Schema):
    
    id = fields.Integer()
    name = fields.String()
    author = fields.String()
    description = fields.String()

@app.route('/books',methods=['GET'])
def get_all_books():
    
    books = Book.get_all()
    serializer = BookSchema(many=True)
    data = serializer.dump(books)
    return jsonify(
        data
    )


@app.route('/books',methods=['POST'])
def create_a_book():
   
    data = request.get_json()
    new_book = Book(
        name = data.get('name'),
        author = data.get('author'),
        description = data.get('description')
    )
    new_book.save()
    serializer = BookSchema()
    data = serializer.dump(new_book)
    return jsonify(
        data
    ),201


@app.route('/book/<int:id>',methods=['GET'])
def get_book(id):
    
    book = Book.get_by_id(id)
    serializer = BookSchema()
    data = serializer.dump(book)
    return jsonify(
        data
    ),200


@app.route('/book/<int:id>',methods=['PUT'])
def update_book(id):
    
    book_to_update = Book.get_by_id(id)
    data = request.get_json()

    book_to_update.name = data.get('name')
    book_to_update.author = data.get('author')
    book_to_update.description = data.get('description')

    db.session.commit()

    serializer=BookSchema()

    book_data=serializer.dump(book_to_update)

    return jsonify(book_data),200

@app.route('/book/<int:id>',methods=['DELETE'])
def delete_book(id):
    
    book_to_delete=Book.get_by_id(id)

    book_to_delete.delete()

    return jsonify({}),204

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"Error"}),500

if __name__ == '__main__':
    app.run(debug = True)


from flask import Flask, request
import book_service as dynamodb

app = Flask(__name__)

@app.route('/createTable')
def root_route():
    dynamodb.create_table_book()
    return 'Table created'

@app.route('/book', methods=['POST'])
def add_book():
    data = request.get_json()
    response = dynamodb.write_to_book(data['id'], data['title'], data['description'],  data['author'],  data['publisher'],  data['year'],  data['isbn'])
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
            'response': response
        }
    return {  
        'msg': 'Some error occcured',
        'response': response
    }

@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    response = dynamodb.read_from_book(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            return { 'Item': response['Item'] }
        return { 'msg' : 'Item not found!' }
    return {
        'msg': 'Some error occured',
        'response': response
    }

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    response = dynamodb.delete_from_book(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }
    return {  
        'msg': 'Some error occcured',
        'response': response
    } 

@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):

    data = request.get_json()
    response = dynamodb.update_in_book(id, data)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }
    return {
        'msg'      : 'Some error occured',
        'response' : response
    }   

@app.route('/upvote/book/<int:id>', methods=['POST'])
def upvote_book(id):
    response = dynamodb.upvote_a_bookBook(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'      : 'Upvotes the book successfully',
            'Upvotes'    : response['Attributes']['upvotes'],
            'response' : response['ResponseMetadata']
        }
    return {
        'msg'      : 'Some error occured',
        'response' : response
    }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
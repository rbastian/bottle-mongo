__author__ = 'rbastian'

import json
import bottle
import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.mydatabase

@bottle.route('/documents', method='PUT')
def put_document():
    data = bottle.request.body.readline()
    if not data:
        bottle.abort(400, 'No data received')

    entity = json.loads(data)
    if not entity.has_key('_id'):
        bottle.abort(400, 'No _id specified')

    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        bottle.abort(400, str(ve))


@bottle.route('/documents/:id', method='GET')
def get_document(id):
    entity = db['documents'].find_one({'_id':id})
    if not entity:
        bottle.abort(404, 'No document with id %s' % id)

    return entity

bottle.run(host='localhost', port=8080)
from djongo import models
from metaphone import doublemetaphone
# from DataCenter.Actor.ActorConnection import ActorConnection

class Actor(models.Model):
  '''
  Defines the Actor class, which can represent
  an organization, a person, or a notable group

  TODO: Add actor location
  '''
  ORGANIZATION = 'ORG'
  PERSON = 'PER'
  ACTOR_TYPE_CHOICES = (
    (ORGANIZATION, 'Organization'),
    (PERSON, 'Person')
  )

  actor_type = models.CharField(
    choices=ACTOR_TYPE_CHOICES,
    default=ORGANIZATION,
    null=False,
    max_length=50
  )

  actor_name = models.CharField(
    max_length=200
  )

  def get_metaphone_name(self):
    metaphone_name = doublemetaphone(self.actor_name)
    return (metaphone_name[0] + metaphone_name[1])

  # def __init__(self, actorType, name, locationID=None, articleIDs=[], connections={}, id=None, db=None, **kwds):
  #   '''
  #   Initializes an Actor object.
  #   '''
  #   self.actorType = actorType
  #   self.name = name
  #   metaphone_name = doublemetaphone(name)
  #   self._a_name = metaphone_name[0] + metaphone_name[1]
  #   self.locationID = locationID
  #   self.articleIDs = articleIDs

  #   # Dictionary to ActorConnections
  #   self.connections = connections

  #   if db:
  #     self._db = db
  #     self._collection = db[Actor._collectionKey]
  #     if not id:
  #       self.storeDB(db)
  #     else:
  #       self._mongoID = id
  #       self._id = str(id)

  # def addArticle(self, articleID):
  #   '''
  #   Adds an article to the Actor oject
  #   '''
  #   self.articleIDs.append(articleID)

  # def updateOrCreateConnection(self, actor, articleID):
  #   '''
  #   Adds a connection to another actor.
  #   If the connection already exists, adds the article
  #   to the existing connection

  #   If the connection doesn't exist, creates a new one.
  #   '''
  #   logging.log(3, 'Actor.updateOrCreateConnection: updating or creating connection')
  #   if actor._id in self.connections:
  #     success = self.updateConnection(actor, articleID)
  #   else:
  #     success = self.createConnection(actor, articleID)
  #   return success

  # def createConnection(self, actor, articleID):
  #   '''
  #   Creates a connection to the new actor
  #   with the new article.
  #   If the connection already exists, throws an error.
  #   '''
  #   if actor._id in self.connections:
  #     logging.error('Actor.createConnection: Connection already exists')
  #     return False

  #   connectionID = ActorConnection([self._mongoID, actor._mongoID], [articleID], db=self._db)._mongoID

  #   # push connection
  #   if not self.createOneDirectionConnection(self._mongoID, actor._mongoID, connectionID): return False
  #   if not self.createOneDirectionConnection(actor._mongoID, self._mongoID, connectionID): return False

  #   return True

  # def createOneDirectionConnection(self, primaryID, secondaryID, connectionID):
  #   '''
  #   Creates a one-directional connection. Returns True if success
  #   '''
  #   query = {'_id': primaryID}
  #   result = self._collection.update_one(query, {
  #     '$set': {f'connections.{str(secondaryID)}': connectionID}
  #   })
  #   if not result.acknowledged:
  #     logging.error('Actor.createOneDirectionConnection: createConnection not acknowledged')
  #     return False
  #   return True

  # def updateConnection(self, actor, articleID):
  #   '''
  #   Updates the existing connection between actors.
  #   If the connection doesn't exist, throws an error.
  #   '''
  #   if actor._id not in self.connections:
  #     logging.error('Actor.updateConnection: Connection does not exist')
  #     return False
  #   query = {'_id': ObjectId(self.connections[actor._mongoID])}
  #   collectionObj = self._collection.find_one(query)
  #   if not collectionObj:
  #     logging.error('Actor.updateConnection: Connection not in database')
  #     return False
  #   collectionObj['_db'] = self._db
  #   connection = ActorConnection.fromDB(collectionObj)
  #   if not connection.updateConnection(articleID): return False
  #   return True

  # def storeDB(self, db):
  #   '''
  #   Stores in database. If the ID already exists, updates the existing entry.
  #   '''
  #   if not db:
  #     logging.error('Actor.storeDB: No DB provided')
  #     return False
  #   encoding = self._serialize()
  #   self._mongoID = self._collection.insert_one(self._serialize()).inserted_id
  #   self._id = str(self._mongoID)

  #   return self._id

  # def _serialize(self):
  #   '''
  #   Serializes the actor object into JSON for Mongo storage
  #   '''
  #   return {
  #     'name': self.name,
  #     '_a_name': self._a_name,
  #     'actorType': self.actorType,
  #     'locationID': self.locationID,
  #     'articleIDs': self.articleIDs,
  #     'connections': self.connections
  #   }

  # @classmethod
  # def fromDB(cls, obj):
  #   '''
  #   Creates an Actor class from MongoDB object
  #   '''
  #   return cls(
  #     obj['actorType'], obj['name'], obj['locationID'],
  #     obj['articleIDs'], obj['connections'], obj['_id'], obj['_db'])

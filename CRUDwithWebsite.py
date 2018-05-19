from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create
def addRestaurant(restaurantName):
    newRestaurant = Restaurant(name = restaurantName)
    session.add(newRestaurant)
    session.commit()

#Read
def getAllRestaurants():
    
    """
    restaurants = session.query(Restaurant).all()
    restaurantsList = []
    for restaurant in restaurants:
        restaurantsList.append(restaurant.name)
    return restaurantsList
    """
    return session.query(Restaurant).all()

def getRestaurant(restaurantId):
    restaurantName = session.query(Restaurant).filter_by(id = restaurantId).one()
    return restaurantName.name

#Update
def editRestaurant(restaurantId, newName):
    restaurant = session.query(Restaurant).filter_by(id =restaurantId).one()
    restaurant.name = newName
    session.add(restaurant)
    session.commit()

#Delete
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    session.delete(restaurant)
    session.commit()
   


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
    restaurants = session.query(Restaurant).all()
    restaurantsList = []
    for restaurant in restaurants:
        restaurantsList.append(restaurant.name)
    return restaurantsList

#Update
def editRestaurant():
    print "edit"

#Delete
def deleteRestaurant():
    print "delete"


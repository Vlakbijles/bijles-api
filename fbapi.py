from facebook import GraphAPI
from datetime import date
from datetime import datetime


def calculateAge(birthday):
    today = date.today()
    bday_object = datetime.strptime(birthday, '%b %d %Y')
    print bday_object
    return today.year - bday_object.year - ((today.month, today.day) <
                                           (bday_object.month, bday_object.day))


# app_id = '1597503327174282'
# app_secret = '7edf79c0afb8a9858709a176a06a2454'

def getUserData(access_token):
    graph = GraphAPI(access_token)
    profile = graph.get_object('me')
    userdata = dict()
    userdata['name'] = profile['first_name']
    userdata['surname'] = profile['last_name']
    userdata['picture'] = "https://graph.facebook.com/" + profile['id'] + \
                          "/picture?redirect=true&width=200&height=200"
    print userdata

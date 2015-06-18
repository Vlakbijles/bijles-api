from facebook import GraphAPI
from datetime import date
from datetime import datetime


def calculate_age(birthday):
    today = date.today()
    bday_object = datetime.strptime(birthday, '%b %d %Y')
    return today.year - bday_object.year - ((today.month, today.day) < (bday_object.month, bday_object.day))


def get_user_data(access_token):
    graph = GraphAPI(access_token)
    try:
        profile = graph.get_object('me')
    except GraphAPI.OAuthError:
        pass

    # Redirect the user to renew his or her token
    userdata = dict()
    userdata['id'] = profile['id']
    userdata['name'] = profile['first_name']
    userdata['surname'] = profile['last_name']
    userdata['picture'] = "https://graph.facebook.com/" + profile['id'] + "/picture?redirect=true&width=200&height=200"
    userdata['acces_token'] = access_token
    # birthday = graph.get_object('me?fields=birthday')
    # userdata['age'] = calculate_age(birthday['birthday'])

    return userdata

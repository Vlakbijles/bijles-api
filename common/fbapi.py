from facebook import GraphAPI
from datetime import date
from datetime import datetime


def calculate_age(birthday):
    today = date.today()
    bday_object = datetime.strptime(birthday, '%b %d %Y')
    return today.year - bday_object.year - ((today.month, today.day) < (bday_object.month, bday_object.day))


def get_fb_user_data(access_token):
    userdata = {}
    try:
        graph = GraphAPI(access_token)
        profile = graph.get_object('me')
        userdata['id'] = profile['id']
        userdata['name'] = profile['first_name']
        userdata['email'] = profile['email']
        userdata['surname'] = profile['last_name']
        userdata['picture'] = "https://graph.facebook.com/" + profile['id'] + "/picture?redirect=true&width=200&height=200"
        userdata['access_token'] = access_token
    except GraphAPI.OAuthError:
        pass

    # Redirect the user to renew his or her token

    return userdata

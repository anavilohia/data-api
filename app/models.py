from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                return user
    return None


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.email = "email" + str(id)
        self.password = self.email + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)

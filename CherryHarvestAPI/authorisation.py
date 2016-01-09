from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    return False
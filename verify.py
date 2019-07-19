from authy.api import AuthyApiClient
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('app_config')
app.secret_key = 'super-secret'

api = AuthyApiClient(app.config['AUTHY_API_KEY'])


@app.route("/start", methods=["POST"])
def start():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")

    r = api.phones.verification_start(
        phone_number=phone_number, 
        country_code=country_code,
        via='sms')

    if r.ok():
        return jsonify(success=True, message = r.content['message'])
    else:
        return jsonify(success=False, message=r.errors()['message'])


@app.route("/check", methods=["POST"])
def check():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")
    code = request.values.get("verification_code")

    r = api.phones.verification_check(phone_number, country_code, code)

    if r.ok():
        return jsonify(success=True, message=r.content['message'])
    else:
        return jsonify(success=False, message=r.errors()['message'])


@app.route("/")
def index():
    """
    Check to make sure environment variables are set.
    """

    if app.config.get('AUTHY_API_KEY') is None:
        return """
        AUTHY_API_KEY not set as an environment variable.
        If you're running this on Heroku, add the environment variable
        using the <a href="https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard">dashboard</a>
        or the <a href="https://devcenter.heroku.com/articles/config-vars#managing-config-vars">CLI</a>
        """
    else:
        return "All set! Use /start and /check endpoints in your application."


if __name__ == '__main__':
    app.run(debug=True)
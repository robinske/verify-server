from twilio.rest import Client
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('app_config')
app.secret_key = 'super-secret'

client = Client(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])


@app.route("/start", methods=["POST"])
def start():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")
    full_phone = "+{}{}".format(country_code, phone_number)

    SERVICE = app.config['SERVICE_SID']

    r = client.verify \
        .services(SERVICE) \
        .verifications \
        .create(to=full_phone, channel='sms')

    if r.status == "pending":
        return jsonify(success=True, message="Verification sent to {}".format(r.to))
    else:
        return jsonify(success=False, message="Error sending verification. Status: {}".format(r.status))


@app.route("/check", methods=["POST"])
def check():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")
    full_phone = "+{}{}".format(country_code, phone_number)
    code = request.values.get("verification_code")
    print(code)

    SERVICE = app.config['SERVICE_SID']

    r = client.verify \
        .services(SERVICE) \
        .verification_checks \
        .create(to=full_phone, code=code)

    if r.status == "approved":
        return jsonify(success=True, message="Valid token.")
    else:
        return jsonify(success=False, message="Invalid token.")


@app.route("/")
def index():
    """
    Check to make sure environment variables are set.
    """

    config_setup_complete = app.config.get('TWILIO_ACCOUNT_SID') and \
        app.config.get('TWILIO_AUTH_TOKEN') and \
        app.config.get('VERIFY_SERVICE_SID')

    if not config_setup_complete:
        return """
        Environment variables not set: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `VERIFY_SERVICE_SID`
        If you're running this on Heroku, add the missing environment variables
        using the <a href="https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard">dashboard</a>
        or the <a href="https://devcenter.heroku.com/articles/config-vars#managing-config-vars">CLI</a>
        """
    else:
        return "All set! Use /start and /check endpoints in your application."


if __name__ == '__main__':
    app.run(debug=True)
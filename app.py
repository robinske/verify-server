from twilio.rest import Client
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('app_config')
app.secret_key = 'super-secret'

client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])


@app.route("/start", methods=["POST"])
def start():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")
    full_phone = "+{}{}".format(country_code, phone_number)

    SERVICE = app.config['VERIFY_SERVICE_SID']

    try:
        r = client.verify \
            .services(SERVICE) \
            .verifications \
            .create(to=full_phone, channel='sms')
        return jsonify(success=True, message="Verification sent to {}".format(r.to))
    except Exception as e:
        return jsonify(success=False, message="Error sending verification: {}".format(e))


@app.route("/check", methods=["POST"])
def check():
    country_code = request.values.get("country_code")
    phone_number = request.values.get("phone_number")
    full_phone = "+{}{}".format(country_code, phone_number)
    code = request.values.get("verification_code")

    SERVICE = app.config['VERIFY_SERVICE_SID']

    try:
        r = client.verify \
            .services(SERVICE) \
            .verification_checks \
            .create(to=full_phone, code=code)

        if r.status == "approved":
            return jsonify(success=True, message="Valid token.")
        else:
            return jsonify(success=False, message="Invalid token.")
    except Exception as e:
        return jsonify(success=False, message="Error checking verification: {}".format(e))


@app.route("/")
def index():
    """
    Check to make sure environment variables are set.
    """
    required_config_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'VERIFY_SERVICE_SID']
    missing_config_vars = []

    for cv in required_config_vars:
        if app.config.get(cv) is None:
            missing_config_vars.append(cv)
    
    if len(missing_config_vars) > 0:
        return """
        Environment variables not set: {}
        If you're running this on Heroku, add the missing environment variables
        using the <a href="https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard">dashboard</a>
        or the <a href="https://devcenter.heroku.com/articles/config-vars#managing-config-vars">CLI</a>
        """.format(", ".join(missing_config_vars))
    else:
        return "All set! Use /start and /check endpoints in your application."
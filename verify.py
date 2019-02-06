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


if __name__ == '__main__':
    app.run(debug=True)
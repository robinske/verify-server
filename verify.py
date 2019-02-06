from authy.api import AuthyApiClient
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.from_object('app_config')
app.secret_key = 'super-secret'

api = AuthyApiClient(app.config['AUTHY_API_KEY'])


@app.route("/start", methods=["POST"])
def start():
    country_code = request.form.get("country_code")
    phone_number = request.form.get("phone_number")

    r = api.phones.verification_start(phone_number, country_code, via='sms')

    if r.ok():
        return jsonify(message = r.content['message'])
    else:
        return jsonify(r.errors())


@app.route("/check", methods=["POST"])
def check():
    country_code = request.form.get("country_code")
    phone_number = request.form.get("phone_number")
    code = request.form.get("verification_code")

    r = api.phones.verification_check(phone_number, country_code, code)

    if r.ok():
        return jsonify(message=r.content['message'])
    else:
        return jsonify(r.errors())


if __name__ == '__main__':
    app.run(debug=True)
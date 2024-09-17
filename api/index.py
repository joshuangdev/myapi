from flask import Flask, jsonify, request, send_from_directory, url_for
import requests, os


app = Flask(__name__)

apikeylist = [
    "8yCEm6ekTJZ0rx4DfXNphuEB0arT5okuGMqFuW4wqIjbaqewkYcqsjK2MfKct3xJHdEhA80DSLv5VtxP8RTZMRthEWpFO9gtzlVYVJnbbsNyajB0Hqg0rKKviZgC2hu8"
]


@app.route("/")
def hello():
    return jsonify(
        {
            "message": "this is a private api. please email me@msft.joshuang.site for access"
        }
    )


@app.route("/api/v1/health")
def health_check():
    return jsonify({"status": "healthy"})


@app.route("/currency")
def currency():
    fromc = request.args.get("fromc", "GBP")
    toc = request.args.get("toc", "USD")
    options = request.args.get("extra", None)
    apikey = request.args.get("apikey", None)
    if not apikey:
        return jsonify({"error": "apikey is required"})
    if not apikey in apikeylist:
        return
    response = requests.get(f"https://api.vatcomply.com/rates?base={fromc}")
    data = response.json()
    if options:
        return jsonify(data)
    if toc in data["rates"]:
        rate = data["rates"][toc]
        return jsonify({"from": fromc, "to": toc, "rate": rate})
    else:
        return jsonify({"error": f"Exchange rate for {toc} not found"}), 404


@app.route("/currency/methods")
def currencyroutes():
    return jsonify(
        {
            "AUD": "Australian Dollar",
            "BGN": "Bulgarian Lev",
            "BRL": "Brazilian Real",
            "CAD": "Canadian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "CZK": "Czech Koruna",
            "DKK": "Danish Krone",
            "EUR": "Euro",
            "GBP": "Great British Pound",
            "HKD": "Hong Kong Dollar",
            "HUF": "Hungarian Forint",
            "IDR": "Indonesian Rupiah",
            "ILS": "Israeli New Shekel",
            "INR": "Indian Rupee",
            "ISK": "Icelandic Krona",
            "JPY": "Japanese Yen",
            "KRW": "South Korean Won",
            "MXN": "Mexican Peso",
            "MYR": "Malaysian Ringgit",
            "NOK": "Norwegian Krone",
            "NZD": "New Zealand Dollar",
            "PHP": "Philippine Peso",
            "PLN": "Polish Zloty",
            "RON": "Romanian Leu",
            "SEK": "Swedish Krona",
            "SGD": "Singapore Dollar",
            "THB": "Thai Baht",
            "TRY": "Turkish Lira",
            "USD": "United States Dollar",
            "ZAR": "South African Rand",
        }
    )


@app.route("/flag")
def serve_asset():
    flag = request.args.get("flag", None)
    apikey = request.args.get("apikey", None)
    if not apikey:
        return jsonify({"error": "apikey is required"})
    if not apikey in apikeylist:
        return
    if not flag:
        return jsonify({"error": "flag is required"})
    return send_from_directory(os.path.join("../assets"), f"{flag}.png")


if __name__ == "__main__":
    app.run(debug=True)

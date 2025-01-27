from flask import Flask, jsonify, request, send_from_directory, url_for
import requests, os, json, time


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


@app.route("/currency/convert")
def currencynameconvert():
    text = request.args.get("text", None)
    apikey = request.args.get("apikey", None)
    if not apikey:
        return jsonify({"error": "apikey is required"})
    if not apikey in apikeylist:
        return jsonify({"error": "invalid apikey"})
    if not text:
        return jsonify({"error": "text is required"})

    currency_codes = {
        "Australian Dollar (AUD)": "AUD",
        "Bulgarian    Lev (BGN)": "BGN",
        "Brazilian Real (BRL)": "BRL",
        "Canadian Dollar (CAD)": "CAD",
        "Swiss Franc (CHF)": "CHF",
        "Chinese Yuan (CNY)": "CNY",
        "Czech Koruna (CZK)": "CZK",
        "Danish Krone (DKK)": "DKK",
        "Euro (EUR)": "EUR",
        "Great British Pound (GBP)": "GBP",
        "Hong Kong Dollar (HKD)": "HKD",
        "Hungarian Forint (HUF)": "HUF",
        "Indonesian Rupiah (IDR)": "IDR",
        "Israeli New Shekel (ILS)": "ILS",
        "Indian Rupee (INR)": "INR",
        "Icelandic Krona (ISK)": "ISK",
        "Japanese Yen (JPY)": "JPY",
        "South Korean Won (KRW)": "KRW",
        "Mexican Peso (MXN)": "MXN",
        "Malaysian Ringgit (MYR)": "MYR",
        "Norwegian Krone (NOK)": "NOK",
        "New Zealand Dollar (NZD)": "NZD",
        "Philippine Peso (PHP)": "PHP",
        "Polish Zloty (PLN)": "PLN",
        "Romanian Leu (RON)": "RON",
        "Swedish Krona (SEK)": "SEK",
        "Singapore Dollar (SGD)": "SGD",
        "Thai Baht (THB)": "THB",
        "Turkish Lira (TRY)": "TRY",
        "United States Dollar (USD)": "USD",
        "South African Rand (ZAR)": "ZAR",
    }

    currency_code = currency_codes.get(text)

    if currency_code:
        return jsonify({"currency": text, "code": currency_code})
    else:
        return jsonify({"error": f"Currency code for '{text}' not found"}), 404


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


@app.route("/convertcountryname")
def convert_country_name():
    name = request.args.get("name", None)
    apikey = request.args.get("apikey", None)
    if not apikey:
        return jsonify({"error": "apikey is required"})
    if not apikey in apikeylist:
        return jsonify({"error": "invalid apikey"})
    if not name:
        return jsonify({"error": "name is required"})
    with open("./data/countryname.json") as f:
        countryname = json.load(f)

    code = countryname.get(name)
    if code:
        return jsonify({"country": name, "code": code})
    else:
        return jsonify({"error": f"Country code for '{name}' not found"}), 404


@app.route("/tka/students")
def studentstkarestricted():
    start = time.time()
    query = request.args.get("q", "").lower()
    apikey = request.args.get("apikey", None)

    if not apikey:
        return jsonify({"error": "apikey is required"})
    if apikey not in apikeylist:
        return jsonify({"error": "invalid apikey"})

    try:
        with open("./data/tkastudents.json") as f:
            students = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "Failed to load student data"}), 500

    p1, p2, p3, exact = [], [], [], []

    for item in students:
        parts = item.lower().split()
        if item.lower() == query:
            exact.append(item)
        if parts[0].startswith(query):
            p1.append(item)
        elif len(parts) > 1 and parts[1].startswith(query):
            p2.append(item)
        elif any(query in part for part in parts):
            p3.append(item)
    results = p1 + p2 + p3

    return jsonify(
        {
            "$Disclaimer": "By using this data, you acknowledge and agree that you are not permitted to use, share, or distribute any personal information without the explicit permission of Joshua Ng or Joshua Ng Cooperation International LLC. Unauthorized use of this data constitutes a violation of privacy laws and is subject to legal action. If you have accessed this data without explicit permission, you must immediately cease using it, delete any stored data, and close any related systems or databases. Failure to comply with these terms is illegal and may result in legal consequences. In particular, unauthorized use of this data may violate the following laws and regulations: General Data Protection Regulation (GDPR) - European Union: Article 5: Principles relating to the processing of personal data (purpose limitation, data minimization, etc.). Article 6: Lawfulness of processing (requirement of a lawful basis for data processing, including consent). Article 7: Conditions for consent (explicit consent required for processing data, including for minors). Article 32: Security of processing (requirement for appropriate security measures in handling personal data). Data Protection Act 2018 - United Kingdom: Section 1: Processing personal data (must be done fairly, lawfully, and transparently). Section 4: Special categories of personal data (requires stricter conditions for processing sensitive data). Section 40: Penalties for non-compliance with data protection regulations, including unauthorized access or processing. Schedule 1: Conditions for processing data, particularly consent and protection of minors. Family Educational Rights and Privacy Act (FERPA) - United States: Section 1232g: Prohibition on unauthorized disclosure of educational records.n 1232g(b): Consent requirement for the release of educational records. Failure to comply with these laws may result in civil and criminal penalties, including fines and legal action. You are required to immediately stop using the data, delete any stored information, and discontinue all related activities to avoid legal consequences.",
            "01-Exact Match": exact,
            "02-First Name Match": p1,
            "03-Last Name Match": p2,
            "04-Any Partial Match": p3,
            "Sorted Results": results,
            "Time Elapsed": f"{time.time() - start} seconds",
            "Data Returned": len(results),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

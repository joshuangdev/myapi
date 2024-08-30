from flask import Flask, abort, jsonify, request, url_for, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, random
from functools import wraps

app = Flask(__name__)


def rd():
    char = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+"
    result = ""
    for i in range(10):
        result += char[random.randint(0, len(char) - 1)]
    return result


API_KEY = rd()
used = False

# Initialize WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(7)


# Weak Authentication
def authenticate_request(request):
    """Authenticate request based on API key."""
    api_key = request.headers.get("Authorization")
    if (
        api_key
        and api_key
        == f"Bearer {API_KEY}TR2auz2gY8KJjrErt9f3HQpAKJL6tA0zMPeje2pSLrjfim4ho9C2W8VlfXcvocVMLW7C8YFPegnXOkPa2uG5oczz9fETkJgvWF4yNrGRnMeHuIBUZL98rrww6LLXG1vr"
    ):
        return True
    return False


@app.route("/")
def route():
    return "404"


@app.route("/unauthorized")
def unauthorized():
    return abort(403)


@app.route("/r/<a>")
def r(a):
    global used
    if (
        a
        == "vktLOEsqWBsIlyXbAuc0cDuxELiVTiP9WDHjNSemqYO87pi217e27fCdFj4BjUs7NHPVYp3TduCj2cgPFVgvl6d76Kqdrazdn6XOIYLulVkJt7azoMHox6IwsOHYnueo"
        and not used
    ):
        used = True
        return API_KEY


@app.route("/api/v1/dvla/<plate>")
def dvlaapi(plate):
    if request.method == "POST":
        return redirect(url_for("route"), code=301)
    if not authenticate_request(request):
        return redirect(url_for("unauthorized"), 301)
    start_time = time.time()
    try:
        result = driverprocess(plate)
        if not result:
            elapsed_time = time.time() - start_time
            return (
                jsonify(
                    {
                        "Error": "Please check terminal",
                        "TimeTaken": f"{elapsed_time:.2f} seconds",
                    }
                ),
                500,
            )
        elapsed_time = time.time() - start_time
        result["timetaken"] = f"{elapsed_time:.2f} seconds"
        return jsonify(result), 200
    except Exception:
        return jsonify({"Error": "Internal Server Error"}), 500


def driverprocess(carplate: str = None):
    if not carplate:
        raise ValueError("Car plate is required.")
    success = False

    def ExtractTaxMot(panels):
        details = {}
        for panel in panels:
            title_element = panel.find_element(By.CLASS_NAME, "govuk-panel__title")
            title = title_element.text.strip()
            body_element = panel.find_element(By.CLASS_NAME, "govuk-panel__body")
            body_text = body_element.text.strip()

            lines = body_text.split("\n")
            if "Taxed" in title:
                details["Tax_Status"] = {
                    "Status": "Taxed",
                    "Tax_Due": lines[-1] if lines else "Not Available",
                }
            elif "MOT" in title:
                details["MOT_Status"] = {
                    "Status": lines[0].strip() if len(lines) > 0 else "Not Available",
                    "Details": lines[1].strip() if len(lines) > 1 else "Not Available",
                }

        if "Tax_Status" not in details:
            details["Tax_Status"] = {
                "Status": "Not Available",
                "Tax_Due": "Not Available",
            }
        if "MOT_Status" not in details:
            details["MOT_Status"] = {
                "Status": "Not Available",
                "Details": "Not Available",
            }
        return details

    def ExtractDetails(detailsclass):
        details = {}
        rows = detailsclass.find_elements(By.CLASS_NAME, "govuk-summary-list__row")
        for row in rows:
            dt = row.find_element(By.TAG_NAME, "dt").text
            dd = row.find_element(By.TAG_NAME, "dd").text
            details[dt] = dd
        return details

    try:
        driver.get("https://vehicleenquiry.service.gov.uk/")
        text_field = driver.find_element(
            By.ID, "wizard_vehicle_enquiry_capture_vrn_vrn"
        )
        text_field.send_keys(carplate)
        driver.find_element(By.ID, "submit_vrn_button").click()
        try:
            driver.find_element(By.ID, "yes-vehicle-confirm").click()
        except Exception:
            return None  # Vehicle not found or not confirmed
        driver.find_element(By.ID, "capture_confirm_button").click()

        resultdetails = {}
        panels = driver.find_elements(By.CLASS_NAME, "govuk-panel--confirmation")
        detailsclass = driver.find_element(By.CLASS_NAME, "summary-no-action")
        resultdetails["TaxAndMot"] = ExtractTaxMot(panels)
        resultdetails["OtherDetails"] = ExtractDetails(detailsclass)
        success = True
    except Exception:
        return None
    finally:
        # Do not quit the driver here if it's reused
        if success:
            return resultdetails
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import os

from flask import Flask, request, render_template, redirect, session, make_response

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils


app = Flask(__name__)
# change the secret key of the app here
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'rpi_saml')
# Path to SAML Folder, in this example it would be saml but you can change it to any folder.
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')

# OneLogin_Saml2 instance
def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth

# Prepare Flask Request for the OneLogin instance
def prepare_flask_request(request):
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host": request.host,
        "script_name": request.path,
        "get_data": request.args.copy(),
        "post_data": request.form.copy(),
    }

# Index
@app.route("/", methods=["GET"])
def index():
    paint_logout = False

    attributes = ''
    if "samlUserdata" in session:
        paint_logout = True
        if len(session["samlUserdata"]) > 0:
            attributes = session["samlUserdata"].items()
    print(attributes)
    return render_template("index.html", attributes=attributes, paint_logout=paint_logout)

# Metadata file that RPI wants
@app.route("/metadata/")
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers["Content-Type"] = "text/xml"
    else:
        resp = make_response(", ".join(errors), 500)
    return resp

# login, redirect to index
@app.route("/login")
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    
    return redirect(auth.login("/"))

# logout, redirects to index
@app.route("/logout")
def logout():
    # you can clear the session, but the more correct way of doing this would be to delete all the attributes that got inserted in to the session
    session.clear()
    return redirect("/")

# acs, where all of the data that SAML gives are processed
@app.route('/acs', methods=['POST'])
def acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False
    request_id = None
    if "AuthNRequestID" in session:
        request_id = session["AuthNRequestID"]

    auth.process_response(request_id=request_id)
    errors = auth.get_errors()
    not_auth_warn = not auth.is_authenticated()
    if len(errors) == 0:
        if "AuthNRequestID" in session:
            del session["AuthNRequestID"]
        session["samlUserdata"] = auth.get_attributes()
        session["samlNameId"] = auth.get_nameid()
        session["samlNameIdFormat"] = auth.get_nameid_format()
        session["samlNameIdNameQualifier"] = auth.get_nameid_nq()
        session["samlNameIdSPNameQualifier"] = auth.get_nameid_spnq()
        session["samlSessionIndex"] = auth.get_session_index()
        self_url = OneLogin_Saml2_Utils.get_self_url(req)
        if "RelayState" in request.form and self_url != request.form["RelayState"]:
            # To avoid 'Open Redirect' attacks, before execute the redirection confirm
            # the value of the request.form['RelayState'] is a trusted URL.
            return redirect(auth.redirect_to(request.form["RelayState"]))
    elif auth.get_settings().is_debug_active():
        error_reason = auth.get_last_error_reason()
    return render_template("index.html", errors=errors, error_reason=error_reason, not_auth_warn=not_auth_warn, success_slo=success_slo, attributes=attributes, paint_logout=paint_logout)

# running the file
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
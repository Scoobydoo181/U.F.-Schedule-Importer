from flask import Flask, render_template, request, redirect, session, url_for
from Static.Python.google_calendar import upload_gcal, credentials_to_dict

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

app = Flask(__name__, template_folder='./Templates',static_folder='./Static')
app.secret_key = "646a20329427e36a6e2e17c2b2037697efd4d84ddbbab1bc6fa413e34dd835e2"


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/how-it-works/')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/import/')
def import_():
    return render_template('import.html')

#Endpoint for the form containing the UFSchedule.ics file
@app.route('/calendar_import', methods=['POST'])
def calendar_import():
    """Parse file enclose in form if already authenticated, else send user to authenticate"""

    if 'credentials' not in session:
        #The form is submit initially and the user needs to authenticate with google
        session['file_text'] = request.files['file'].read()
        return redirect(url_for('authorize'))
    
    #The user has already authenticated and the processing can be done

    credentials = Credentials(**session['credentials'])

    #Parse file and send data
    upload_gcal(session['file_text'], credentials)

    #Store credentials
    session['credentials'] = credentials_to_dict(credentials)

    #Send the user to the success page
    return redirect(url_for('success'))


@app.route('/authorize')
def authorize():
    SCOPES = ['https://www.googleapis.com/auth/calendar.events'] 
    
    #Load application credentials and set redirect url for callback
    flow = Flow.from_client_secrets_file('Static/Python/credentials.json', scopes=SCOPES)
    flow.redirect_uri = url_for('oauth_callback', _external=True)

    #Get authorization url and save state to session
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state

    #Send user to authorize
    return redirect(authorization_url)

@app.route('/oauth-callback')
def oauth_callback():
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    state = session['state']

    flow = Flow.from_client_secrets_file('Static/Python/credentials.json', scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth_callback', _external=True)

    #Exchange response for token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    #Store credentials in session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('calendar_import'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':    
    app.run(debug=True)
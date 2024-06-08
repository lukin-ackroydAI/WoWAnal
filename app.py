pp.py
git commit -m "Add app.py with improved error handling"
git push origin main
import os
import requests
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'http://127.0.0.1:5000/callback'

@app.route('/')
def login():
    auth_url = f"https://www.warcraftlogs.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://www.warcraftlogs.com/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_response = requests.post(token_url, data=token_data)
    
    try:
        token_json = token_response.json()
    except requests.exceptions.JSONDecodeError:
        return 'Error decoding token response'

    session['access_token'] = token_json.get('access_token')
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    profile_url = 'https://www.warcraftlogs.com/api/v2/user'
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}"
    }
    profile_response = requests.get(profile_url, headers=headers)
    
    try:
        profile_json = profile_response.json()
    except requests.exceptions.JSONDecodeError:
        return 'Error decoding profile response'
    
    return profile_json

@app.route('/logs')
def logs():
    report_url = 'https://www.warcraftlogs.com/api/v2/client'
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}"
    }
    report_data = {
        "query": """
        {
            reportData {
                reports(limit: 10) {
                    data {
                        code
                        title
                        owner {
                            name
                        }
                        fights {
                            id
                            name
                            kill
                        }
                    }
                }
            }
        }
        """
    }
    report_response = requests.post(report_url, json=report_data, headers=headers)
    
    try:
        report_json = report_response.json()
    except requests.exceptions.JSONDecodeError:
        return 'Error decoding report response'
    
    return report_json

@app.route('/guild_characters')
def guild_characters():
    guild_id = 123456  # Replace with your guild ID
    character_url = 'https://www.warcraftlogs.com/api/v2/client'
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}"
    }
    character_data = {
        "query": f"""
        {{
            characterData {{
                characters(guildID: {guild_id}) {{
                    data {{
                        id
                        name
                        classID
                        specID
                    }}
                }}
            }}
        }}
        """
    }
    character_response = requests.post(character_url, json=character_data, headers=headers)
    
    try:
        character_json = character_response.json()
    except requests.exceptions.JSONDecodeError:
        return 'Error decoding character response'
    
    return character_json

if __name__ == '__main__':
    app.run(debug=True)


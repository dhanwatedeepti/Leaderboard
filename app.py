from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, template_folder='templates')  # Make sure HTML is in /templates
CORS(app)

EXCEL_FILE = 'leaderboard/Leaderboard.xlsx'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/Leaderboard')
def leaderboard():
    df = pd.read_excel(EXCEL_FILE, sheet_name="users")
    df = df[['Name', 'Score', 'Email']].sort_values(by='Score', ascending=False)
    players = df.to_dict(orient='records')
    return jsonify([
        {"name": p['Name'], "score": int(p['Score']), "email": p['Email']} for p in players
    ])

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render gives a random port
    app.run(host='0.0.0.0', port=port, debug=True)

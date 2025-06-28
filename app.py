from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, template_folder='templates')  # Make sure HTML is in /templates
CORS(app)

EXCEL_FILE = 'Leaderboard.xlsx'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/Leaderboard')
def leaderboard():
    try:
        
        EXCEL_FILE = 'Leaderboard.xlsx'
        df = pd.read_excel(EXCEL_FILE)
        # Check required columns
        if not all(col in df.columns for col in ['Name', 'Score', 'Email']):
            return jsonify({"error": "Missing one or more required columns: Name, Score, Email"}), 400
        df = df[['Name', 'Score', 'Email']].sort_values(by='Score', ascending=False)
        players = df.to_dict(orient='records')
        return jsonify([
            {"name": p['Name'], "score": int(p['Score']), "email": p['Email']} for p in players
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render gives a random port
    app.run(host='0.0.0.0', port=port, debug=True)

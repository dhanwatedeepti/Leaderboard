from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

EXCEL_FILE = 'Leaderboard.xlsx'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/Leaderboard')
def leaderboard():
    try:
        df = pd.read_excel(EXCEL_FILE)

        required = ['Name', 'Score', 'Email']
        missing = [col for col in required if col not in df.columns]
        if missing:
            return jsonify({"error": f"Missing column(s): {missing}. Found: {df.columns.tolist()}"}), 400

        df = df[required].sort_values(by='Score', ascending=False)
        players = df.to_dict(orient='records')

        result = []
        for p in players:
            name = p['Name']
            jpg_path = os.path.join(app.static_folder, f"{name}.jpg")
            png_path = os.path.join(app.static_folder, f"{name}.png")

            if os.path.exists(jpg_path):
                image = f"{name}.jpg"
            elif os.path.exists(png_path):
                image = f"{name}.png"
            else:
                image = "default.jpg"

            result.append({
                "name": name,
                "score": int(p['Score']),
                "email": p['Email'],
                "image": image
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

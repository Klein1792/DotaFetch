from flask import Flask, request
import requests

app = Flask(__name__)

def fetch_dota_data(steam_id_32):
    url = f"https://api.opendota.com/api/players/{steam_id_32}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "API error"}

def fetch_wl_data(steam_id_32):
    url = f"https://api.opendota.com/api/players/{steam_id_32}/wl?limit=10"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "API error"}

@app.route('/mmr/<steam_id_32>')
def get_mmr(steam_id_32):
    data = fetch_dota_data(steam_id_32)
    if "error" in data:
        return data["error"]
    leaderboard_rank = data.get("leaderboard_rank")
    if leaderboard_rank is not None:
        return f"Leaderboard Rank: {leaderboard_rank}"
    solo_mmr = data.get("solo_competitive_rank", "Not public")
    return f"Solo MMR: {solo_mmr}"

@app.route('/wl/<steam_id_32>')
def get_wl(steam_id_32):
    data = fetch_wl_data(steam_id_32)
    if "error" in data:
        return data["error"]
    wins = data.get("win", 0)
    losses = data.get("lose", 0)
    total = wins + losses
    win_rate = (wins / total * 100) if total > 0 else 0
    return total > 0 and f"Wins/Losses (last 10): {wins}/{losses} ({win_rate:.1f}%)" or "No recent matches found"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
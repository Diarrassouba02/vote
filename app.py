from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os


liste_numero=['0707871695','0595081204',
              '0747777610','0779086153'
              ,'67003373','0544506738',
               '0701719813','0707441838',
               '0757190488','0777990808',
               '0709790650','0709885676',
               '08908496','0708398140',
               '0747855212','0506134518',
               '0749756028','82834829',
               '0747628299','0404016555',
               '0748185271','0173299878'
               '0140760133','0708167296'
               ]
app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'votes.json')

def load_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def init_db():
    """Initialiser la BD si elle n'existe pas"""
    try:
        if not os.path.exists(DB_PATH):
            default_data = {
                "candidates": [
                    {"id": 1, "nom": "KOUASSI Ange", "slogan": "Unis pour une 6ème meilleure !", "emoji": "🌟", "votes": 0},
                    {"id": 2, "nom": "DIALLO Fatou", "slogan": "Ensemble, on va plus loin !", "emoji": "🚀", "votes": 0},
                    {"id": 3, "nom": "BAMBA Koné", "slogan": "Le changement, c'est maintenant !", "emoji": "⚡", "votes": 0},
                    {"id": 4, "nom": "OUATTARA Mariam", "slogan": "La force de l'unité !", "emoji": "💪", "votes": 0}
                ],
                "voters": []
            }
            save_db(default_data)
            print(f"✅ BD créée: {DB_PATH}")
        else:
            print(f"✅ BD existe déjà: {DB_PATH}")
    except Exception as e:
        print(f"❌ Erreur init_db: {e}")

# Initialiser la BD au démarrage
init_db()

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        db = load_db()
        return jsonify(db['candidates'])
    except Exception as e:
        print(f"❌ Erreur get_candidates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()
    telephone = data.get('telephone', '').strip()
    candidate_id = data.get('candidate_id')
    
    if telephone not in liste_numero:
       return jsonify({'error': 'Ce numéro n\'est pas autorisé à voter'}), 403

    if not telephone or not candidate_id:
        return jsonify({'error': 'Numéro de téléphone et candidat requis'}), 400

    # Validate phone number (Côte d'Ivoire format)
    import re
    phone_clean = re.sub(r'\s+', '', telephone)
    if not re.match(r'^(0?[0-9]{8,10})$', phone_clean):
        return jsonify({'error': 'Numéro de téléphone invalide'}), 400

    db = load_db()

    # Check if already voted
    if phone_clean in db['voters']:
        return jsonify({'error': 'Ce numéro a déjà voté !'}), 409

    # Find candidate
    candidate = next((c for c in db['candidates'] if c['id'] == candidate_id), None)
    if not candidate:
        return jsonify({'error': 'Candidat introuvable'}), 404

    # Register vote
    candidate['votes'] += 1
    db['voters'].append(phone_clean)
    save_db(db)

    return jsonify({'success': True, 'message': f'Vote pour {candidate["nom"]} enregistré !'})

@app.route('/api/results', methods=['GET'])
def get_results():
    db = load_db()
    total = sum(c['votes'] for c in db['candidates'])
    results = []
    for c in db['candidates']:
        results.append({
            **c,
            'percentage': round((c['votes'] / total * 100) if total > 0 else 0, 1)
        })
    results.sort(key=lambda x: x['votes'], reverse=True)
    return jsonify({'candidates': results, 'total_votes': total})

@app.route('/api/check-phone', methods=['POST'])
def check_phone():
    data = request.get_json()
    telephone = data.get('telephone', '').strip()
    import re
    phone_clean = re.sub(r'\s+', '', telephone)
    db = load_db()
    already_voted = phone_clean in db['voters']
    return jsonify({'already_voted': already_voted})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

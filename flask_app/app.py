from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Initialiser Supabase dans une fonction
def get_supabase():
    from supabase import create_client
    url = os.environ.get("SUPABASE_URL", "https://piqxujpixtloryjlmett.supabase.co")
    key = os.environ.get("SUPABASE_KEY", "sb_publishable_WVFlat2SPzaEnkgm6y6meA_idLg03H1")
    return create_client(url, key)

@app.route('/')
def index():
    """Page d'accueil"""
    supabase = get_supabase()
    moments = supabase.table('moments').select('*').order('created_at', desc=True).execute()
    return render_template('index.html', moments=moments.data)

@app.route('/create', methods=['POST'])
def create_moment():
    """Créer un moment"""
    supabase = get_supabase()
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'mode': request.form['mode'],
        'created_by': request.form['created_by']
    }
    supabase.table('moments').insert(data).execute()
    return redirect(url_for('index'))

@app.route('/moment/<int:moment_id>')
def moment_detail(moment_id):
    """Détails d'un moment"""
    supabase = get_supabase()
    moment = supabase.table('moments').select('*').eq('id', moment_id).single().execute()
    participants = supabase.table('participations').select('*').eq('moment_id', moment_id).eq('status', 'approved').execute()
    requests = supabase.table('participations').select('*').eq('moment_id', moment_id).eq('status', 'pending').execute()
    return render_template('moment.html', moment=moment.data, participants=participants.data, requests=requests.data)

@app.route('/join/<int:moment_id>', methods=['POST'])
def join_moment(moment_id):
    """Rejoindre un moment"""
    supabase = get_supabase()
    moment = supabase.table('moments').select('mode').eq('id', moment_id).single().execute()
    status = 'approved' if moment.data['mode'] == 'auto' else 'pending'
    
    data = {
        'moment_id': moment_id,
        'user_name': request.form['user_name'],
        'status': status
    }
    supabase.table('participations').insert(data).execute()
    return redirect(url_for('moment_detail', moment_id=moment_id))

@app.route('/approve/<int:participation_id>')
def approve_request(participation_id):
    """Approuver une demande"""
    supabase = get_supabase()
    participation = supabase.table('participations').select('moment_id').eq('id', participation_id).single().execute()
    supabase.table('participations').update({'status': 'approved'}).eq('id', participation_id).execute()
    return redirect(url_for('moment_detail', moment_id=participation.data['moment_id']))

@app.route('/reject/<int:participation_id>')
def reject_request(participation_id):
    """Rejeter une demande"""
    supabase = get_supabase()
    participation = supabase.table('participations').select('moment_id').eq('id', participation_id).single().execute()
    moment_id = participation.data['moment_id']
    supabase.table('participations').delete().eq('id', participation_id).execute()
    return redirect(url_for('moment_detail', moment_id=moment_id))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
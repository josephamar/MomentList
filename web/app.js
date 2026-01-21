// Configuration Supabase
const SUPABASE_URL = 'https://piqxujpixtloryjlmett.supabase.co';
const SUPABASE_KEY = 'sb_publishable_WVFlat2SPzaEnkgm6y6meA_idLg03H1';

// Initialiser le client Supabase
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

let currentMomentId = null;

// Au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    loadMoments();
    setupEventListeners();
});

// Configuration des écouteurs d'événements
function setupEventListeners() {
    document.getElementById('createMomentForm').addEventListener('submit', createMoment);
    document.getElementById('joinBtn').addEventListener('click', joinMoment);
    document.getElementById('backBtn').addEventListener('click', backToList);
}

// Afficher un message
function showMessage(text, type = 'success') {
    const container = document.querySelector('.container');
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    container.insertBefore(message, container.firstChild);
    
    setTimeout(() => message.remove(), 3000);
}

// Créer un moment
async function createMoment(e) {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const mode = document.getElementById('mode').value;
    const createdBy = document.getElementById('createdBy').value;
    
    const { data, error } = await supabase
        .from('moments')
        .insert([{ title, description, mode, created_by: createdBy }])
        .select();
    
    if (error) {
        showMessage('Erreur lors de la création: ' + error.message, 'error');
        return;
    }
    
    showMessage('✅ Moment créé avec succès!');
    document.getElementById('createMomentForm').reset();
    loadMoments();
}

// Charger tous les moments
async function loadMoments() {
    const { data, error } = await supabase
        .from('moments')
        .select('*')
        .order('created_at', { ascending: false });
    
    if (error) {
        showMessage('Erreur lors du chargement: ' + error.message, 'error');
        return;
    }
    
    displayMoments(data);
}

// Afficher les moments
function displayMoments(moments) {
    const container = document.getElementById('momentsList');
    
    if (moments.length === 0) {
        container.innerHTML = '<p>Aucun moment disponible. Créez-en un!</p>';
        return;
    }
    
    container.innerHTML = moments.map(moment => `
        <div class="moment-card" onclick="showMomentDetails(${moment.id})">
            <h3>${moment.title}</h3>
            <p>${moment.description}</p>
            <p><strong>Créé par:</strong> ${moment.created_by}</p>
            <span class="moment-badge badge-${moment.mode}">
                ${moment.mode === 'auto' ? '🚀 Auto' : '📨 Sur demande'}
            </span>
        </div>
    `).join('');
}

// Afficher les détails d'un moment
async function showMomentDetails(momentId) {
    currentMomentId = momentId;
    
    // Charger le moment
    const { data: moment, error: momentError } = await supabase
        .from('moments')
        .select('*')
        .eq('id', momentId)
        .single();
    
    if (momentError) {
        showMessage('Erreur: ' + momentError.message, 'error');
        return;
    }
    
    // Afficher les infos du moment
    document.getElementById('momentInfo').innerHTML = `
        <h3>${moment.title}</h3>
        <p>${moment.description}</p>
        <p><strong>Mode:</strong> ${moment.mode === 'auto' ? 'Rejoindre automatiquement' : 'Sur demande'}</p>
        <p><strong>Créé par:</strong> ${moment.created_by}</p>
    `;
    
    // Cacher la liste, montrer les détails
    document.querySelector('.moments-list').style.display = 'none';
    document.querySelector('.create-moment').style.display = 'none';
    document.getElementById('momentDetails').style.display = 'block';
    
    // Charger participants et demandes
    loadParticipants(momentId);
    loadRequests(momentId);
}

// Rejoindre un moment
async function joinMoment() {
    const userName = document.getElementById('userName').value.trim();
    
    if (!userName) {
        showMessage('Veuillez entrer votre nom', 'error');
        return;
    }
    
    // Récupérer le moment pour connaître son mode
    const { data: moment } = await supabase
        .from('moments')
        .select('mode')
        .eq('id', currentMomentId)
        .single();
    
    const status = moment.mode === 'auto' ? 'approved' : 'pending';
    
    const { error } = await supabase
        .from('participations')
        .insert([{
            moment_id: currentMomentId,
            user_name: userName,
            status: status
        }]);
    
    if (error) {
        if (error.code === '23505') {
            showMessage('Vous participez déjà à ce moment!', 'error');
        } else {
            showMessage('Erreur: ' + error.message, 'error');
        }
        return;
    }
    
    if (status === 'approved') {
        showMessage('✅ Vous avez rejoint le moment!');
        loadParticipants(currentMomentId);
    } else {
        showMessage('📨 Demande envoyée! En attente d\'approbation.');
        loadRequests(currentMomentId);
    }
    
    document.getElementById('userName').value = '';
}

// Charger les participants
async function loadParticipants(momentId) {
    const { data, error } = await supabase
        .from('participations')
        .select('*')
        .eq('moment_id', momentId)
        .eq('status', 'approved');
    
    if (error) {
        showMessage('Erreur: ' + error.message, 'error');
        return;
    }
    
    const container = document.getElementById('participantsList');
    
    if (data.length === 0) {
        container.innerHTML = '<p>Aucun participant pour le moment.</p>';
        return;
    }
    
    container.innerHTML = data.map(p => `
        <div class="participant-item">
            <span>👤 ${p.user_name}</span>
        </div>
    `).join('');
}

// Charger les demandes en attente
async function loadRequests(momentId) {
    const { data, error } = await supabase
        .from('participations')
        .select('*')
        .eq('moment_id', momentId)
        .eq('status', 'pending');
    
    if (error) {
        showMessage('Erreur: ' + error.message, 'error');
        return;
    }
    
    const container = document.getElementById('requestsList');
    
    if (data.length === 0) {
        container.innerHTML = '<p>Aucune demande en attente.</p>';
        return;
    }
    
    container.innerHTML = data.map(r => `
        <div class="request-item">
            <span>👤 ${r.user_name}</span>
            <div class="request-actions">
                <button class="btn-approve" onclick="approveRequest(${r.id})">✅ Approuver</button>
                <button class="btn-reject" onclick="rejectRequest(${r.id})">❌ Rejeter</button>
            </div>
        </div>
    `).join('');
}

// Approuver une demande
async function approveRequest(participationId) {
    const { error } = await supabase
        .from('participations')
        .update({ status: 'approved' })
        .eq('id', participationId);
    
    if (error) {
        showMessage('Erreur: ' + error.message, 'error');
        return;
    }
    
    showMessage('✅ Demande approuvée!');
    loadParticipants(currentMomentId);
    loadRequests(currentMomentId);
}

// Rejeter une demande
async function rejectRequest(participationId) {
    const { error } = await supabase
        .from('participations')
        .delete()
        .eq('id', participationId);
    
    if (error) {
        showMessage('Erreur: ' + error.message, 'error');
        return;
    }
    
    showMessage('❌ Demande rejetée.');
    loadRequests(currentMomentId);
}

// Retour à la liste
function backToList() {
    document.querySelector('.moments-list').style.display = 'block';
    document.querySelector('.create-moment').style.display = 'block';
    document.getElementById('momentDetails').style.display = 'none';
    loadMoments();
}
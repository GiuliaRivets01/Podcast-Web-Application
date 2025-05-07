from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_session import Session
from datetime import date, datetime
import dao

from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from PIL import Image

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# HOME PAGE
@app.route('/', methods=['GET', 'POST'])
def home():
  podcasts = dao.get_podcasts()
  return render_template('home.html', podcasts = podcasts)


# PROFILO UTENTE
@app.route('/users/<int:id>')
def profilo(id):
    user = dao.get_user_by_id(id)

    # Nella pagina del profilo dell'utente viene eventualmente visualizzata anche la lista degli episodi che segue 
    follow = dao.get_follow(id)
    return render_template('profilo.html', user = user, follow = follow)


# PAGINA DEL SINGOLO PODCAST 
@app.route('/podcasts/<int:id>')
def single_pod(id):
    pod = dao.get_pod(id)
    episodi = dao.get_episodes(id)

    # Quando un episodio viene modificato/aggiunto/cancellato, la lista degli episodi viene aggiornata
    modifica_lista_ep(id)

    # user_in_db è usato per verificare se un certo user segue già un preciso podcast oppure no
    user_in_db = False
    if current_user.is_authenticated:
        user_id = current_user.id
        podcast_id = pod['id']
        user_in_db = dao.get_user_in_follow(user_id, podcast_id)
        if user_in_db:
            user_in_db = 1
        else:
            user_in_db = 0

    return render_template('pod.html', pod=pod, episodi = episodi, user_in_db = user_in_db)

def modifica_lista_ep(id):
    pod = dao.get_pod(id)
    episodi = dao.get_episodes(id)
    dao.modify_lista_episodi(pod, episodi)
    return


# PAGINA DEL SINGOLO EPISODIO
@app.route('/episodes/<int:id>')
def single_ep(id):
    ep = dao.get_ep(id)
    commenti = dao.get_comments(ep['id'])
    return render_template('ep.html', ep=ep, commenti = commenti)


# NUOVO PODCAST
@app.route('/podcasts/new', methods=['GET', 'POST'])
def new_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.tipo:
            podcast = request.form.to_dict()

            if podcast['descrizione'] == '':
                app.logger.error('La descrizione del podcast non può essere vuota!')
                flash('Podcast non creato correttamente: il podcast non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            if podcast['titolo'] == '':
                app.logger.error('Devi inserire un titolo')
                flash('Podcast non creato correttamente: devi inserire un titolo!', 'danger')
                return redirect(url_for('home'))

            pod_image = request.files['immagine']
            if pod_image:
                pod_image.save('static/' + pod_image.filename)
                podcast['immagine'] = pod_image.filename
            else:
                app.logger.error('É necessario inserire un\'immagine!')
                flash('Podcast non creato correttamente: devi inserire un\'immagine!', 'danger')
                return redirect(url_for('home'))
            
            id_utente = current_user.id
            podcast['autore_id'] = id_utente


            success = dao.add_podcast(podcast)
            if success:
                flash('Podcast creato correttamente', 'success')
            else:
                flash('Errore nella creazione del podcast: riprova!', 'danger')

    return redirect(url_for('home'))


# NUOVO EPISODIO
@app.route('/episodes/new', methods=['GET', 'POST'])
def new_episode():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.tipo:
            episode = request.form.to_dict()

            if episode['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash('Errore nella creazione dell\'episodio: il titolo non può essere vuoto!', 'danger')

            if episode['descrizione'] == '':
                app.logger.error('La descrizione non può essere vuota!')
                flash('Errore nella creazione dell\'episodio: la descrizione non può essere vuota!', 'danger')
                return redirect(url_for('single_pod', id=episode['podcast_id']))
            
            if episode['data'] == '':
                app.logger.error('Devi selezionare una data')
                flash('Errore nella creazione dell\'episodio: devi selezionare una data!', 'danger')
                return redirect(url_for('single_pod', id=episode['podcast_id']))

            if datetime.strptime(episode['data'], '%Y-%m-%d').date() < date.today():
                app.logger.error('Data errata')
                flash('Errore nella creazione dell\'episodio: la data deve maggiore o uguale a quella corrente', 'danger')
                return redirect(url_for('single_pod', id=episode['podcast_id']))

            file_audio = request.files['file_audio']
            if file_audio:
                file_audio.save('static/' + file_audio.filename)
                episode['file_audio'] = file_audio.filename
            else:
                app.logger.error('É necessario inserire un file audio!')
                flash('Errore nella creazione dell\'episodio: devi inserire un file audio', 'danger')
                return redirect(url_for('single_pod', id=episode['podcast_id']))

            id_utente = current_user.id
            episode['autore_id'] = id_utente

            success = dao.add_episode(episode)

            if success:
                flash('Episodio creato correttamente', 'success')
            else:
                flash('Errore nella creazione dell\'episodio: riprova!', 'danger')

    return redirect(url_for('single_pod', id=episode['podcast_id']))


# MODIFICA EPISODIO
@app.route('/episodes/modify', methods=['GET', 'POST'])
def modify_episode():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.tipo:
            episode = request.form.to_dict()

            if episode['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash('Errore durante la modifica dell\'episodio: il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('single_ep', id=episode['id']))


            if episode['descrizione'] == '':
                app.logger.error('La descrizione non può essere vuota!')
                flash('Errore durante la modifica dell\'episodio: la descrizione non può essere vuota!', 'danger')
                return redirect(url_for('single_ep', id=episode['id']))

            
            file_audio = request.files['file_audio']
            if file_audio:
                file_audio.save('static/' + file_audio.filename)
                episode['file_audio'] = file_audio.filename
            else:
                app.logger.error('É necessario inserire un file audio!')
                flash('Errore durante la modifica dell\'episodio: devi inserire un file audio.', 'danger')
                return redirect(url_for('single_ep', id=episode['id']))

            id_utente = current_user.id
            success = dao.modify_episode(episode, id_utente)

            if success:
                flash('Episodio modificato correttamente', 'success')
            else:
                flash('Errore durante la modifica dell\'episodio: riprova!', 'danger')

    return redirect(url_for('single_ep', id=episode['id']))


# MODIFICA PODCAST
@app.route('/podcasts/modify', methods=['GET', 'POST'])
def modify_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.tipo:
            podcast = request.form.to_dict()
            
            if podcast['titolo'] == '':
                app.logger.error('Il titolo del podcast non può essere vuoto!')
                flash('Errore durante la modifica del podcast: il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('single_pod', id=podcast['id']))
            
            pod_image = request.files['immagine']
            if pod_image:
                pod_image.save('static/' + pod_image.filename)
                podcast['immagine'] = pod_image.filename
            else:
                app.logger.error('Devi inserire un\'immagine!')
                flash('Errore durante la modifica del podcast: devi inserire un\'immagine!', 'danger')
                return redirect(url_for('single_pod', id=podcast['id']))
            
            if podcast['descrizione'] == '':
                app.logger.error('La descrizione del podcast non può essere vuota!')
                flash('Errore durante la modifica del podcast: la descrizione non può essere vuota!', 'danger')
                return redirect(url_for('single_pod', id=podcast['id']))
        
            
            id_utente = current_user.id
            podcast['autore_id'] = id_utente

            success = dao.modify_podcast(podcast, id_utente)

            if success:
                flash('Podcast modificato correttamente', 'success')
            else:
                flash('Errore durante la modifica del podcast: riprova!', 'danger')

    return redirect(url_for('single_pod', id=podcast['id']))

# ELIMINA EPISODIO
@app.route('/episodes/delete', methods=['POST'])
def delete_episode():
    if current_user.is_authenticated and current_user.tipo:
        episode = request.form.to_dict()

        success = dao.delete_episode(episode)

        if success:
            flash('L\'episodio è stato eliminato correttamente', 'success')
        else:
            flash('Errore durante l\'eliminazione dell\'episodio: riprova!', 'danger')

    return redirect(url_for('single_pod', id = episode['podcast_id']))


# ELIMINA PODCAST
@app.route('/podcasts/delete', methods=['POST'])
def delete_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.tipo:
            podcast = request.form.to_dict()

            success = dao.delete_podcast(podcast)

    if success:
        flash('Il podcast è stato eliminato correttamente', 'success')
    else:
        flash('Errore durante l\'eliminaione del podcast: riprova!', 'danger')

    return redirect(url_for('home'))


# LOAD USER
@login_manager.user_loader
def load_user(user_id):

    utente = dao.get_user_by_id(user_id)

    if utente is not None:
        user = User(id=utente['id'], nickname=utente['nickname'], password=utente['password'],
                    immagine_profilo=utente['immagine_profilo'], tipo=utente['tipo'])
    else:
        user = None

    return user

# LOGIN
@app.route('/accedi')
def login():
    return render_template('login.html')

@app.route('/accedi', methods=['POST'])
def login_pod():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = dao.get_user_by_nickname(nickname)

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    else:
        # Login_user
        new = User(id=user['id'], nickname=user['nickname'], password=user['password'],
                   immagine_profilo=user['immagine_profilo'], tipo=user['tipo'])
        # L'attuale user object viene passato a questo metodo
        login_user(new, True)

        return redirect(url_for('home'))

# REGISTRAZIONE UTENTE 
@app.route('/iscriviti')
def signup():
    return render_template('signup.html')


@app.route('/iscriviti', methods=['POST'])
def signup_pod():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    tipo = request.form.get('tipo')

    user_in_db = dao.get_user_by_nickname(nickname)

    if user_in_db:
        flash('C\'è già un utente registrato con questo nickname', 'danger')
        return redirect(url_for('signup'))
    else:
        img_profilo = ''
        usr_image = request.files['immagine_profilo']
        if usr_image:
            img = Image.open(usr_image)
            ext = usr_image.filename.split('.')[1]
            img.save('static/' + nickname.lower() + '.' + ext)
            img_profilo = nickname.lower() + '.' + ext

        new_user = {
            "nickname": nickname,
            # Salva le password nel server
            "password": generate_password_hash(password, method='sha256'),
            "immagine_profilo": img_profilo,
            "tipo": tipo
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione dell\'utente: riprova!', 'danger')

    return redirect(url_for('signup'))


# LOGOUT 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# SEGUI PODCAST
@app.route('/follow', methods=['POST'])
def add_follow():
    if request.method == 'POST':
        if current_user.is_authenticated:
            follow = request.form.to_dict()

            user_id = current_user.id
            follow['user_id'] = user_id
            
            user_in_follow = dao.check_follow(follow, user_id)
            if user_in_follow:
                flash('Segui già questo podcast!', 'danger')
            else: 
                success = dao.add_follow(follow, user_id)
                if success:
                    flash('Pocast seguito', 'success')
                else:
                    flash('Errore nel seguire il podcast: riprova!', 'danger')

    return redirect(url_for('single_pod', id=follow['podcast_id']))


# NUOVO COMMENTO
@app.route('/comments/new', methods=['POST'])
def new_comment():
    commento = request.form.to_dict()
    if current_user.is_authenticated:
        if commento['testo'] == '':
            app.logger.error('Il commento non può essere vuoto!')
            flash('Commento non creato correttamente: il commento non può essere vuoto!', 'danger')
            return redirect(url_for('single_ep', id=commento['episodio_id']))

        id_utente = current_user.id
        success = dao.add_comment(commento, id_utente)

        if success:
            flash('Commento creato correttamente', 'success')
        else:
            flash('Errore nella creazione del commento: riprova!', 'danger')

    return redirect(url_for('single_ep', id=commento['episodio_id']))


# ELIMINA COMMENTO
@app.route('/comments/delete', methods=['POST'])
def delete_comment():
    if current_user.is_authenticated:
        commento = request.form.to_dict()

        success = dao.delete_comment(commento)

        if success:
            flash('Commento eliminato correttamente', 'success')
        else:
            flash('Errore durante l\'eliminazione del commento: riprova!', 'danger')

    return redirect(url_for('single_ep', id=commento['episodio_id']))


# SMETTI DI SEGUIRE
@app.route('/unfollow', methods=['POST'])
def unfollow():
    if current_user.is_authenticated:
        follow = request.form.to_dict()

        id_utente = current_user.id
        success = dao.delete_follow(follow, id_utente)

        if success:
            flash('Non segui più questo podcast', 'success')
        else:
            flash('Errore durante la cancellazione del follow: riprova!', 'danger')

    return redirect(url_for('single_pod', id=follow['podcast_id']))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)



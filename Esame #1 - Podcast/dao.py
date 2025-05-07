import sqlite3
import datetime

# PRENDE LA LISTA DI TUTTI I PODCAST
def get_podcasts():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT podcasts.id, podcasts.titolo, podcasts.immagine, podcasts.descrizione, podcasts.categoria, podcasts.lista_episodi, users.nickname FROM podcasts LEFT JOIN users ON podcasts.autore_id = users.id'
    cursor.execute(sql)
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts


# PRENDE UN PODCAST CON UN CERTO ID
def get_pod(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT podcasts.id, podcasts.titolo, podcasts.immagine, podcasts.descrizione, podcasts.categoria, podcasts.autore_id, podcasts.lista_episodi, users.nickname FROM podcasts LEFT JOIN users ON podcasts.autore_id = users.id WHERE podcasts.id = ?'
    cursor.execute(sql, (id,))
    pod = cursor.fetchone()

    cursor.close()
    conn.close()

    return pod


# PRENDE UN EPISODIO CON UN CERTO ID
def get_ep(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT episodi.id, episodi.titolo, episodi.descrizione, episodi.autore_id, episodi.data, episodi.file_audio, episodi.podcast_id, podcasts.immagine, podcasts.titolo AS titolo_pod FROM episodi LEFT JOIN podcasts ON episodi.podcast_id = podcasts.id WHERE episodi.id = ?'
    cursor.execute(sql, (id,))
    ep = cursor.fetchone()

    cursor.close()
    conn.close()

    return ep


# PRENDE LA LISTA DI EPISODI APPARTENENTI A UN CERTO PODCAST
# L'argomento della funzione (id) serve per identificare il podcast di appartenenza dell'episodio
def get_episodes(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT episodi.id, episodi.titolo, episodi.descrizione, episodi.data, episodi.file_audio FROM episodi LEFT JOIN users ON episodi.autore_id = users.id WHERE episodi.podcast_id = ? ORDER BY data ASC'
    cursor.execute(sql, (id,))
    episodi = cursor.fetchall()

    cursor.close()
    conn.close()

    return episodi


# AGGIUNGE UN PODCAST
def add_podcast(podcast):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO podcasts (titolo, immagine, descrizione, categoria, autore_id, lista_episodi) VALUES(?,?,?,?,?,?)'
    cursor.execute(sql, (podcast['titolo'], podcast['immagine'], podcast['descrizione'], podcast['categoria'], podcast['autore_id'], podcast['lista_episodi']))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# AGGIUNGE UN EPISODIO
def add_episode(episode):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    #x = datetime.datetime.now()
    #x.strftime("%Y-%m-%d")

    sql = 'INSERT INTO episodi (titolo, descrizione, data, file_audio, podcast_id, autore_id) VALUES(?,?,?,?,?,?)'
    cursor.execute(sql, (episode['titolo'], episode['descrizione'], episode['data'], episode['file_audio'], episode['podcast_id'], episode['autore_id']))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# ELIMINA UN EPISODIO
def delete_episode(episode):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'DELETE FROM episodi WHERE id=?'
    cursor.execute(sql, (episode['id'], ))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# MODIFICA UN EPISODIO
def modify_episode(episode, autore_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'UPDATE episodi SET titolo=?, descrizione=?, file_audio=?, autore_id=? WHERE id=?'
    cursor.execute(sql, (episode['titolo'], episode['descrizione'], episode['file_audio'], autore_id, episode['id']))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# MODIFICA UN PODCAST
def modify_podcast(podcast, autore_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'UPDATE podcasts SET titolo=?, immagine=?, descrizione=?, categoria=?, autore_id=? WHERE id=?'
    cursor.execute(sql, (podcast['titolo'], podcast['immagine'], podcast['descrizione'], podcast['categoria'], autore_id, podcast['id']))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# ELIMINA UN PODCAST
def delete_podcast(podcast):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'DELETE FROM podcasts WHERE id=?'
    cursor.execute(sql, (podcast['id'], ))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# PRENDE UN UTENTE CON UN CERTO NICKNAME
def get_user_by_nickname(nickname):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE nickname = ?'
    cursor.execute(sql, (nickname,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# PRENDE UN CERTO UTENTE CHE SEGUE UN CERTO PODCAST
def get_user_in_follow(user_id, podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM follow WHERE user_id= ? AND podcast_id = ?'
    cursor.execute(sql, (user_id, podcast_id))
    user_in_follow = cursor.fetchone()

    cursor.close()
    conn.close()

    return user_in_follow


# PRENDE UN UTENTE DATO IL SUO ID
def get_user_by_id(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# AGGIUNGE UN UTENTE
def add_user(user):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO users(nickname,password,immagine_profilo, tipo) VALUES(?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['nickname'], user['password'], user['immagine_profilo'], user['tipo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# AGGIUNGE UN FOLLOWER A UN CERTO PODCAST
def add_follow(follow, user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'INSERT INTO follow (podcast_id, user_id) VALUES(?,?)'
    cursor.execute(sql, (follow['podcast_id'], user_id))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# CONTROLLA SE UN UTENTE SEGUE GIA' UN PODCAST O NO
def check_follow(follow, user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM follow WHERE podcast_id = ? AND user_id =?'
    cursor.execute(sql, (follow['podcast_id'], user_id))
    user_in_follow = cursor.fetchone()

    cursor.close()
    conn.close()

    return user_in_follow


# PRENDE I FOLLOW DI UN UTENTE (quindi i podcast che segue)
def get_follow (user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT follow.podcast_id, follow.user_id, podcasts.immagine, podcasts.titolo, podcasts.descrizione, users.nickname FROM follow LEFT JOIN podcasts ON follow.podcast_id = podcasts.id LEFT JOIN users ON podcasts.autore_id = users.id WHERE user_id =?'
    cursor.execute(sql, (user_id, ))

    follow = cursor.fetchall()

    cursor.close()
    conn.close()

    return follow


# PRENDE I COMMENTI DI UN EPISODIO
def get_comments(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT commenti.id, commenti.data_pubblicazione, commenti.testo, users.nickname, commenti.user_id, users.immagine_profilo FROM commenti LEFT JOIN users ON commenti.user_id = users.id WHERE commenti.episodio_id = ?'
    cursor.execute(sql, (id,))
    commenti = cursor.fetchall()

    cursor.close()
    conn.close()

    return commenti

# AGGIUNGE UN COMMENTO
def add_comment(commento, id_utente):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'INSERT INTO commenti(data_pubblicazione,testo,user_id,episodio_id) VALUES(?,?,?,?)'
    cursor.execute(sql, (x.strftime("%Y-%m-%d"), commento['testo'], id_utente, commento['episodio_id']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# ELIMINA UN COMMENTO
def delete_comment(commento):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'DELETE FROM commenti WHERE id=?'
    cursor.execute(sql, (commento['id'], ))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# UTENTE SMETTE DI SEGUIRE UN CERTO PODCAST
def delete_follow(follow, user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'DELETE FROM follow WHERE podcast_id=? AND user_id = ?'
    cursor.execute(sql, (follow['podcast_id'], user_id))
   
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# LISTA DEGLI EPISODI DI UN PODCAST VIENE MODIFICATA
def modify_lista_episodi(podcast, episodi):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    lista = ""
    for ep in episodi:
        lista = lista + " " + ep['titolo']
    sql = 'UPDATE podcasts SET lista_episodi = ? WHERE id=?'
    cursor.execute(sql, (lista, podcast['id']))
   
    try:
        conn.commit()
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return


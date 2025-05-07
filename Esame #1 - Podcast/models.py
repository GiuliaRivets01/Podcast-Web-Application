from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id, nickname, password, immagine_profilo, tipo):
        self.id = id
        self.nickname = nickname
        self.password = password
        self.immagine_profilo = immagine_profilo
        self.tipo = tipo
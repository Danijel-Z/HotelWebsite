from datetime import datetime
from Pythonhtml import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Kund.query.get(int(user_id))


class Kund(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Namn = db.Column(db.String(30), unique=False, nullable=False)
    Personnummer = db.Column(db.String(30), unique=False, nullable=False)
    Telefonnummer = db.Column(db.String(50), unique=False, nullable=False)
    Mail = db.Column(db.String(50), unique=False, nullable=False)
    Lösenord = db.Column(db.String(50), unique=False, nullable=False)

    Bokningar = db.relationship("Bokning", backref="kund", lazy=True)

    def __init__(self, namn: str, personnummer: str, telefonnummer: str, mail: str, lösenord: str):
        super().__init__()
        self.Namn = namn
        self.Personnummer = personnummer
        self.Telefonnummer = telefonnummer
        self.Mail = mail
        self.Lösenord = lösenord


class Rum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TypAvRum = db.Column(db.String(30), unique=False, nullable=False)
    AntalPersoner = db.Column(db.Integer, unique=False, nullable=False)
    Pris = db.Column(db.Integer, unique=False, nullable=False)
    Area = db.Column(db.Integer, unique=False, nullable=False)
    ExtraSäng = db.Column(db.Integer, unique=False, nullable=True)

    Bokningar = db.relationship("Bokning", backref="rum", lazy=True)

    def __init__(self, TypAvRum: str, antalPersoner: int, rumPris: int, rumArea: int, extrasäng: int = 0):
        super().__init__()
        self.TypAvRum = TypAvRum
        self.AntalPersoner = antalPersoner
        self.Pris = rumPris
        self.Area = rumArea
        self.ExtraSäng = extrasäng


class Bokning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StartDatum = db.Column(db.DateTime, unique=False,
                           nullable=False, default=datetime.utcnow)
    SlutDatum = db.Column(db.DateTime, unique=False, nullable=False)
    Kund_id = db.Column(db.Integer, db.ForeignKey("kund.id"), nullable=False)
    Rum_id = db.Column(db.Integer, db.ForeignKey("rum.id"), nullable=False)
    Fakturor = db.relationship("Faktura", backref="bokning", lazy=True)

    def __init__(self, startdatum: str, slutdatum: str, kund_id: int, rum_id: int):
        super().__init__()
        self.StartDatum = startdatum
        self.SlutDatum = slutdatum
        self.Kund_id = kund_id
        self.Rum_id = rum_id


class Faktura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StartDatum = db.Column(db.DateTime, unique=False,
                           nullable=False, default=datetime.utcnow)
    FörfalloDatum = db.Column(db.DateTime, unique=False, nullable=False)
    TotalPris = db.Column(db.Integer, unique=False, nullable=False)
    Betalning = db.Column(db.Boolean, unique=False,
                          nullable=False, default=False)
    Boknings_id = db.Column(
        db.Integer, db.ForeignKey("bokning.id"), nullable=False)

    def __init__(self, startdatum: str, förfallodatum: str, bokningensTotalaPris: int, bokning_id: int):
        super().__init__()
        self.StartDatum = startdatum
        self.FörfalloDatum = förfallodatum
        self.TotalPris = bokningensTotalaPris
        self.Boknings_id = bokning_id
        self.Betalning = False


db.create_all()

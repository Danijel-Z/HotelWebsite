from datetime import datetime, timedelta, date
from flask_wtf import FlaskForm
from sqlalchemy.util.langhelpers import NoneType
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Pythonhtml.models import Kund, Rum, Bokning
from flask_login import current_user
from Pythonhtml import db


class RegistreringForm(FlaskForm):

    personnummer = StringField("Personnummer", validators=[
                               DataRequired(), Length(min=10, max=12)])

    användarnamn = StringField("Användarnamn", validators=[
                               DataRequired(), Length(min=2, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    mobilnummer = StringField("Mobilnummer", validators=[
                              DataRequired(), Length(min=10, max=20)])

    lösenord = PasswordField("Lösenord", validators=[DataRequired()])

    konfirmera_lösenord = PasswordField(
        "Bekräfta lösenord", validators=[DataRequired(), EqualTo("lösenord", message="Lösenord måste matcha")])

    submit = SubmitField("Registrera")

    def validate_personnummer(self, personnummer: StringField):
        if personnummer.data.isnumeric():
            kund = Kund.query.filter_by(Personnummer=personnummer.data).first()
            if kund:
                raise ValidationError(f"Du är redan kund hos oss.")

        else:
            raise ValidationError("Fel inmatad personnummer.")


class LoggaInForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    lösenord = PasswordField("Lösenord", validators=[DataRequired()])
    komihågmig = BooleanField("Kom ihåg mig")
    submit = SubmitField("Logga in")


class UppdateraKontotForm(FlaskForm):
    användarnamn = StringField('Användarnamn',
                               validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    mobilnummer = StringField("Mobilnummer", validators=[
                              DataRequired(), Length(min=10, max=20)])

    submit = SubmitField('Uppdatera infon')

    def validate_användarnamn(self, användarnamn):
        if användarnamn.data != current_user.Namn:
            kund = Kund.query.filter_by(Namn=användarnamn.data).first()
            if kund:
                raise ValidationError(
                    'Detta användarnamn är taget. Vänligen välj ett annat.')

    def validate_email(self, email):
        if email.data != current_user.Mail:
            kund = Kund.query.filter_by(Mail=email.data).first()
            if kund:
                raise ValidationError(
                    'Detta mejl är taget. Vänligen välj ett annat.')


class BokaRumForm(FlaskForm):
    startdatum = DateTimeField('Startdatum',
                               validators=[DataRequired(message="Fel inmatad datum")], format="%Y-%m-%d")
    slutdatum = DateTimeField('Slutdatum',
                              validators=[DataRequired(message="Fel inmatad datum")], format="%Y-%m-%d")

    rum = SelectField("Rum", validators=[DataRequired()], choices=[("1", "Rum 1: Enkelrum/1 Person/400kr/13m2"), ("2", "Rum 2: Enkelrum/2 Personer/700kr/16m2"),
                      ("3", "Rum 3: Dubbelrum/2 Personer/1200kr/20m2"), ("4", "Rum 4: Dubbelrum/2 Personer/1500kr/25m2/+1 Extra säng")])

    submit = SubmitField('Boka rum')

    def validate_slutdatum(form, slutdatum):
        if type(slutdatum.data) != NoneType and type(form.startdatum.data) != NoneType:
            SistaDatumManFårBoka = datetime.now() + timedelta(days=14)

            if slutdatum.data < form.startdatum.data:
                raise ValidationError(
                    "Slutdatumet får ej vara tidigare än startdatumet.")
            if slutdatum.data > SistaDatumManFårBoka:
                raise ValidationError(
                    f"Slutdatumet får ej vara efter {SistaDatumManFårBoka.strftime('%Y-%m-%d')}")

    def validate_startdatum(form, startdatum: datetime):
        if type(startdatum.data) != NoneType and type(form.slutdatum.data) != NoneType:
            if startdatum.data.date() < date.today():
                raise ValidationError(
                    "Startdatumet får ej vara tidigare än dagensdatum")

    def validate_rum(form, rum):
        if type(form.startdatum.data) != NoneType and type(form.slutdatum.data) != NoneType:
            SistaDatumManFårBoka = datetime.now() + timedelta(days=14)
            upptagnaBokningar_påvaltRum = db.session.query(Bokning).filter(
                Bokning.StartDatum >= datetime.now(), Bokning.SlutDatum <= SistaDatumManFårBoka, Bokning.Rum_id == int(rum.data)).all()

            if upptagnaBokningar_påvaltRum:
                for upptagenBokning in upptagnaBokningar_påvaltRum:
                    if form.startdatum.data >= upptagenBokning.StartDatum and form.startdatum.data <= upptagenBokning.SlutDatum:
                        raise ValidationError(
                            f"Denna rum är upptaget vid angivna startdatum. Vänligen välj ett annat datum.")

    # def validate_email(self, email):
    #     if email.data != current_user.Mail:
    #         kund = Kund.query.filter_by(Mail=email.data).first()
    #         if kund:
    #             raise ValidationError(
    #                 'Detta mejl är taget. Vänligen välj ett annat.')

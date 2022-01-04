from datetime import datetime, timedelta
from flask import render_template, request, session, url_for, flash, redirect
from Pythonhtml import app, db
from Pythonhtml.forms import RegistreringForm, LoggaInForm, UppdateraKontotForm, BokaRumForm
from Pythonhtml.models import Kund, Faktura, Rum, Bokning
from flask_login import login_user, current_user, logout_user, login_required


def kollaOmFakturanÄrBetalt(bokning: Bokning):
    pass


def getLengthFromList(lista):
    return len(lista)


def getförfallodatum(startdatum: datetime):
    förfallodatum = startdatum + timedelta(days=10)
    förfallodatum = datetime.strftime(förfallodatum, "%Y-%m-%d")
    return förfallodatum


def visaLedigaRumUnderValtDatum(valtDatum: str) -> list[Rum]:
    listaMedLedigaRum = []
    listaMedUpptagnaRum = []
    alla_bokningar = Bokning.query.all()

    for bokning in alla_bokningar:
        if valtDatum == bokning.StartDatum.strftime("%Y-%m-%d"):
            hittaRum = Rum.query.filter_by(id=bokning.Rum_id).first()
            if hittaRum:
                listaMedUpptagnaRum.append(hittaRum)

    if len(listaMedUpptagnaRum) != 0:
        for rum in Rum.query.all():
            if rum not in listaMedUpptagnaRum:
                listaMedLedigaRum.append(rum)
        return listaMedLedigaRum
    return ""


def visaLedigaRumUnderVissDatum(startdatum: str, slutdatum: str) -> list:
    listaMedUpptagnaRum = []
    alla_upptagna_bokningar = db.session.query(Bokning).filter(
        Bokning.StartDatum >= startdatum, Bokning.SlutDatum <= slutdatum).all()

    if alla_upptagna_bokningar:
        for bokning in alla_upptagna_bokningar:
            upptaget_rum = db.session.query(
                Rum).filter_by(id=bokning.Rum_id).first()
            if upptaget_rum:
                listaMedUpptagnaRum.append(upptaget_rum.id)

    alla_lediga_rum = db.session.query(Rum).filter(
        Rum.id.not_in(listaMedUpptagnaRum)).all()

    return alla_lediga_rum


def getValues(fromSession: dict) -> list:
    listaMedValues = fromSession.values()
    return listaMedValues


@app.route('/')
def index():
    return render_template('hotel.html')


@app.route('/admin')
@login_required
def admin():
    if current_user.Namn == "admin" and current_user.Mail == "admin@gmail.com":
        fakturor = Faktura.query.filter(
            Faktura.Betalning == 0, Faktura.FörfalloDatum).all()
        for faktura in fakturor:
            if faktura.FörfalloDatum < datetime.now() + timedelta(days=10):
                bokning = Bokning.query.filter(
                    Bokning.id == faktura.Boknings_id).first()
                if bokning:
                    db.session.delete(faktura)
                    db.session.delete(bokning)
                    db.session.commit()
        return render_template("rum.html")
    flash("Du har inte tillgång till adminverktyg", "failure")
    return redirect(url_for("hem"))


@app.route("/nyrum", methods=["POST"])
def skaparum():
    if request.method == "POST":
        TypAvRum = request.form["TypAvRum"]
        AntalPersoner = request.form["AntalPersoner"]
        Area = request.form["Area"]
        Pris = request.form["Pris"]
        ExtraSäng = request.form["ExtraSäng"]
        rum = Rum(TypAvRum, AntalPersoner, Pris, Area, ExtraSäng)
        db.session.add(rum)
        db.session.commit()
        flash("Rummet har skapats!", "success")
        return redirect(url_for("admin"))
    flash("Det gick inte att skapa", "failure")
    return render_template("hotel.html")


@app.route("/templates/bokning.html", methods=["GET", "POST"])
@login_required
def bokning():
    form = BokaRumForm()
    if form.validate_on_submit():
        #print(form.startdatum.data, form.slutdatum.data, form.rum.data)
        startdatum = datetime.strftime(form.startdatum.data, "%Y-%m-%d")
        slutdatum = datetime.strftime(form.slutdatum.data, "%Y-%m-%d")
        valtRumID = int(form.rum.data)

        kund = current_user
        bokning = Bokning(startdatum, slutdatum, int(kund.id), valtRumID)
        db.session.add(bokning)
        # Commita eller inte?
        db.session.commit()

        rum = Rum.query.filter_by(id=valtRumID).first()
        förfallodatum = getförfallodatum(form.startdatum.data)
        faktura = Faktura(startdatum, förfallodatum, rum.Pris, bokning.id)
        db.session.add(faktura)
        db.session.commit()

        flash("Din rumbokning har skapats.", "success")
        return redirect(url_for('bokning'))
    bokningStartDatum = datetime.now()
    bokningSlutDatum = bokningStartDatum + timedelta(days=14)
    delta = timedelta(days=1)
    dictMedLedigaDatum = {}
    for rumID in range(1, 5):
        Rummetsupptagnaboknignar = db.session.query(Bokning).filter(
            Bokning.StartDatum >= bokningStartDatum.strftime("%Y-%m-%d"), Bokning.SlutDatum <= bokningSlutDatum.strftime("%Y-%m-%d"), Bokning.Rum_id == rumID).all()
        ListaMedUpptagnaDatum = []
        for bokning in Rummetsupptagnaboknignar:
            while bokning.StartDatum <= bokning.SlutDatum:
                ListaMedUpptagnaDatum.append(
                    bokning.StartDatum.strftime("%Y-%m-%d"))
                bokning.StartDatum += delta

        ListaMedLedigaDatum = []
        while bokningStartDatum.strftime("%Y-%m-%d") <= bokningSlutDatum.strftime("%Y-%m-%d"):
            if bokningStartDatum.strftime("%Y-%m-%d") not in ListaMedUpptagnaDatum:
                ListaMedLedigaDatum.append(bokningStartDatum)
                bokningStartDatum += delta
            else:
                bokningStartDatum += delta

        bokningStartDatum = datetime.now()
        dictMedLedigaDatum[rumID] = ListaMedLedigaDatum

    bokningStartDatum = datetime.now()
    allaUpptagnabokningar = db.session.query(Bokning).filter(
        Bokning.StartDatum >= bokningStartDatum, Bokning.SlutDatum <= bokningSlutDatum).all()

    return render_template("bokning.html", title="Boka Rum", form=form, allaupptagnabokningar=allaUpptagnabokningar, bokningstartdatum=bokningStartDatum, bokningslutdatum=bokningSlutDatum, dictmedledigadatum=dictMedLedigaDatum, getlength=getLengthFromList)


@app.route("/templates/text.html")
def omWaikiki():
    return render_template('text.html')


@app.route("/registrera", methods=["GET", "POST"])
def registrera():
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    form = RegistreringForm()
    if form.validate_on_submit():
        kund = Kund(form.användarnamn.data, form.personnummer.data,
                    form.mobilnummer.data, form.email.data, form.lösenord.data)
        db.session.add(kund)
        db.session.commit()
        flash(
            f"Kontot för {form.användarnamn.data} har skapats! Du kan logga in nu.", "success")
        return redirect(url_for("loggain"))
    return render_template("registrera.html", title="Registrera", form=form)


@app.route("/loggaIn", methods=["GET", "POST"])
def loggain():
    if current_user.is_authenticated:
        return redirect(url_for("hem"))
    form = LoggaInForm()
    if form.validate_on_submit():
        kund = Kund.query.filter_by(
            Mail=form.email.data).first()
        if kund and kund.Lösenord == form.lösenord.data:
            login_user(kund, remember=form.komihågmig.data)
            nästa_sida = request.args.get("next")
            return redirect(nästa_sida) if nästa_sida else redirect(url_for("hem"))
        else:
            flash(
                "Det gick inte att logga in. Vänligen kolla om du har mattat in rätt mail/lösenord.", "failure")
    return render_template("loggain.html", title="Logga In", form=form)


@app.route("/loggaUt")
def loggaut():
    logout_user()
    return redirect(url_for("hem"))


@app.route("/templates/minkonto.html", methods=["GET", "POST"])
@login_required
def minKonto():
    form = UppdateraKontotForm()
    if form.validate_on_submit():
        current_user.Namn = form.användarnamn.data
        current_user.Mail = form.email.data
        current_user.Telefonnummer = form.mobilnummer.data
        db.session.commit()
        flash("Ditt konto information har uppdaterats!", "success")
        return redirect(url_for("minKonto"))
    elif request.method == "GET":
        form.användarnamn.data = current_user.Namn
        form.email.data = current_user.Mail
        form.mobilnummer.data = current_user.Telefonnummer
    return render_template("minkonto.html", title="Min konto", form=form)


@app.route("/templates/minbokning.html")
@login_required
def minbokning():
    kund = db.session.query(Bokning).join(
        Rum).filter(Bokning.Kund_id == current_user.id).all()
    # print(kund[0].Fakturor[0].FörfalloDatum)
    return render_template('minbokning.html', kund=kund)


@app.route("/templates/minbokning.html/<int:rum_id>/<startDatum>", methods=["GET", "POST"])
@login_required
def hanterabokning(rum_id, startDatum):
    bokning = db.session.query(Bokning).join(
        Rum).filter(Bokning.Kund_id == current_user.id, Bokning.Rum_id == rum_id, Bokning.StartDatum == startDatum).first()
    if bokning:
        form = BokaRumForm()
        if form.validate_on_submit():
            startdatum = datetime.strftime(form.startdatum.data, "%Y-%m-%d")
            slutdatum = datetime.strftime(form.slutdatum.data, "%Y-%m-%d")
            valtRumID = int(form.rum.data)
            bokning.StartDatum = startdatum
            bokning.SlutDatum = slutdatum
            bokning.Rum_id = valtRumID
            db.session.commit()
            flash("Din bokning har ändrats.", "success")
        return render_template("hanterabokning.html", bokning=bokning, form=form)
    b = current_user
    flash("Hittade inte valda rummet", "failure")
    return redirect(url_for("minbokning"))


@app.route("/templates/minbokning.html/<int:rum_id>/<startDatum>/raderabokning", methods=["GET", "POST"])
@login_required
def raderabokning(rum_id, startDatum):
    try:
        hittabokning = db.session.query(Bokning).join(
            Rum).filter(Bokning.Kund_id == current_user.id, Bokning.Rum_id == rum_id, Bokning.StartDatum == startDatum).first()
        if hittabokning:
            faktura = Faktura.query.filter(
                Faktura.Boknings_id == hittabokning.id).first()
            if faktura:
                db.session.delete(faktura)
            db.session.delete(hittabokning)
            db.session.commit()
            flash("Din bokning har avbokats.", "success")
            return redirect(url_for('minbokning'))
    except:
        flash("Något blev fel, bokningen finns inte med i vår system", "failure")
        return redirect(url_for('hanterabokning', rum_id=rum_id, startDatum=startDatum))


@app.route("/templates/minbokning.html/<int:rum_id>/<startDatum>/faktura", methods=["GET", "POST"])
def betaladfaktura(rum_id, startDatum):
    bokning = Bokning.query.filter(Bokning.Rum_id == rum_id, Bokning.StartDatum ==
                                   startDatum, Bokning.Kund_id == current_user.id).first()
    faktura = Faktura.query.filter(Faktura.Boknings_id == bokning.id).first()
    if faktura.Betalning == False:
        faktura.Betalning = True
        db.session.commit()
        flash("Din faktura är nu betalt", "success")
    else:
        flash("Din bokning är redan betalad", "success")
    return redirect(url_for('minbokning'))


@app.route("/templates/hotel.html")
def hem():
    return render_template('hotel.html')


# @app.route("/submit", methods=["POST"])
# def submit():
#     if request.method == "POST":
#         startdatum = request.form["startdatum"]
#         slutdatum = request.form["slutdatum"]
#         valtRumID = request.form["rum"]
#         kund = current_user
#         bokning = Bokning(startdatum, slutdatum, int(kund.id), int(valtRumID))
#         db.session.add(bokning)
#         db.session.commit()

#         rum = Rum.query.filter_by(id=int(valtRumID)).first()
#         förfallodatum = datetime.strptime(
#             startdatum, "%Y-%m-%d") + timedelta(days=10)
#         förfallodatum = datetime.strftime(förfallodatum, "%Y-%m-%d")
#         faktura = Faktura(startdatum, förfallodatum, rum.Pris, bokning.id)
#         db.session.add(faktura)
#         db.session.commit()
#         # FotbollVm = Exempel.query.all()
#         # for table in FotbollVm:
#         #     print(table.data)

#         return render_template("bokning.html", message="Din bokning har sparats!")


# @app.route("/loggain", methods=["POST", "GET"])
# def loggaIn():
#     if request.method == "POST":
#         användare = request.form["personnummer"]
#         kund = Kund.query.filter_by(Personnummer=användare).first()
#         if kund:
#             session["användare"] = [kund.Namn,
#                                     kund.Personnummer, kund.Telefonnummer, kund.Mail]
#             return redirect(url_for("minKonto"))

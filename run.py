from Pythonhtml import app

# db.drop_all()
# db.create_all()


# class RumBokning(db.Model):
#     Id = db.Column(db.Integer, primary_key=True)
#     Rum_ID =  db.Column(db.Integer, db.ForeignKey("rum.Id"), nullable=False)
#     Bokning_ID = db.Column(db.Integer, db.ForeignKey("bokning.Id"), nullable=False)

# class RumFaktura(db.Model):
#     Id = db.Column(db.Integer, primary_key=True)
#     Rum_ID = db.Column(db.Integer, db.ForeignKey("rum.Id"), nullable=False)
#     Faktura_ID = db.Column(db.Integer, db.ForeignKey("faktura.Id"), nullable=False)

# hotel = True
# while hotel:
#     print("""
#         1. Registrera Kund
#         2. Skapa antal rum
#         3. Boka ett rum
#         4. Avsluta
#         """)
#     val = input("Välj ett av valen")
#     if val == "4":
#         hotel = False
#     elif val == "1":
#         kund = Kund()
#         kund.Namn = input("Ange Namn: ")
#         kund.Personnummer = input("Personnummer: ")
#         kund.Telefonnummer = input("Telefonnummer: ")
#         kund.Mail = input("Ditt mail: ")
#         db.session.add(kund)
#         db.session.commit()
#     elif val == "2":
#         selRum = int("Ange antal rum: ")
#         for _ in range(selRum):
#             rum = Rum()
#             rum.TypAvRum = input("Ange typ av rum: ")
#             rum.Pris = input("Ange pris: ")
#             rum.Area = input("Ange rumets area: ")
#             rum.AntalPersoner = input("Max antal personer: ")
#             db.session.add(rum)
#             db.session.commit()
#     elif val == "3":
#         boka = Bokning()
#         boka.StartDatum = "2021-10-04"
#         boka.SlutDatum = "2021-12-05"
#         perNummer = input("Ange personnummer: ")
#         hittaKund = Kund.query.filter_by(Personnummer=perNummer).first()
#         if hittaKund:
#             boka.Kund_ID = hittaKund.Id
#             db.session.add(boka)
#             db.session.commit()
#     elif val == "5":
#         for kund in Kund.query.all():
#             print(f"{kund.Namn} {kund.Id} {kund.Personnummer}")


if __name__ == "__main__":
    # index()
    app.run(host="127.0.0.1", port=5000, debug=True)

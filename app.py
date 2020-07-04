from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://bngfsyvnjqcepp:211c9372dba7764f68b5c77839d5e2392037db77875e3e43fcab7f9468e98630@ec2-3-231-46-238.compute-1.amazonaws.com:5432/d4b8i2lkij5b74")
db = scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)


@app.route("/")
def index():
    flights=db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/a",methods=["POST"])
def book():
    name=request.form.get("y")

    try:
        flight_id=int(request.form.get("x"))
    except ValueError:
        return render_template("success.html",m="Please select flight")

    if name =="":
        return render_template("success.html",m="Please enter the name")

    if db.execute("SELECT * FROM flights WHERE id=:s",{"s":flight_id}).rowcount==0:
        return render_template("success.html",m="No such flight with that id.")

    if db.execute("SELECT * FROM passengers WHERE flight_id=:s AND name=:n",{"s":flight_id, "n":name}).rowcount!=0:
        return render_template("success.html",m="You have already booked before")
    db.execute("INSERT INTO passengers (name,flight_id) VALUES(:n,:f)",{"n":name, "f":flight_id})
    db.commit()

    return render_template("success.html",m="Succeed!")

@app.route("/flight")
def flights():
    flights=db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html",flights=flights)

@app.route("/flight/<int:d>")
def flight(d):
    flight=db.execute("SELECT * FROM flights WHERE id=:d",{"d":d}).fetchone()
    names=db.execute("SELECT name FROM passengers WHERE flight_id=:d",{"d":d}).fetchall()
    if names is None:
        return render_template("success.html",m="No passengers")
    return render_template("flight.html", names=names, flight=flight)

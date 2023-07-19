from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/contact')
def contact():
   return render_template("contact.html")

@app.route('/about')
def about():
   return render_template("about.html")

@app.route('/all_champions')
def all_champions():
   conn = sqlite3.connect('OPGG.db')
   cur = conn.cursor()
   cur.execute('SELECT * FROM Champions')
   results = cur.fetchall()
   return render_template('all_champions.html', results=results)

@app.route('/champion/<int:id>')
def pizza(id):
   conn=sqlite3.connect('OPGG.db')
   cur = conn.cursor()
   cur.execute('SELECT * FROM Champions')
   pizza = cur.fetchone()
   
   cur.execute("SELECT name FROM Base WHERE id=?",(pizza[4],))
   base=cur.fetchone()
   
   cur.execute("SELECT name FROM Toppings WHERE id IN(SELECT tid FROM PizzaToppings WHERE pid=?)",(id,))
   toppings=cur.fetchall()

   
   return render_template("pizza.html", pizza=pizza, base=base, toppings=toppings)


if __name__ == "__main__":
    app.run(debug = True)


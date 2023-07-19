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
def viewchampion(id):
   conn=sqlite3.connect('OPGG.db')
   cur = conn.cursor()
  # cur.execute('SELECT * FROM Champions')
  # pizza = cur.fetchone()

   cur.execute("SELECT item_name FROM Items WHERE item_id IN(SELECT iid FROM champion_item WHERE cid=?)",(id,))
   itemdata=cur.fetchall()
   
   cur.execute("SELECT * FROM Champions WHERE champion_id=?",(id,))
   champdata=cur.fetchone()

   
   return render_template("champion.html", champdata=champdata,itemdata=itemdata)


if __name__ == "__main__":
    app.run(debug = True)


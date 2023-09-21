from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)
#directs to home page
@app.route('/')
def home():
    return render_template("home.html")
#directs to contact page
@app.route('/contact')
def contact():
   return render_template("contact.html")
#directs to about page
@app.route('/about')
def about():
   return render_template("about.html")

#directs to all_champion page
@app.route('/all_champions')
def all_champions():
   conn = sqlite3.connect('OPGG.db')
   cur = conn.cursor()
#selects all champions from the database
   cur.execute('SELECT * FROM Champions')
   results = cur.fetchall()
   return render_template('all_champions.html', results=results)

@app.route('/chatbox')
def chatbox():
    conn = sqlite3.connect('OPGG.db')
    cur = conn.cursor()
#select info from chatbox database
    cur.execute("SELECT message_id, name, message_content FROM Chatbox")
    messages = cur.fetchall()

    conn.close()
    return render_template('chatbox.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    message_content = request.form.get('message_content')
    conn = sqlite3.connect('OPGG.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO Chatbox (name, message_content) VALUES (?, ?)", (name, message_content))
    conn.commit()
    conn.close()
    
    return redirect('/chatbox')

#directs to all_item page
@app.route('/all_items')
def all_items():
   conn = sqlite3.connect('OPGG.db')
   cur = conn.cursor()
#selects all items from the database
   cur.execute('SELECT * FROM Items')
   results = cur.fetchall()
   return render_template('all_items.html', itemdata=results)

#item page in items/id format
@app.route('/items/<id>')
def viewitem(id):
   conn=sqlite3.connect('OPGG.db')
   cur = conn.cursor()
   cur.execute("SELECT * FROM Items WHERE item_id=?",(id,))
   itemdata=cur.fetchone()
   return render_template("items.html",itemdata=itemdata)
#champion page in champion/id format
@app.route('/champion/<id>')
def viewchampion(id):
   conn=sqlite3.connect('OPGG.db')
   cur = conn.cursor()

   cur.execute("SELECT item_name,item_id FROM Items WHERE item_id IN(SELECT iid FROM champion_item WHERE cid=?)",(id,))
   itemdata=cur.fetchall()
   
   cur.execute("SELECT * FROM Champions WHERE champion_id=?",(id,))
   champdata=cur.fetchone()



   
   return render_template("champion.html", champdata=champdata,itemdata=itemdata)
   


if __name__ == "__main__":
    app.run(debug = True)


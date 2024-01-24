from flask import Flask
from flask import render_template 
from flask import request

import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/enternew")
def datacar():
    return render_template("datacar.html")

@app.route("/addrec", methods = ['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm    = request.form['nm']
            tahun = request.form['tahun']
            warna = request.form['warna']
            harga = request.form['harga']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO datacar (name, tahun, warna, harga) VALUES (?,?,?,?)", (nm, tahun, warna, harga)) 
                msg = "Data Berhasil Ditambahkan"
            
        except:
            con.rollback()
            msg = "Data Gagal Ditambahkan"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute("SELECT * from datacar")

    rows = cur.fetchall()

    return render_template ("list.html", rows=rows)


@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sql.connect("database.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM datacar WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nm = request.form['nm']
            tahun = request.form['tahun']
            warna= request.form['warna']
            harga = request.form['harga']

            # UPDATE a specific record in the database based on the rowid
            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE datacar SET name='"+nm+"', tahun='"+tahun+"', warna='"+warna+"', harga='"+harga+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE datacar SET name="+nm+", tahun="+tahun+", warna="+warna+", harga="+harga+" WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sql.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM datacar WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
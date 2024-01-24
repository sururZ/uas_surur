from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new student to the database
@app.route("/enternew")
def enternew():
    return render_template("student.html")

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            nim = request.form['nim']
            prodi = request.form['prodi']
            pesan = request.form['pesan']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO mahasiswa (name, nim, prodi, pesan) VALUES (?,?,?,?)",(nm, nim, prodi, pesan))

                con.commit()
                msg = "Berhasil di Tambahkan ke Database"
        except:
            con.rollback()
            msg = "Gagal Tambah Laporan"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route to SELECT all data from the database and display in a table      
@app.route('/list')
def list():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM mahasiswa")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("list.html",rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM mahasiswa WHERE rowid = " + id)

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
            nim = request.form['nim']
            prodi = request.form['prodi']
            pesan = request.form['pesan']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE mahasiswa SET name='"+nm+"', nim='"+nim+"', prodi='"+prodi+"', pesan='"+pesan+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Berhasil Mengubah Laporan"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE mahasiswa SET name="+nm+", nim="+nim+", prodi="+prodi+", pesan="+pesan+" WHERE rowid="+rowid

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
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM mahasiswa WHERE rowid="+rowid)

                    con.commit()
                    msg = "Laporan Berhasil di Hapus"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)
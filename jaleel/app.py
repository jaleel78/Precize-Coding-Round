from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('sat_results.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS sat_results
             (name text PRIMARY KEY, city text, country text, pincode text, score integer, passed text)''')


conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        country = request.form['country']
        pincode = request.form['pincode']
        score = request.form['score']
        passed = 'Pass' if int(score) > 30 else 'Fail'

        conn = sqlite3.connect('sat_results.db')
        c = conn.cursor()

        # Insert the data into the table
        c.execute("INSERT INTO sat_results (name, city, country, pincode, score) VALUES (?, ?, ?, ?, ?)", (name, city, country, pincode, score))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return redirect('/')
    else:
        return render_template('insert.html')


@app.route('/view')
def view():
    # Create a connection to the database
    conn = sqlite3.connect('sat_results.db')
    c = conn.cursor()

    # Retrieve all the data from the table
    c.execute("SELECT * FROM sat_results")
    data = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('view.html', data=data)

@app.route('/get_rank', methods=['GET', 'POST'])
def get_rank():
    if request.method == 'POST':
        name = request.form['name']

        # Create a connection to the database
        conn = sqlite3.connect('sat_results.db')
        c = conn.cursor()

        # Retrieve the data for the given name
        c.execute("SELECT * FROM sat_results WHERE name=?", (name,))
        data = c.fetchone()

        # Retrieve the rank of the candidate
        c.execute("SELECT COUNT(*) FROM sat_results WHERE score > ?", (data[4],))
        rank = c.fetchone()[0] + 1

        # Close the connection
        conn.close()

        return 'Rank of {} is {}'.format(name, rank)
    else:
        return render_template('get_rank.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        passed = 'Pass' if int(score) > 30 else 'Fail'

        # Create a connection to the database
        conn = sqlite3.connect('sat_results.db')
        c = conn.cursor()

        # Update the score for the given name
        c.execute("UPDATE sat_results SET score=?, passed=? WHERE name=?", (score, passed, name))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return 'Score updated successfully!'
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        name = request.form['name']

        # Create a connection to the database
        conn = sqlite3.connect('sat_results.db')
        c = conn.cursor()

        # Delete the record for the given name
        c.execute("DELETE FROM sat_results WHERE name=?", (name,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return 'Record deleted successfully!'
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)

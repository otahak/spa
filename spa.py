import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/z25'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 300
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 200
app.config['POOL_PRE_PING'] = True
db = SQLAlchemy(app)

#defining the page object - need to turn this into its own file and import it above to do it the OOP way
class Page(db.Model):
	__tablename__ = 'pages'
	id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title         = db.Column(db.String(65))
	description   = db.Column(db.String(255))
	src           = db.Column(db.String(65))
	number        = db.Column(db.Integer)
	created_at    = db.Column(db.DateTime)

pageCount = len(Page.query.all())

@app.route('/')
def index():
	currentPage = Page.query.order_by(Page.id.desc()).first()
	return render_template('home.html', page=currentPage)

@app.route('/about')
def about():
	return 'about us placeholder'

@app.route('/contact')
def contact():
	return 'contact us placeholder'

@app.route('/p/<n>', methods=['GET', 'POST'])
def pageNumber(n):
	N = int(n)
	if request.method == 'POST':				
		if N > 0 and N <= pageCount:
			#p = session.query(Page).filter(Page.number == n).first()
			p = Page.query.filter_by(id=n).first()
			return json.dumps([{'response': 'good', 'submitted': n, 'page' : { 'number' : p.number, 'src' : p.src, 'title' : p.title, 'description' : p.description, 'first' : 1, 'last' : int(pageCount)}}])
		else:
			return json.dumps([{'response': 'bad', 'submitted': n}])

	elif request.method == 'GET':
		if N > 0 and N <= pageCount:
			p = Page.query.filter_by(id=n).first()
			return render_template('home.html', page=p)
		else:
			return json.dumps([{pageCount}])			
	else:
		return json.dumps([{'response' : 'uhoh'}])

@app.errorhandler(500)
def server_error(e):
	#need to create a dedicated 500 error page
	return "shit", 500

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html', page=Page.query.filter_by(id=0).first()), 404



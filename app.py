from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SubmitField,SelectField,DateField
from wtforms.validators import DataRequired, email_validator, Length, EqualTo
from datetime import datetime
import feedparser


from flask_mysqldb import MySQL



app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "CTKDANTE"
app.config['MY_SQL HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "dante"
app.config['MYSQL_DB'] = "users_db"

db = MySQL(app)



# creating the form class
class signupForm(FlaskForm):
    firstName = StringField('Enter Name', validators=[DataRequired(), Length(min=2, max=50)])
    secondName = StringField(validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Enter email', validators=[DataRequired()])
    phoneNumber = StringField('Enter Number', validators=[DataRequired(), Length(min=10, max=13)])
    password = PasswordField('Enter password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm passord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


#creating another for class for user input
class user_input(FlaskForm):
    commodity = SelectField('Choose commodity To foreast', choices=[('sugar', 'Sugar'),
                 ('maize', 'Maize'), ('rice', 'Rice'), ('Beans', 'Beans')])
    #forecasted_date = DateField('Enter Date to forecast', format="%Y-%m-%d")
    forecasted_date = SelectField('Choose Month in which to forecast', choices=[('2023-02-15', 'January'),
    ('2023-02-15', 'Febuary'), ('2023-03-15', 'March'), ('2023-04-15', 'April'), ('2023-05-15', 'May'), ('2023-06-15', 'June'), 
    ('2023-07-15', 'July'), ('2023-08-15', 'August'), ('2023-09-15', 'September'), ('2023-10-15', 'October'), ('2023-11-15', 'November'), ('2023-12-15', 'December')])
    
    submit = SubmitField('Forecast')
    


@app.route('/')
def index():
    return render_template('index.html')
   

@app.route('/index')
def index1():
    return render_template('index.html')

#signup route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    
    form = signupForm()
    

    if form.validate_on_submit():
        print("Form validation successful")
        firstName = form.firstName.data
        secondName = form.secondName.data
        email = form.email.data
        phoneNumber =form.phoneNumber.data
        password = form.password.data
        password2 = form.confirm_password.data
        date_added = datetime.utcnow()

        
        

        cur = db.connection.cursor()
        cur.execute("SELECT email FROM user_info WHERE email = %s", (email,))
        existing_email = cur.fetchone()

        if existing_email:
            flash("email already exists")
        else:   
            cur.execute(" INSERT INTO user_info (FirstName, SecondName, email, phoneNumber,password, date_added ) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, secondName, email, phoneNumber, password,date_added ))
            db.connection.commit()
            cur.close()
            return redirect(url_for('trends'))
        
    else: flash(form.errors)


        
           
    
    return render_template('sign_up.html',  
    form = form)

@app.route('/Forecast', methods = ['GET', 'POST']) 
def forecast():
    form = user_input()
    if form.validate_on_submit():
        choice = form.commodity.data
        date_choice = form.forecasted_date.data
        
        flash('Here is Your forecast of ' +choice+ ' For date ' +date_choice)
        print(choice +" is for month "+ date_choice )
    
    else: print(form.errors)

    
    

    return render_template('Forecast.html', form = form)


#Trends route
@app.route('/Dashboard')
def trends():
    return render_template('Dashboard.html')

#'About us' Route
@app.route('/about')
def about():
    return render_template('about.html')

#routes for trends extensions
@app.route('/Summary')
def summary():
    return render_template("summary.html")

#creating dynamic tables
headings = ('    ','Owino', 'Mbale', 'Masaka', 'Gulu')
data = (
    ('Sugar', '', '', '', ''),
    ('Rice', '', '', '', ''),
    ('Maize flour', '', '', '', ''),
    ('Beans', '', '', '', '')

)
commodity_heading = ('Sugar', 'Rice', 'Maize Flour', 'Beans')
lowest_prx = 2000

@app.route('/Key_Stats')
def key_stats():
#creating the feed parser
    feed_url = 'http://feeds.bbci.co.uk/news/business/rss.xml'
    feed = feedparser.parse(feed_url)

# Access the feed data
    feed_title = feed.feed.title
    entries = feed.entries
    return render_template("stats.html", headings = headings, data = data,
    
    commodity_heading = commodity_heading,
    lowest_prx = lowest_prx,
    feed_title = feed_title,
    entries = entries
    )

@app.route('/Explanations')
def explanations():
    return render_template('explanations.html')

@app.route('/Recommendations')
def recommendations():
    return render_template('recommendations.html')



if __name__ == "__main__":
    app.run(debug=True)


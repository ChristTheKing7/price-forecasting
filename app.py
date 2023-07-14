from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SubmitField,SelectField,DateField
from wtforms.validators import DataRequired, email_validator, Length, EqualTo
from datetime import datetime
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib





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
    commodity = SelectField('Choose commodity To foreast', choices=[('Sugar', 'Sugar'),
                 ('Maize', 'Maize'), ('Rice', 'Rice'), ('Beans', 'Beans')])
    #forecasted_date = DateField('Enter Date to forecast', format="%Y-%m-%d")
    forecasted_date = SelectField('Choose Month in which to forecast', choices=[('2023-02-15', 'January'),
    ('2023-02-15', 'Febuary'), ('2023-03-15', 'March'), ('2023-04-15', 'April'), ('2023-05-15', 'May'), ('2023-06-15', 'June'), 
    ('2023-07-15', 'July'), ('2023-08-15', 'August'), ('2023-09-15', 'September'), ('2023-10-15', 'October'), ('2023-11-15', 'November'), ('2023-12-15', 'December')])
    
    submit = SubmitField('Forecast')
    
def sendmail():
   
    return 

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
    commodity_heading = ('','Owino', 'Mbale', 'Masaka', 'Gulu')
    choice = 0

    if form.validate_on_submit():
        choice = form.commodity.data
        date_choice = form.forecasted_date.data
        
        flash('Here is Your forecast of ' +choice+ ' For date ' +date_choice)
        print(choice +" is for month "+ date_choice )
        

        condition = True
        


    else: condition = False

    return render_template('Forecast.html', form = form, condition = condition,
    commodity_heading = commodity_heading, choice = choice,
    labels = label,values_flour = values_flour,
   values_beans = values_beans, values_sugar=values_sugar, values_rice= values_rice)


#Trends route
@app.route('/Dashboard')
def trends():
    
    message = "this is our price for this month"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    email = "ssembatyadavid54@gmail.com"
    server.login("price4cast@gmail.com", "Price4c@st256")
    server.sendmail('price4cast@gmail.com', email, message)
    return render_template('Dashboard.html')

#'About us' Route
@app.route('/about')
def about():
    return render_template('about.html')

#Data for prices
data = [
        ("January", 1597, 2045, 3564, 4837),
        ("Febuary", 1497, 2090, 3932, 4276),
        ("March", 1580, 2500, 3048, 4091),
        ("April", 2197, 2600, 3019, 4849),
        ("May", 1550, 2700, 3782, 4092),
        ("June", 1297,2000, 3892, 4823),
        ("July", 1597, 1956, 3649, 4104),
        ("August", 1527, 2020, 3892, 4824),
        ("September", 1697, 1500, 3820, 4024),
        ("October", 1530, 2300, 3672, 4034),
        ("November", 1545, 2400, 3732, 4783),
        ("December", 1559, 1900, 3313, 4013),

    ]
label = [row[0] for row in data]
#flour
values_flour_owino = [row[1] for row in data]
values_flour_masaka = [row[2] for row in data]
values_flour_mbale = [row[3] for row in data]
values_flour_gulu = [row[4] for row in data]

#sugar
values_sugar_owino = [row[1] for row in data]
values_sugar_masaka =  [row[2] for row in data]
values_sugar_mbale = [row[3] for row in data]
values_sugar_gulu = [row[4] for row in data]

#rice
values_rice_owino = [row[1] for row in data]
values_rice_masaka = [row[2] for row in data]
values_rice_mbale = [row[3] for row in data]
values_rice_gulu = [row[4] for row in data]

#beans
values_beans_owino = [row[1] for row in data]
values_beans_masaka = [row[2] for row in data]
values_beans_mbale = [row[3] for row in data]
values_beans_gulu = [row[4] for row in data]

#dummy overall
values_flour = [row[1] for row in data]
values_beans = [row[2] for row in data]
values_sugar = [row[3] for row in data]
values_rice = [row[4] for row in data]

#routes for trends extensions
@app.route('/Summary', methods = ["POST", "GET"])
def summary():
   

    return render_template('summary.html', labels = label,
   values_flour = values_flour,
   values_beans = values_beans, 
   values_sugar=values_sugar,
   values_rice= values_rice,
   values_flour_owino = values_flour_owino,
   values_flour_masaka = values_flour_masaka,
   values_flour_mbale = values_flour_mbale,
   values_flour_gulu = values_flour_gulu,
   values_sugar_owino = values_sugar_owino,
   values_sugar_masaka = values_sugar_masaka,
   values_sugar_mbale = values_sugar_mbale,
   values_sugar_gulu = values_sugar_gulu,
   values_rice_owino = values_rice_owino,
   values_rice_masaka = values_rice_masaka,
   values_rice_mbale = values_rice_mbale,
   values_rice_gulu = values_rice_gulu,
   values_beans_owino = values_beans_owino,
   values_beans_masaka = values_beans_masaka,
   values_beans_mbale = values_beans_mbale,
   values_beans_gulu = values_beans_gulu,
   )
    

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


    
    
#creating the feed parser
def fetch_feeds():
    feed_url = 'http://feeds.bbci.co.uk/news/business/rss.xml'
    feed = feedparser.parse(feed_url)
    
    entries = feed.entries
    feed_urls = [entry.link for entry in entries]

    feed_title = feed.feed.title

    return feed_title, entries, feed_urls
#scheduler = BlockingScheduler()
# # Schedule the fetch_feeds function to run daily at a specific time
# scheduler.add_job(fetch_feeds, 'interval', days=1, start_date='2023-07-10 19:06:00')
# # Start the scheduler
# scheduler.start()

@app.route('/Key_Stats')
def key_stats():
    feed_title, entries, feed_urls = fetch_feeds()
    

    return render_template("stats.html", headings = headings, data = data,
    
    commodity_heading = commodity_heading,
    lowest_prx = lowest_prx,
    feed_title = feed_title,
    entries = entries,
    feed_urls = feed_urls
    )



@app.route('/Recommendations', methods = ["POST", "GET"])
def recommendations():
    

   return render_template('recommendations.html', labels = label,
   values_flour = values_flour,
   values_beans = values_beans, 
   values_sugar=values_sugar,
   values_rice= values_rice,
   values_flour_owino = values_flour_owino,
   values_flour_masaka = values_flour_masaka,
   values_flour_mbale = values_flour_mbale,
   values_flour_gulu = values_flour_gulu,
   values_sugar_owino = values_sugar_owino,
   values_sugar_masaka = values_sugar_masaka,
   values_sugar_mbale = values_sugar_mbale,
   values_sugar_gulu = values_sugar_gulu,
   values_rice_owino = values_rice_owino,
   values_rice_masaka = values_rice_masaka,
   values_rice_mbale = values_rice_mbale,
   values_rice_gulu = values_rice_gulu,
   values_beans_owino = values_beans_owino,
   values_beans_masaka = values_beans_masaka,
   values_beans_mbale = values_beans_mbale,
   values_beans_gulu = values_beans_gulu,
   )
 



if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SubmitField,SelectField,DateField
from wtforms.validators import DataRequired, email_validator, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import feedparser
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from flask_mail import Message, Mail
import os





from flask_mysqldb import MySQL



app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "CTKDANTE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://users_db_yfaj_user:imK9YfoZzmj3J1GUFS085uEECdmwxccI@dpg-cips9plgkuvrtof1qm3g-a.oregon-postgres.render.com/users_db_yfaj'
app.config['SQLALCHEMY_ECHO'] = True  # Optional: For printing SQL commands
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable tracking modifications


#postgres://users_db_yfaj_user:imK9YfoZzmj3J1GUFS085uEECdmwxccI@dpg-cips9plgkuvrtof1qm3g-a.oregon-postgres.render.com/users_db_yfaj
#db_uri = 'postgres://users_db_yfaj_user:imK9YfoZzmj3J1GUFS085uEECdmwxccI@dpg-cips9plgkuvrtof1qm3g-a.oregon-postgres.render.com/users_db_yfaj'
 

mail = Mail(app)

db = SQLAlchemy(app)

#create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, )
    FirstName = db.Column(db.String(50), nullable= False)
    SecondName = db.Column(db.String(50), nullable= False)
    email = db.Column(db.String(100), nullable= False, unique=True)
    password = db.Column(db.String(50), nullable= False)
    phoneNumber = db.Column(db.String, nullable= False)
    #date_added = db.Column(db.DateTime, Default=datetime.utcnow)



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

##prices for the current onth
def send_mail_wrapper():
    Rice_this_month = 4000
    Sugar_this_month = 3500
    cassava_this_month = 2000
    send_mail(Rice_this_month, Sugar_this_month, cassava_this_month)


    
def send_mail(rice, sugar, cassava):
    with app.app_context():
        email = "elitecs256@gmail.com"
        message = Message("Price Alerts", recipients=[email], sender='price4cast@gmail.com')
        message.subject = 'Alerts for this Month!'
        #converting the integer prices to strings
        rice_str = str(rice)
        sugar_str = str(sugar)
        cassava_str = str(cassava)

        message.body = 'These are our prices for this month:\nRice: ' + rice_str + ', Sugar: ' + sugar_str + ', Cassava: ' + cassava_str
        try:
        # Your email sending code here
        # For example, using smtplib to send an email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            email = "ssembatyadavid54@gmail.com"
            server.login("price4cast@gmail.com", "rmkpwdsijfwtauee")
            server.sendmail('price4cast@gmail.com', email, "Your email content")
            server.quit()
            print("Email sent successfully!")
        except smtplib.SMTPDataError as e:
            print(f"SMTPDataError: {e}")
            print("Daily user sending quota exceeded. Please try again later or upgrade your account.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print(message.body)
#creating a function that fetches emails
def get_emails():
    # Query the Users table to get only the 'email' column
    emails = Users.query.with_entities(Users.email).all()

    # Extract the emails from the query result (list of tuples) into a list
    email_list = [email for (email,) in emails]
    print(email_list)

    return email_list
        
# #creating a scheduler that sends emails
email_scheduler = BackgroundScheduler()
email_scheduler.add_job(send_mail_wrapper, 'interval', days=30, start_date='2023-07-17 10:35:00')
# # # Start the scheduler
email_scheduler.start()



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
        with app.app_context():
            
            user = Users(FirstName=firstName, SecondName=secondName, email=email, password=password, phoneNumber=phoneNumber)
            db.session.add(user)
            db.session.commit() 
        
        
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
   values_beans = values_beans, values_sugar=values_sugar, values_rice= values_rice,
   lowest_prx =lowest_prx )


#Trends route
@app.route('/Dashboard')
def trends():
    get_emails()
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
    with app.app_context():
        feed_url = 'http://feeds.bbci.co.uk/news/business/rss.xml'
        feed = feedparser.parse(feed_url)
    
        entries = feed.entries
        feed_urls = [entry.link for entry in entries]

        feed_title = feed.feed.title


    return feed_title, entries, feed_urls
#creating scheduler that fetches feeds daily
Feed_scheduler = BackgroundScheduler()
# # Schedule the fetch_feeds function to run daily at a specific time
Feed_scheduler.add_job(fetch_feeds, 'interval', days=1, start_date='2023-07-10 19:06:00')
# # Start the scheduler
Feed_scheduler.start()


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
def get_all_users():
    with app.app_context():
        users = Users.query.all()
        print(users)

get_all_users()



if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()


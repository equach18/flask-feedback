from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedbacks"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'shhhheeecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
with app.app_context():
    db.create_all()
debug = DebugToolbarExtension(app)


@app.route('/')
def root():
    """Redirects to the register page"""
    return redirect("/register")

@app.route('/register', methods=["POST", "GET"])
def register_user():
    """Renders registration form if user is not signed in. Handles when the user submits the form"""
    form = RegisterForm()
    
    if "username" in session:
        return redirect(f"/users/{session["username"]}")
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        # create new user and add to db
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        
        # add user to session
        session["username"] = user.username
        
        return redirect(f"/users/{session["username"]}")
    else:
        return render_template("register.html", form=form)
    
@app.route("/login", methods=["POST", "GET"])
def login_user():
    """Shows and processes the login form"""
    form = LoginForm()
    
    if "username" in session:
        return redirect(f"/users/{session["username"]}")
            
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # authenticate the user - returns user or False if the user does not exist
        user = User.authenticate(username, password)
        
        # if the user exists, then add that user to the session and redirect 
        if user:
            session["username"] = user.username
            return redirect(f"/users/{session["username"]}")
    else:
        return render_template("login.html", form=form)

@app.route("/users/<username>")
def show_user(username):
    """Displays a template that shows the user info if they are logged in."""
    user = User.query.get_or_404(username)
    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!", "error")
        return redirect("/")
    return render_template("user.html", user=user)        

@app.route("/logout")
def logout():
    """Logs the user out and redirects to the homepage"""
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["POST", "GET"])
def add_feedback(username):
    """Shows and processes the new feedback form"""
    if "username" not in session or username != session['username']:
        flash("You must be logged in to add!", "error")
        return redirect("/")
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("new-feedback.html", form=form)
        
@app.route("/feedback/<int:feedback_id>/update", methods=["POST","GET"])
def update_feedback(feedback_id):
    """Shows and processes the updated feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to update this post!", "error")
        return redirect("/")
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("edit-feedback.html", form=form)
    
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Deletes the feedback of the user and redirects back the the user page"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to delete this post!", "error")
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()
        
    return redirect(f"/users/{feedback.username}")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """"Deletes the user from the database and redirects to the homepage"""
    if "username" not in session or username != session['username']:
        flash("You must be logged in to delete this user", "error")
        return redirect("/")
    
    user = User.query.get_or_404(username)
    
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/")
    
    

            
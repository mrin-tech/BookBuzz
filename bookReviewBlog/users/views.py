# views for the users
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from bookReviewBlog import db
from bookReviewBlog.models import User, BlogPost
from bookReviewBlog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from bookReviewBlog.users.pictureHandler import add_profile_pic

users = Blueprint('users', __name__)

# register
@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # if the form is valid then get the user
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Success!')

            # checks if the user was trying to reach a page that required a dead login
            next = request.args.get('next')
            if next==None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

#
# the users account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        # if they add a picture to their account
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profilePics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


# the users list of blog posts
@users.route("/<username>")
def userPosts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('userBlogPosts.html', blog_posts=blog_posts, user=user)

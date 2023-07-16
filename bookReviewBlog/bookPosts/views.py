from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from bookReviewBlog import db
from bookReviewBlog.models import BlogPost
from bookReviewBlog.bookPosts.forms import BookPostForm

bookPosts = Blueprint('bookPosts', __name__)

# create a post
@bookPosts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BookPostForm()
    if form.validate_on_submit():
        blogPost = BlogPost(title=form.title.data,
                            text=form.text.data,
                            userId=current_user.id)
        db.session.add(blogPost)
        db.session.commit()
        flash('blog post created')
        return redirect(url_for('core.index'))
    return render_template('createPost.html', form=form)


# view a post
@bookPosts.route('/<int:blogPostID>')
def blogPost(blogPostID):
    blogPost = BlogPost.query.get_or_404(blogPostID)
    return render_template('blogPostView.html', title=blogPost.title, date=blogPost.date, post=blogPost)


# update
@bookPosts.route('/<int:blogPostID>/update', methods=['GET', 'POST'])
@login_required
def update(blogPostID):
    blogPost = BlogPost.query.get_or_404(blogPostID)
    if blogPost.author != current_user:
        abort(403)
    form = BookPostForm()
    if form.validate_on_submit():
        blogPost.title=form.title.data
        blogPost.text=form.text.data

        db.session.commit()
        flash('blog post updated')
        return redirect(url_for('bookPosts.blogPost', blogPostID=blogPost.id))
    elif request.method == 'GET':
        form.title.data = blogPost.title
        form.text.data = blogPost.text
    return render_template('createPost.html', title='Updating', form=form)


# delete
@bookPosts.route('/<int:blogPostID>/delete', methods=['GET', 'POST'])
@login_required
def deletePost(blogPostID):
    blogPost = BlogPost.query.get_or_404(blogPostID)
    if blogPost.author != current_user:
        abort(403)
    
    db.session.delete(blogPost)
    db.session.commit()
    flash('blog post deleted')
    return redirect(url_for('core.index'))
    
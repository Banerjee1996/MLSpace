from flask import render_template ,url_for , flash , redirect , request ,abort,Blueprint
from flaskblog.posts.forms import PostForm
from flaskblog import  db 
from flaskblog.models import Post
from flask_login import current_user , login_required
from flaskblog.utils import save_post_picture 


posts = Blueprint('posts',__name__)


@posts.route("/post/new",methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        page  = Post(title = form.title.data ,content = form.content.data,author = current_user.id,image_file=save_post_picture(form.picture.data))
        page.save()
        flash('Your post has been created !!!!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,legend = 'New Post')


@posts.route("/post/<post_id>")
def post(post_id):
    post  = Post.objects(id=post_id).first()
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<post_id>/update",methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post  = Post.objects(id=post_id).first()
    if post.author.id != current_user.id :
        #flash(str(post.author.id),'success')
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        flash('Your post has been updated !!!!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static',filename = 'profile_pics/' + post.image_file)
    return render_template('create_post.html',title='Update Post',
                         image_file=image_file,form=form,legend = 'Update Post')



@posts.route("/post/<post_id>/delete",methods = ['POST'])
@login_required
def delete_post(post_id):
    post  = Post.objects(id=post_id).first()
    if post.author.id != current_user.id :
        abort(403)
    Post.objects(id=post_id).delete()
    flash('Your post has been updated !!!!','success')
    return redirect(url_for('main.home'))


 



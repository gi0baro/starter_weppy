from weppy import response, url
from weppy.tools import requires

from heliosphere import app, auth, db


@app.on_error(404)
def error_404():
    response.meta.title = "Heliosphere-404"
    return app.render_template("404.haml")


@app.route("/")
def welcome():
    response.meta.title = "Heliosphere"
    return dict()


@app.route('/account(/<str:f>)?(/<str:k>)?')
def account(f, k):
    response.meta.title = "Heliosphere | Account"
    form = auth(f, k)
    return dict(req=f, form=form)


@app.route()
def users():
    response.meta.title = "Heliosphere | Users"
    users = db(db.User.id > 0).select()
    return dict(users=users)


@app.route("/user/<str:userid>")
@requires(auth.is_logged_in, url('main.account', 'login'))
def profile(userid):
    user = db.User(id=userid)
    response.meta.title = "Heliosphere | " + user.first_name + " " + \
                          user.last_name + " profile"
    return dict(user=user)

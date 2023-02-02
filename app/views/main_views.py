from flask import Blueprint,render_template, url_for, session,g, request, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User,Profile

from app.forms import ModifyPasswordForm

from app import db

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@bp.route('/clinic_user_choice')
def clinic_user_choice():
    profile_list = Profile.query.filter_by(idx_user=g.user.idx).all() 
    return render_template('clinic_user_choice.html', profile_list=profile_list)

@bp.route('/specialist_board')
def specialist_board():
    return render_template('board.html')


@bp.route('/admin_board')
def admin_board():
    return render_template('admin_board.html')



@bp.route('/board/<int:profile_idx>/')
def board(profile_idx):
    profile = Profile.query.get(profile_idx)
    return render_template('board.html', profile=profile)


@bp.route('/mypage/', methods=('GET', 'POST'))
def mypage():
    form = ModifyPasswordForm()
    if request.method == 'POST' and form.validate_on_submit() and check_password_hash(g.user.password, form.password.data):
        user=User.query.get(g.user.idx)
        user.password=generate_password_hash(form.password1.data)
        db.session.commit()
        return redirect(url_for('main.mypage'))
    profile_list = Profile.query.filter_by(idx_user=g.user.idx).all() 
    return render_template('mypage.html', profile_list=profile_list, form=form)




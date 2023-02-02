
from datetime import datetime
from flask import Blueprint,url_for, render_template,flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db
from app.models import User,Profile

from app.forms import LoginForm, ClinicCreateForm, SpecialistCreateForm, AdminCreateForm, ProfileCreateForm, FindIdForm, FindPasswordForm, FindPasswordForm_reset
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.idx
            if user.type=='clinic':
                return redirect(url_for('main.clinic_user_choice'))
            elif user.type=='specialist':
                return redirect(url_for('main.specialist_board'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)



@bp.route('/clinic_signup/', methods=('GET', 'POST'))
def clinic_signup():
    form = ClinicCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            user = User(user_id=form.user_id.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        corporate_registration_number=form.corporate_registration_number.data,
                        clinic_name=form.clinic_name.data,
                        name=form.name.data,
                        phone=form.phone.data,
                        create_date=datetime.now(),
                        type='clinic')
            db.session.add(user)
            db.session.commit()
            profile = Profile(idx_user=user.idx,
                    profile_name=form.name.data,
                    create_date=datetime.now(),
                    )
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/clinic_signup.html', form=form)



@bp.route('/profile_signup/', methods=('GET', 'POST'))
def profile_signup():
    form = ProfileCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        profile = Profile(idx_user=g.user.idx,
                    profile_name=form.profile_name.data,
                    create_date=datetime.now(),
                    )
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('main.clinic_user_choice'))
    return render_template('auth/profile_signup.html', form=form)


@bp.route('/specialist_signup/', methods=('GET', 'POST'))
def specialist_signup():
    form = SpecialistCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            user = User(user_id=form.user_id.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        specialist_license_number=form.specialist_license_number.data,
                        name=form.name.data,
                        phone=form.phone.data,
                        create_date=datetime.now(),
                        type='specialist')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/specialist_signup.html', form=form)



@bp.route('/profile_delete/')
def profile_delete():
    profile_list = Profile.query.filter_by(idx_user=g.user.idx).all() 
    return render_template('auth/profile_delete.html',profile_list=profile_list)



@bp.route('/delete/<int:profile_idx>')
def delete(profile_idx):
    profile = Profile.query.get_or_404(profile_idx)
    db.session.delete(profile)
    db.session.commit()
    return redirect(url_for('main.clinic_user_choice'))



@bp.route('/find_id/', methods=('GET', 'POST'))
def find_id():
    form = FindIdForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data, phone=form.phone.data).first()
        if user:
            message='당신의 아이디는'+ user.user_id +'입니다.'
            flash(message)
            return redirect(url_for('auth.login'))
        else:
            flash('해당 정보에 맞는 ID는 없습니다. 다시 한번 확인하여 주세요.')
            return redirect(url_for('auth.find_id'))
    return render_template('auth/find_id.html',form=form)


@bp.route('/find_password/', methods=('GET', 'POST'))
def find_password():
    form = FindPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data, name=form.name.data, phone=form.phone.data).first()
        if user:
            return redirect(url_for('auth.find_password_reset',user=user.user_id))
        else:
            flash('해당 정보에 맞는 데이터가 없습니다. 다시 한번 확인하여 주세요.')
            return redirect(url_for('auth.find_password'))
    return render_template('auth/find_password.html',form=form)




@bp.route('/find_password_reset/<string:user>',methods=('GET', 'POST'))
def find_password_reset(user):
    form = FindPasswordForm_reset()
    if request.method == 'POST' and form.validate_on_submit():
        a = User.query.filter_by(user_id=user).first()
        a.password=generate_password_hash(form.password1.data)
        db.session.commit()
        flash('비밀번호가 변경되었습니다.')
        return redirect(url_for('auth.login'))
    return render_template('auth/find_password_reset.html',form=form)



@bp.route('/admin_login/', methods=('GET', 'POST'))
def admin_login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.idx
            return redirect(url_for('main.admin_board'))
        flash(error)
    return render_template('auth/admin_login.html', form=form)


@bp.route('/admin_signup/', methods=('GET', 'POST'))
def admin_signup():
    form = AdminCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            user = User(user_id=form.user_id.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        name=form.name.data,
                        phone=form.phone.data,
                        create_date=datetime.now(),
                        type='admin')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.admin_login'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/admin_signup.html', form=form)

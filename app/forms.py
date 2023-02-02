from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    user_id = StringField('아이디', validators=[DataRequired('아이디는 필수입력 항목입니다.')])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])



class ClinicCreateForm(FlaskForm):
    user_id = StringField('사용자아이디', validators=[DataRequired(), Length(min=3, max=25)])
    corporate_registration_number = StringField('사업자 등록번호', validators=[DataRequired()])
    clinic_name = StringField('상호명', validators=[DataRequired()])
    name = StringField('사용자 이름', validators=[DataRequired()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    phone = StringField('핸드폰번호', validators=[DataRequired()])


class ProfileCreateForm(FlaskForm):
    profile_name = StringField('사용자이름', validators=[DataRequired()])
    


class SpecialistCreateForm(FlaskForm):
    user_id = StringField('사용자아이디', validators=[DataRequired(), Length(min=3, max=25)])
    specialist_license_number = StringField('수의사 등록번호', validators=[DataRequired()])
    name = StringField('진단의 이름', validators=[DataRequired()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    phone = StringField('핸드폰번호', validators=[DataRequired()])



class AdminCreateForm(FlaskForm):
    user_id = StringField('사용자아이디', validators=[DataRequired(), Length(min=3, max=25)])
    name = StringField('사용자 이름', validators=[DataRequired()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    phone = StringField('핸드폰번호', validators=[DataRequired()])



class ModifyPasswordForm(FlaskForm):
    password = PasswordField('기존비밀번호', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])



class FindIdForm(FlaskForm):
    name = StringField('사용자 이름', validators=[DataRequired()])
    phone = StringField('핸드폰번호', validators=[DataRequired()])




class FindPasswordForm(FlaskForm):
    user_id = StringField('사용자아이디', validators=[DataRequired(), Length(min=3, max=25)])
    name = StringField('사용자 이름', validators=[DataRequired()])
    phone = StringField('핸드폰번호', validators=[DataRequired()])
   


class FindPasswordForm_reset(FlaskForm):
    password1 = PasswordField('password1', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
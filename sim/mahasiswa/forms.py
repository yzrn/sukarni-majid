from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sim.models import Tmahasiswa
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class mahasiswa_F(FlaskForm):
    npm= StringField('NPM', validators=[DataRequired(),Length(min=10, max=15)])
    nama= StringField('Nama', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired()])
    kelas= StringField('Kelas', validators=[DataRequired()]) 
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass =PasswordField('konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    alamat= TextAreaField('Alamat', validators=[DataRequired()])
    submit=SubmitField('Daftar')

    #cek npm
    def validate_npm(self, npm):
        ceknpm=Tmahasiswa.query.filter_by(npm=npm.data).first()
        if ceknpm:
            raise ValidationError('NPM ini Telah Terdaftar, Pake NPM yang Lain da')

    #cek Email
    def validate_email(self, email):
        cekemail=Tmahasiswa.query.filter_by(email=email.data).first()
        if cekemail:
            raise ValidationError('EMAIL ini Telah Terdaftar, Pake EMAIL yang Lain da')


class loginmahasiswa_F(FlaskForm):
    npm= StringField('NPM', validators=[DataRequired()])
    password=PasswordField('Password',  validators=[DataRequired()])
    submit=SubmitField('login')


class editmahasiswa_F(FlaskForm):
    npm= StringField('NPM', validators=[DataRequired(),Length(min=10, max=15)])
    nama= StringField('Nama', validators=[DataRequired()])
    email= StringField('Email', validators=[DataRequired()])
    kelas= StringField('Kelas', validators=[DataRequired()]) 
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass =PasswordField('konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    alamat= TextAreaField('Alamat', validators=[DataRequired()])
    foto= FileField('Ubah Foto Profile Anda', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Edit Data')

    #cek npm
    def validate_npm(self, npm):
        if npm.data != current_user.npm:
            ceknpm=Tmahasiswa.query.filter_by(npm=npm.data).first()
            if ceknpm:
                raise ValidationError('NPM ini Telah Terdaftar, Pake NPM yang Lain da')

    #cek Email
    def validate_email(self, email):
        if email.data != current_user.email:
            cekemail=Tmahasiswa.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('EMAIL ini Telah Terdaftar, Pake EMAIL yang Lain da')

class pengaduan_F(FlaskForm):
    subjek= StringField('Subjek', validators=[DataRequired()])
    kategori= SelectField(u'kategori pengaudan', choices=[('administrasi','pelayanan administrasi'), ('fasilitas','Fasilitas'), ('dosen','dosen')], validators=[DataRequired()])
    detail_pengaduan= TextAreaField('Pengaduan', validators=[DataRequired()])
    submit=SubmitField('Kirim')

class editpengaduan_F(FlaskForm):
    subjek= StringField('Subjek', validators=[DataRequired()])
    kategori= SelectField(u'kategori pengaudan', choices=[('administrasi','pelayanan administrasi'), ('fasilitas','Fasilitas'), ('dosen','dosen')], validators=[DataRequired()])
    detail_pengaduan= TextAreaField('Pengaduan', validators=[DataRequired()])
    submit=SubmitField('edit')


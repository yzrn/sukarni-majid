from audioop import add
from flask import Flask, render_template, redirect, request, url_for, Blueprint, flash
from sim.mahasiswa.forms import mahasiswa_F, loginmahasiswa_F, editmahasiswa_F, pengaduan_F, editpengaduan_F
from sim.models import Tmahasiswa, Tpengaduan
from sim import db, bcrypt 
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from sim import app
from PIL import Image


rmahasiswa= Blueprint ('rmahasiswa',__name__)

@rmahasiswa.route("/")
def home():
    return render_template("home.html")

@rmahasiswa.route("/about")
def about():
    return render_template("about.html")

@rmahasiswa.route("/registrasi")
def registrasi():
    return render_template("registrasi.html")

@rmahasiswa.route("/data_mahasiswa", methods=['GET','POST'])
def data_m():
    form=mahasiswa_F()
    if form.validate_on_submit():
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add_mahasiswa=Tmahasiswa(npm=form.npm.data, nama=form.nama.data, email=form.email.data,
        password=pass_hash, kelas=form.kelas.data, alamat=form.alamat.data)
        db.session.add(add_mahasiswa)
        db.session.commit()
        flash(f'Akun- {form.npm.data} yeeee berhasil daftar','info')
        return redirect(url_for('rmahasiswa.loginmahasiswa'))

    return render_template("data_mahasiswa.html", form=form)


@rmahasiswa.route("/login_mahasiswa", methods=['GET','POST'])
def loginmahasiswa():
    if current_user.is_authenticated:
        return redirect(url_for('rmahasiswa.home'))
    form=loginmahasiswa_F()
    if form.validate_on_submit():
        ceknpm=Tmahasiswa.query.filter_by(npm=form.npm.data).first()
        if ceknpm and bcrypt.check_password_hash(ceknpm.password, form.password.data):
            login_user(ceknpm)
            flash('welcome', 'warning')
            return redirect(url_for('rmahasiswa.akunmahasiswa'))
        else:
                flash('login Gagal, Periksa NPM dan password kembali', 'danger')

    return render_template("login_mahasiswa.html", form=form)
 
@rmahasiswa.route("/akunmahasiswa")
@login_required
def akunmahasiswa():
    return render_template("akunmahasiswa.html")


@rmahasiswa.route("/logout_mahasiswa",)
def logout_mahasiswa():
    logout_user()
    return redirect(url_for('rmahasiswa.home'))

#save foto
def simpan_foto(form_foto):
    random_hex= secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_foto.filename)
    foto_fn= random_hex + f_ext
    foto_path= os.path.join(app.root_path, 'sim/static/foto', foto_fn)
    ubah_size=(300,300)
    j=Image.open(form_foto)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn



@rmahasiswa.route("/edit_mahasiswa", methods=['GET','POST'])
@login_required
def edit_mahasiswa():
    form=editmahasiswa_F()
    if form.validate_on_submit():
        if form.foto.data:
            file_foto=simpan_foto(form.foto.data)
            current_user.foto = file_foto 
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.npm=form.npm.data
        current_user.nama=form.nama.data
        current_user.email=form.email.data
        current_user.kelas=form.kelas.data
        current_user.alamat=form.alamat.data
        current_user.password=pass_hash
        db.session.commit()
        flash('Data Anda berhasil di ubah', 'warning')
        return redirect(url_for('rmahasiswa.edit_mahasiswa'))
    elif request.method=="GET":
       form.npm.data=current_user.npm
       form.nama.data=current_user.nama
       form.email.data=current_user.email
       form.kelas.data=current_user.kelas
       form.alamat.data=current_user.alamat
    
    return render_template("edit_mahasiswa.html", form=form)

@rmahasiswa.route("/pengaduan", methods=['GET','POST'])
@login_required
def pengaduan():
    dt_pengaduan=Tpengaduan.query.filter_by(mahasiswa_id=current_user.id)
    form=pengaduan_F()
    if form.validate_on_submit():
        #tambah data pengaduan
        add_pengaduan= Tpengaduan(subjek=form.subjek.data, kategori=form.kategori.data, detail_pengaduan=form.detail_pengaduan.data, mahasiswa=current_user)
        db.session.add(add_pengaduan)
        db.session.commit()
        flash('Data telah di submit', 'warning')
        return redirect(url_for('rmahasiswa.pengaduan'))
    return render_template("pengaduan.html", form=form, dt_pengaduan=dt_pengaduan)


@rmahasiswa.route("/pengaduan/<int:ed_id>/update", methods=['GET','POST'])
@login_required
def update_pengaduan(ed_id):
    form=editpengaduan_F()
    dt_pengaduan=Tpengaduan.query.get_or_404(ed_id)
    if request.method=="GET":
        form.subjek.data=dt_pengaduan.subjek
        form.kategori.data=dt_pengaduan.kategori
        form.detail_pengaduan.data=dt_pengaduan.detail_pengaduan
    elif form.validate_on_submit():
        dt_pengaduan.subjek=form.subjek.data
        dt_pengaduan.kategori=form.kategori.data
        dt_pengaduan.detail_pengaduan=form.detail_pengaduan.data
        db.session.commit()
        flash('data telah di ubah', 'warning')
        return redirect(url_for('rmahasiswa.pengaduan'))
        
    return render_template('edit_pengaduan.html', form=form)


@rmahasiswa.route("/delete/<id>", methods=['GET','POST'])
@login_required
def hapus_pengaduan(id):
    h_pengaduan=Tpengaduan.query.get(id)
    db.session.delete(h_pengaduan)
    db.session.commit()
    flash('Data Anda berhasil di hapus', 'warning')
    return redirect(url_for('rmahasiswa.pengaduan'))


@rmahasiswa.route("/artikel/<info>")
def artikel_info(info):
    return"Halaman Artikel " + info ; 
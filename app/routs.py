from flask import *
from app import stuff, mysql
import io


def routs(app):
    @app.route("/")
    def r():

        wronge = request.args.get('wronge', None)
        return render_template('login.html', wronge=wronge)


    @app.route('/clinic', methods=['GET', 'POST'])
    def clinic():
        
        if request.method == 'POST':
            #info = session['clinic_info']
            if request.form.get('type') == 'log':
                email = request.form.get('log-email')
                pas = request.form.get('log-pass')
            
                x = stuff.clinic('', pas, email)
                
                if x.login():
                    if 'clinic_info' in session:
                        session['clinic_info']['id'] = x.getId()
                    session['clinic_info'] = {
                        'id': x.getId()
                    }
                    print(session['clinic_info'])
                    print(x.getId())
                    
                else:
                    return redirect(url_for('r', wronge = "The password or email is uncorrect"))
                
                
            elif(request.form.get('type') == 'signin'):
                name = request.form.get('name')
                email = request.form.get('signin-email')
                pas = request.form.get('pass')
                phone = request.form.get('phone')
                location = request.form.get('location')
                discr = request.form.get('discribtion')
                logo = request.files.get('img')
                fields = ",".join(request.form.getlist('field'))
                x = stuff.clinic(name, pas, email, phone, location, discr, logo, fields)
                
                if(x.signin()):
                    if 'clinic_info' in session:
                        session['clinic_info']['id'] = x.getId()
                    session['clinic_info'] = {
                        'id': x.getId()
                    }
                    print(session['clinic_info'])
                    print(x.getId())
                else:
                    return redirect(url_for('r', wronge = "The email is used"))


            elif request.form.get('type') == 'doc':
                fname = request.form.get('f-name')
                lname = request.form.get('l-name')
                price = request.form.get('price')
                discr = request.form.get('discribtion')
                pic = request.files.get('img')
                fields = ",".join(request.form.getlist('field'))
                days = ",".join(request.form.getlist('day'))
                id = session['clinic_info']['id']
                x = stuff.clinic()
                x.infoById(id)
                x.addDoc(fname, lname, fields, days, pic, price)

        
        id = session['clinic_info']['id']
        x = stuff.clinic()
        x.infoById(id)
        return render_template('clinic.html', clinic=x)
       

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            #info = session['patient_info']
            if request.form.get('type') == 'log':
                email = request.form.get('log-email')
                pas = request.form.get('log-pass')
                x = stuff.patient('', pas, email)
                if x.login():
                    if 'patient_info' in session:
                        session['patient_info']['id'] = x.getId()
                    session['patient_info'] = {
                        'id' : x.getId()
                    }
                    print(session['patient_info'])
                    print(x.getId())
                else:
                    return redirect(url_for('r', wronge = "The password or email is uncorrect"))

            if request.form.get('type') == 'signin':
                fname = request.form.get('f-name')
                lname = request.form.get('l-name')
                email = request.form.get('signin-email')
                pas = request.form.get('pass')
                phone = request.form.get('phone')
                age = request.form.get('age')
                x = stuff.patient(fname, pas, email, lname, phone, age)                    
                if(x.signin()):
                    if 'patient_info' in session:
                        session['patient_info']['id'] = x.getId()
                    session['patient_info'] = {
                        'id' : x.getId()
                    }
                    print(session['patient_info'])
                    print(x.getId())
                else:
                   return redirect(url_for('r', wronge = "The email is used"))

            if request.form.get('type') == 'app':
                patientId = request.form.get('patientId')
                doctorId = request.form.get('doctorId')
                clinicId = request.form.get('clinicId')
                Day = request.form.get('Day').split(',')
                x = stuff.app_(patientId=patientId, doctorId=doctorId, clinicId=clinicId, date = Day[1], time = Day[0])                    
                if(x.create()):
                    pass
                else:
                   return redirect(url_for('home', wrongapp = 1))
                 
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id)        
        return render_template('home.html', user = x)
    
    @app.route('/logo/<int:logo_id>')
    def logo(logo_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT logo FROM clinic WHERE clinic_id = %s", (logo_id,))
            result = cur.fetchone()
            cur.close()
            
            if result:
                logo_data = result[0]
                return send_file(io.BytesIO(logo_data), mimetype='image/jpeg')
            else:
                return "Image not found", 404
        except mysql.connector.Error as err:
            return f"Error: {err}", 500
        
    @app.route('/img/<int:img_id>')
    def image(img_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT picture FROM doctor WHERE id = %s", (img_id,))
            result = cur.fetchone()
            cur.close()
            
            if result:
                img_data = result[0]
                return send_file(io.BytesIO(img_data), mimetype='image/jpeg')
            else:
                return "Image not found", 404
        except mysql.connector.Error as err:
            return f"Error: {err}", 500

    @app.route('/addDoctor', methods=['GET', 'POST'])
    def addDoc():
        id = session['clinic_info']['id']
        x = stuff.clinic()
        x.infoById(id)
        return render_template('addDoctor.html', clinic=x)
    
    @app.route('/profile')
    def profile():
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id)
        x.update_waitingtime()
        return render_template('profile.html', user = x)
    
    @app.route('/clinic_page/<int:clinic_id>')
    def clinicPage(clinic_id):
        y = stuff.clinic()
        y.infoById(clinic_id)
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id)
        return render_template('clinic_page.html', clinic = y, user = x) 

    @app.route('/clinic_page/<int:clinic_id>/<int:DocId>')
    def ev(clinic_id, DocId):
        y = stuff.clinic()
        y.infoById(clinic_id)
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id)
        ev = request.args.get('ev')
        y.setDocev(DocId, id, ev)
        return redirect((f'/clinic_page/{clinic_id}'))
    
    @app.route('/appointments/<int:clinic_id>/<int:DocId>')
    def appnmt(clinic_id, DocId):
        y = stuff.clinic()
        y.infoById(clinic_id)
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id) 
        a = stuff.app_()
        return render_template('appointments.html', clinic=y, DocId=DocId, user = x, app_ = a)
    
    @app.route('/profile/<int:app_id>')
    def remove(app_id):
        id = session['patient_info']['id']
        x = stuff.patient()
        x.infoById(id)
        a = stuff.app_(app_id)
        a.remove_app(app_id)
        return render_template('profile.html', user = x)
    
    @app.route('/appc/<int:DocId>')
    def appc(DocId):
        id = session['clinic_info']['id']
        y = stuff.clinic()
        y.infoById(id)
        y.update_waitingtime_by_doctor(DocId)
        a = stuff.app_()
        return render_template('appc.html', clinic=y, DocId=DocId, app_ = a)
    
    @app.route('/appc/<int:DocId>/<int:app_id>')
    def removeapp( DocId, app_id):
        id = session['clinic_info']['id']
        y = stuff.clinic()
        y.infoById(id)
        a = stuff.app_(app_id)
        a.remove_app(app_id)
        return render_template('appc.html', clinic=y, DocId=DocId, app_ = a)
    
    @app.route('/appc/<int:DocId>/<int:app_id>/5')
    def addF(DocId, app_id):
        id = session['clinic_info']['id']
        y = stuff.clinic()
        y.infoById(id)
        a = stuff.app_(app_id)
        a.addFive(DocId)
        return render_template('appc.html', clinic=y, DocId=DocId)
    
    @app.route('/appc', methods=['GET', 'POST'])
    def addapp(): 
        if request.method == 'POST':
            if request.form.get('type') == 'app':
                        email = request.form.get('email')
                        doctorId = request.form.get('doctorId')
                        clinicId = request.form.get('clinicId')
                        Day = request.form.get('Day').split(',')
                        p = stuff.patient(email=email)
                        info = p.check_email()
                        if(info):
                            patientId = info[0]
                            x = stuff.app_(patientId=patientId, doctorId=doctorId, clinicId=clinicId, date = Day[1], time = Day[0])                    
                            x.create()
                        else:
                            return redirect((f'/appc/{doctorId}?wrongapp = 1'))
                        return redirect((f'/appc/{doctorId}'))
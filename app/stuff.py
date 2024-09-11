
from app import mysql
from datetime import *
from math import *

class User:
    def __init__(self, name, pas, email):
        self.name = name
        self.pas = pas
        self.email = email

    def getId(self):
        try:
            cur = mysql.connection.cursor()
            query = f"SELECT {self.__class__.__name__}_id FROM ecp.{self.__class__.__name__} WHERE email = %s"
            cur.execute(query, (self.email,))
            result = cur.fetchone()
            cur.close()
            return result[0] if result else None
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
   
    def check_email(self):
        try:
            cur = mysql.connection.cursor()
            query = f"SELECT * FROM ecp.{self.__class__.__name__} WHERE email = %s"
            cur.execute(query, (self.email,))
            result = cur.fetchone()
            cur.close()
            if result:
                return result
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

class clinic(User):
    def __init__(self, name='', pas='', email='', phone='', location='', discr='', logo='', fiedls = ''):
        super().__init__(name, pas, email)
        self.phone = phone
        self.location = location
        self.discr = discr
        self.logo = logo
        self.fields = fiedls
     
    def signin(self):
        if not(self.check_email()):
            try:
                cur = mysql.connection.cursor()
                query = "CALL AddClinic(%s, %s, %s, %s, %s, %s, %s, %s);"
                cur.execute(query, (self.name, self.email, self.phone, self.pas, self.fields, self.logo.read(), self.discr, self.location))
                mysql.connection.commit()
                cur.close()
                return 1
            except mysql.connect.Error as err:
                print(f"Error: {err}")
                return None
        return 0

    def login(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.clinic WHERE email = %s AND password = %s"
            cur.execute(query, (self.email, self.pas))
            result = cur.fetchone()
            cur.close()
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
    
        if result:    
            self.name = result[1]
            self.phone = result[3]
            self.location = result[8]
            self.discr = result[7]
            self.logo = result[6]
            #self.logo = f"data:image/jpeg;base64,{l.decode('utf-8')}" if l else None
            self.fields = result[5]
            return 1
        else:
            return 0
        
    def infoById(self, id):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.clinic WHERE clinic_id = %s"
            cur.execute(query, (id,))
            result = cur.fetchone()
            cur.close()
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
    
        if result:    
            self.name = result[1]
            self.email = result[2]
            self.phone = result[3]
            self.location = result[8]
            self.discr = result[7]
            self.logo = result[6]
            self.fields = result[5]
            self.pas = result[4]
            return 1
        else:
            return 0
        
    def addDoc(self, fn, ls, fld, wd, pic, price):
        try:
            cur = mysql.connection.cursor()
            query = "CALL AddDoctor(%s, %s, %s, %s, %s, %s, %s);"
            em = self.getId()
            cur.execute(query, (em, fn, ls, fld, wd, pic.read(), price))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def removeDoc(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "CALL RemoveDoctor(%s);"
            cur.execute(query, (DocId,))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

    def getImgUrl(self):
        return f'/logo/{self.getId()}'
    
    def getDoctors(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.doctor WHERE clinic_id = %s"
            id = self.getId()
            cur.execute(query, (id,))
            result = cur.fetchall()
            cur.close()
            if result:
                return result
            else:
                return []
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def getDocev(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT GetDoctorEvolution(%s)"
            cur.execute(query, (DocId,))
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def setDocev(self, DocId, PId, ev):
        try:
            cur = mysql.connection.cursor()
            query = "CALL AddEvaluation(%s, %s, %s)"
            cur.execute(query, (PId,DocId,ev))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

    def getDays(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT work_days FROM ecp.doctor WHERE id = %s"
            cur.execute(query, (DocId,))
            result = cur.fetchone()
            cur.close()
            return result[0].split(",") if result else []
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

    def DocById(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.doctor WHERE id = %s"
            cur.execute(query, (DocId,))
            result = cur.fetchone()
            cur.close()
            return result if result else []
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
    
    def avlDaysDateTime(self, DocId):
        daynum={
                "Monday" : 0,
                "Tuesday" : 1,
                "Wednesday" : 2,
                "Thursday" : 3,
                "Friday" : 4,
                "Saturday" : 5,
                "Sunday" : 6
                }
        numlist = [] 

        for x in self.getDays(DocId):
            if x in daynum.keys():
                numlist.append(daynum[x])

        today = datetime.today()
        if datetime.now().time() > time(19,0,0):
            today = today + timedelta(days=1)
        current_weekday = today.weekday()
        
           # current_weekday = 0 if current_weekday == 6 else (current_weekday + 1)
        

        #I used rotation algorthm we used iv lab3 to make arr match 7 days from today
        arr = [x for x in range(current_weekday, 7)]
        arr2 = [x for x in range(0, current_weekday)]
        arr.extend(arr2)


          
        start_of_week = today
        available_days = [start_of_week + timedelta(days=i) for i in range(7)]   
        
        dic = {arr[i]:available_days[i].strftime('%Y-%m-%d') for i in range(len(arr))}

        result=[]
        daynames = list(daynum.keys())
        for x in numlist:
            if x in dic.keys():
                result.append([daynames[x],dic[x]])

        return result

    def update_waitingtime_by_doctor(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "CALL ecp.update_waitingtime_by_doctor(%s)"
            cur.execute(query, (DocId,))
            mysql.connection.commit()
            cur.close() 
            return 1
                
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def app_c(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = """
            SELECT appointment.appointment_id FROM appointment
            JOIN appointment_state ON appointment.appointment_id = appointment_state.appointment_id 
            WHERE appointment_state.state = 0 AND appointment.clinic_id = %s AND appointment.doctor_id = %s 
            ORDER BY time ASC;
              """
            id = self.getId()
            cur.execute(query, (id, DocId))
            result = cur.fetchall()
            cur.close()
            appObjList = ['', '', '']
            todaydate = datetime.now().date()
            todaytime = datetime.now().time()
            todayObj = []
            current = []
            other = []
            if result:
                for x in result:
                    y = app_(x[0])
                    y.info(x[0])

                    objTime = (y.time + datetime.strptime('00:00:00', '%H:%M:%S')).time()
                    objendTime = (y.endtime + datetime.strptime('00:00:00', '%H:%M:%S')).time()
                    objDate = y.date
                    if objDate == todaydate:
                        if objTime <= todaytime and objendTime >= todaytime:
                            current.append(y)
                            continue
                        todayObj.append(y)
                        continue
                    other.append(y)
                
                appObjList[0] = current
                appObjList[1] = todayObj
                appObjList[2] = other

                return appObjList
            else:
                return[]

        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
class patient(User):
    def __init__(self, fname='', pas='', email='', lname='', phone='', age=''):
        super().__init__(fname, pas, email)
        self.lname = lname
        self.phone = phone
        self.age = age

    def signin(self):
        if not(self.check_email()):
            try:
                cur = mysql.connection.cursor()
                query = "CALL AddPatient(%s, %s, %s, %s, %s, %s);"
                cur.execute(query, (self.name, self.lname, self.email, self.phone, self.age, self.pas))
                mysql.connection.commit()
                cur.close()
                return 1
            except mysql.connect.Error as err:
                print(f"Error: {err}")
                return None
        return 0 
        
    def login(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.patient WHERE email = %s AND password = %s"
            cur.execute(query, (self.email, self.pas))
            result = cur.fetchone()
            cur.close()
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
    
        if result:    
            self.fname = result[1]
            self.lname = result[2]
            self.phone = result[4]
            self.age = result[5]
            return 1
        else:
            return 0
        
    def infoById(self, id):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.patient WHERE patient_id = %s"
            cur.execute(query, (id,))
            result = cur.fetchone()
            cur.close()
            if result:    
                self.fname = result[1]
                self.lname = result[2]
                self.email = result[3]
                self.phone = result[4]
                self.age = result[5]
                return 1
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
    
    def getClinics(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.clinic"
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            if result:
                return result
            else:
                return []
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def DocEv(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT point FROM ecp.evaluations WHERE patient_id = %s AND doctor_id = %s"
            cur.execute(query, (self.getId(), DocId))
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def update_waitingtime(self):
        try:
            cur = mysql.connection.cursor()
            query = "CALL update_waitingtime(%s)"
            id = self.getId()
            cur.execute(query, (id,))
            mysql.connection.commit()
            cur.close() 
            return 1
                
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def app_p(self):
        try:
            cur = mysql.connection.cursor()
            query = """
            SELECT appointment.appointment_id FROM appointment
            JOIN appointment_state ON appointment.appointment_id = appointment_state.appointment_id 
            WHERE appointment_state.state = 0 AND appointment.patient_id = %s  
              """
            id = self.getId()
            cur.execute(query, (id,))
            result = cur.fetchall()
            cur.close()
            todaydate = datetime.now().date()
            todaytime = datetime.now().time()
            current = []
            others = []
            appObjList = ['', '']
            if result:
                for x in result:
                    y = app_(x[0])
                    y.info(x[0])

                    objTime = (y.time + datetime.strptime('00:00:00', '%H:%M:%S')).time()
                    objendTime = (y.endtime + datetime.strptime('00:00:00', '%H:%M:%S')).time()
                    objDate = y.date
                    if objDate == todaydate:
                        if objTime <= todaytime and objendTime >= todaytime:
                            current.append(y)
                            continue
                    others.append(y)

                appObjList[0] = current
                appObjList[1] = others
                return appObjList
            else:
                return[]

        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
class app_():
    def __init__(self, id='', patientId='', doctorId='', clinicId='', date='', time='', numOfpaientBefore='', wTime='', endtime='' ):
        self.id = id
        self.patientId = patientId
        self.doctorId = doctorId
        self.clinicId = clinicId
        self.date = date
        self.time = time
        self.Before = numOfpaientBefore
        self.wTime = wTime
        self.endtime = endtime

    def create(self):
        self.time = datetime.strptime(self.time, '%H:%M:%S')
        endtime = self.time +  timedelta(minutes=30)
        self.endtime = endtime.time()
        self.time = self.time.time() 
        try:
            cur = mysql.connection.cursor()
            query = "CALL ADD_APP(%s, %s, %s, %s, %s, %s);"
            cur.execute(query, (self.patientId, self.doctorId, self.clinicId, self.date, self.time, self.endtime))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def createWithpassInfo(self, patientId, doctorId, clinicId, date, time):        
        try:
            cur = mysql.connection.cursor()
            query = "CALL ADD_APP(%s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute(query, (patientId, doctorId, clinicId, date, time))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def info(self, id):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM ecp.appointment WHERE appointment_id = %s"
            cur.execute(query, (id,))
            result = cur.fetchone()
            cur.close()
            if result:    
                self.id = result[0]
                self.patientId = result[1]
                self.doctorId = result[2]
                self.clinicId = result[3]
                self.date = result[4]
                self.time = result[5]
                self.Before = result[6]
                self.wTime = result[7]
                self.endtime = result[8]
                return 1
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def appGap(self, DocId, dateDay):
        try:
            cur = mysql.connection.cursor()
            query =  """
            SELECT appointment.time, appointment.endtime FROM appointment
            JOIN appointment_state ON appointment.appointment_id = appointment_state.appointment_id
            WHERE appointment.doctor_id = %s AND appointment.date = %s AND appointment_state.state = 0
            ORDER BY time ASC;
            """
            cur.execute(query, (DocId, dateDay))
            result = cur.fetchall()
            cur.close()
            if result:
                x = datetime.strptime('00:00:00', '%H:%M:%S')
                y = result[0][0]
                r = y + x
                r = r.time()
                
                if not(r == time(8,0,0)):
                    now = datetime.now()
                    D = datetime.strptime(dateDay, '%Y-%m-%d')
                    # cutoff_time = time(19, 0, 0)
                    # begin_time = time(8,0,0)
                    if not(now.date() == D.date()):
                        return time(8,0,0)
                   

                if len(result) < 2:
                    return False
            for i in range(len(result) - 1):
                curr_end = (result[i][1] + datetime.strptime('00:00:00', '%H:%M:%S'))
                next_start = (result[i + 1][0] + datetime.strptime('00:00:00', '%H:%M:%S'))
            
                if curr_end != next_start:
                    diff = next_start - curr_end
                    diffmin = diff.total_seconds() / 60

                    if(diffmin > 30):
                        y = curr_end.time()
                        return y
        
            return False
        
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def avTime(self, DocId, dateDay):

        gap = self.appGap(DocId, dateDay)
        if gap:
            return gap

        try:
            cur = mysql.connection.cursor()
            query =  """
            SELECT endtime FROM appointment
            JOIN appointment_state ON appointment.appointment_id = appointment_state.appointment_id
            WHERE appointment.doctor_id = %s AND appointment.date = %s AND appointment_state.state = 0
            ORDER BY endtime DESC
            LIMIT 1;
            """
            cur.execute(query, (DocId, dateDay))
            result = cur.fetchone()
            cur.close()
            now = datetime.now()
            D = datetime.strptime(dateDay, '%Y-%m-%d')
            if result:
               
                x = datetime.strptime('00:00:00', '%H:%M:%S')
                y = result[0]
                latest_endtime = y + x
                latest_endtimet = latest_endtime.time()
                cutoff_time = time(19, 0, 0)
                
                
                #The issue was is [TypeError TypeError: '<' not supported between instances of 'datetime.timedelta' and 'datetime.time']
                if latest_endtimet < cutoff_time:
                    return latest_endtimet
                else:
                    return "This day is fully booked"
            else:
                cutoff_time = time(19, 0, 0)
                begin_time = time(8,0,0)
                if now.date() == D.date() and now.time() < cutoff_time and now.time() > begin_time:
                    z = now + timedelta(minutes=30)
                    z = z.strftime("%H:%M:%S")
                    return z

                else:
                    return '08:00:00'
                
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def remove_app(self, appId):
        try:
            cur = mysql.connection.cursor()
            query = "CALL DONE_APP(%s);"
            cur.execute(query, (appId,))
            mysql.connection.commit()
            cur.close()
            return 1
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def doctorName(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT first_name, last_name  FROM ecp.doctor WHERE id = %s"
            cur.execute(query, (self.doctorId,))
            result = cur.fetchone()
            cur.close()
            if result:    
                return result[0] +" "+ result[1]
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def patientName(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT first_name, last_name  FROM ecp.patient WHERE patient_id = %s"
            cur.execute(query, (self.patientId,))
            result = cur.fetchone()
            cur.close()
            if result:    
                return result[0] +" "+ result[1]
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None
        
    def clinicName(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT name  FROM ecp.clinic WHERE clinic_id = %s"
            cur.execute(query, (self.clinicId,))
            result = cur.fetchone()
            cur.close()
            if result:    
                return result[0]
            else:
                return 0
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

    def wformat(self, per):

        houres = floor(per / 60)
        min = floor(per % 60)
        days = floor(houres / 24)
        

        return   [days, floor(houres%24), min] if days else [houres, min] if houres else [per]

    def addFive(self, DocId):
        try:
            cur = mysql.connection.cursor()
            query =  """
            UPDATE appointment a
            JOIN appointment_state a_s ON a.appointment_id = a_s.appointment_id
            SET a.time = ADDTIME(a.time, '00:05:00'), 
            a.endtime = ADDTIME(a.endtime, '00:05:00'), 
            a.waiting_time = a.waiting_time + 5
            WHERE a.doctor_id = %s 
            AND a.date = DATE(NOW())
            AND number_of_patients_before > 0
            AND a_s.state = FALSE;
            """
            cur.execute(query, (DocId,))
            mysql.connection.commit()

            query =  """
            UPDATE appointment a
            JOIN appointment_state a_s ON a.appointment_id = a_s.appointment_id
            SET a.endtime = ADDTIME(a.endtime, '00:05:00') 
            WHERE a.doctor_id = %s 
            AND a.date = DATE(NOW())
            AND number_of_patients_before = 0
            AND a_s.state = FALSE;
            """
            cur.execute(query, (DocId,))
            mysql.connection.commit()
            cur.close()           
            return 1
              
        except mysql.connect.Error as err:
            print(f"Error: {err}")
            return None

# def convertFormat(num):
#     num = num[1:]
#     num = '+218' + num
#     return num

# def send_sms(to_phone_number, message):
#     client.messages.create(
#         body=message,
#         from_=twilio_number,
#         to=to_phone_number
#     )   

# def notify_patient_if_time():
#     try:
#         cursor = mysql.connection.cursor()

#         now = datetime.now()

#         query = """
#             SELECT patient.phone_number, appointment.time, appointment.date
#             FROM appointment
#             JOIN patient ON appointment.patient_id = patient.patient_id
#             WHERE appointment.date = CURDATE() AND TIMESTAMPDIFF(MINUTE, NOW(), CONCAT(appointment.date, ' ', appointment.time)) <= 5;
#         """
#         cursor.execute(query)
#         appointments = cursor.fetchall()

#         for appointment in appointments:
#             phone_number = convertFormat(appointment[0])
#             appointment_time = appointment[1]
#             appointment_date = appointment[2]
#             message = f"Reminder: Your appointment at {appointment_time} on {appointment_date}."

#             send_sms(phone_number, message)

#         mysql.connection.commit()
        
#     except mysql.connect.Error as err:
#         print(f"Error: {err}")

# scheduler = BackgroundScheduler()
# scheduler.add_job(notify_patient_if_time, 'interval', minutes=5)
# scheduler.start()

# try:
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()

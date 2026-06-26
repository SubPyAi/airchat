import uuid
import datetime

class SessionControl:
    
    def __init__(self, db):
        self.db = db
    
    def create_session(self, uid):
        session_id = str(uuid.uuid4())
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE u_id = %s AND expired = 0", (uid,))
            if len(cursor.fetchall()) > 0:
                return None
            else:
                cursor.execute("INSERT INTO sessions (sess_id, u_id, until, expired) VALUES (%s, %s, %s, %s)", (session_id, uid, int(datetime.datetime.now().strftime("%Y%m%d"))+1, 0))
                self.db.commit()
            return session_id

    def discard_session(self, session_id):
        with self.db.cursor() as cursor:
            cursor.execute("UPDATE sessions SET expired = 1 WHERE sess_id = %s", (session_id,))
            self.db.commit()
    
    def get_sess_id(self, uid):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE u_id = %s AND expired = 0", (uid,))
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0][0]
            else:
                return None
    
    def get_uid(self, session_id):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE sess_id = %s AND expired = 0", (session_id,))
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0][1]
            else:
                return None
    
    def is_session_valid(self, session_id):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE sess_id = %s AND expired = 0", (session_id,))
            result = cursor.fetchall()
            return len(result) > 0
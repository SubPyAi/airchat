class UserControl:

    def __init__(self, db):
        self.db = db

    def db_create_user(self, userdata):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT uname FROM users WHERE uname = %s", (userdata['uname'],))
            existing_user = cursor.fetchall()
            print(existing_user)
            print(len(existing_user))
            if len(existing_user) > 1:
                return False
            else:
                query = "INSERT INTO users (uname, pwd, acc_col, status, u_id) VALUES (%s, %s, %s, %s, %s)"
                values = (userdata['uname'], userdata['pwd'], userdata['acc_col'], userdata['status'], userdata['u_id'])

                cursor = self.db.cursor()
                cursor.execute(query, values)
                self.db.commit()

                return True
    
    def db_remove_user(self, username, uid):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s AND u_id = %s", (username, uid))
            existing_user = cursor.fetchall()
            if len(existing_user) == 0:
                return False
            else:
                query = "DELETE FROM users WHERE uname = %s AND u_id = %s"
                cursor.execute(query, (username, uid))
                self.db.commit()
                return True
    
    def db_update_data(self, uid, data, key):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE u_id = %s", (uid,))
            existing_user = cursor.fetchall()
            if len(existing_user) == 0:
                return False
            else:
                query = f"UPDATE users SET {key} = %s WHERE u_id = %s"
                cursor.execute(query, (data, uid))
                self.db.commit()
                return True
    
    def db_get_uid(self, uname):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT u_id FROM users WHERE uname = %s", (uname,))
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0][0]
            else:
                return None
    
    def db_get_data(self, uid, key):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT {key} FROM users WHERE u_id = %s", (uid,))
            result = cursor.fetchall()
            if len(result) > 0:
                return result[0][0]
            else:
                return None
            
    def db_authenticate_user(self, uname, pwd):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s AND pwd = %s", (uname, pwd))
            existing_user = cursor.fetchall()
            if len(existing_user) == 0:
                return False
            else:
                return True

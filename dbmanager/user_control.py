class UserControl:

    def __init__(self, db):
        self.db = db

    def db_create_user(self, userdata):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s", (userdata['username'],))
            existing_user = cursor.fetchone()
            if existing_user:
                return False
            else:
                query = "INSERT INTO users (uname, pwd, acc_col, status, u_id) VALUES (%s, %s, %s, %s, %s)"
                values = (userdata['username'], userdata['password'], userdata['acc_col'], userdata['status'], userdata['u_id'])

                cursor = self.db.cursor()
                cursor.execute(query, values)
                self.db.commit()

                return True
    
    def db_remove_user(self, username):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s", (username,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return False
            else:
                query = "DELETE FROM users WHERE uname = %s"
                cursor.execute(query, (username,))
                self.db.commit()
                return True
    
    def db_update_data(self, uname, data, key):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s", (uname,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return False
            else:
                query = f"UPDATE users SET {key} = %s WHERE uname = %s"
                cursor.execute(query, (data, uname))
                self.db.commit()
                return True
    
    def db_get_uid(self, uname):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT u_id FROM users WHERE uname = %s", (uname,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    
    def db_get_acc_col(self, uname):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT acc_col FROM users WHERE uname = %s", (uname,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

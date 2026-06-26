import datetime

class MessageControl:
    def __init__(self, db):
        self.db = db

    def get_all_messages(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM messages ORDER BY at ASC")
            rows = cursor.fetchall()
            cols = cursor.column_names

        messages = []
        for row in rows:
            messages.append({cols[i]: row[i] for i in range(len(cols))})
        
        for i in range(len(messages)):
            messages[i]['at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return messages

    def add_message(self, data):
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (uname, msg, at, acc_col) VALUES (%s, %s, %s, %s)",
                (data.get('uname'), data.get('message'), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.get('acc_col').replace('#', ''))
            )
            self.db.commit()
    
    def get_last_message(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM messages ORDER BY at DESC LIMIT 1")
            row = cursor.fetchone()
            cursor.fetchall()
            if row:
                cols = cursor.column_names
                return {cols[i]: row[i] for i in range(len(cols))}
            return None
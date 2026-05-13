import sqlite3

class DatabaseService:
    def __init__(self, connection):
        self.connection = connection

    def get_duty_descriptions(self, duty_ids):

        number_of_duties = ', '.join(['?'] * len(duty_ids))

        query = f"SELECT Duty, Description FROM duties WHERE id IN ({number_of_duties})"

        cursor = self.connection.cursor()
        cursor.execute(query, duty_ids)
        rows = cursor.fetchall()

        return [{"Duty": row[0], "Description": row[1]} for row in rows]

    def save_duties(self, duty_ids):

        duties_to_save = [(duty_id,) for duty_id in duty_ids]

        query = f"INSERT OR IGNORE INTO saved_duties (id) VALUES (?)"

        cursor = self.connection.cursor()

        cursor.executemany(query, duties_to_save)
        self.connection.commit()

    def get_saved_duties(self):
        query = """
                SELECT duty.id, duty.Duty, duty.Description
                FROM duties duty
                         JOIN saved_duties saved ON duty.id = saved.id
                """
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        return [{"id": row[0], "Duty": row[1], "Description": row[2]} for row in rows]

    def remove_saved_duty(self, duty_id):

        query = "DELETE FROM saved_duties WHERE id = ?"

        cursor = self.connection.cursor()

        cursor.execute(query, (duty_id,))
        self.connection.commit()



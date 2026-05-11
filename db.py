import sqlite3

class DatabaseService:
    def __init__(self, connection):
        self.connection = connection

    def get_duty_descriptions(self, duty_ids):

        number_of_duties = ', '.join(['?'] * len(duty_ids))

        query = f"SELECT description FROM Duty WHERE id IN ({number_of_duties})"

        cursor = self.connection.cursor()

        cursor.execute(query, duty_ids)

        rows = cursor.fetchall()

        return [row[0] for row in rows]


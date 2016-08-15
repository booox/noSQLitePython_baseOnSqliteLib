"""
:::::::::::::::::: ParsanIT Database SQLite Library this is based on sqlite3 module  ::::::::::::::::::
:::::::::::::::::: in python3 and just use where that you don't want use sql command ::::::::::::::::::
::::::::::::::::::         NOT GOOD, BUT IS TEST PROJECT, BETTER DO NOT USE          ::::::::::::::::::
::::::::::::::::::                  ParsanIT.ir  BKHost.ir  IranPy.ir                ::::::::::::::::::
"""

import sqlite3


class SQLite3(object):
    db = None
    database_name = None
    db_opened = False

    def __init__(self, db_name):
        self.database_name = db_name
        print('A new Object of database created...')
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        if self.db_opened is False:
            self.db = sqlite3.connect(self.database_name)
            self.db_opened = True
            print('The database is connected to program.')
        else:
            print('The database was opened.')

    def close(self):
        if self.db_opened is True:
            self.db.close()
            self.db_opened = False
            print('The database disconnected from program.')
        else:
            print('The database was closed')

    def create_table(self, table_name, *fields_arg, **fields_kwarg):
        str_fields = self.__field_creator(*fields_arg, **fields_kwarg)
        self.db.execute('''CREATE TABLE {0}({1})'''.format(table_name, str_fields))

    def create_table_interactivity(self, table_name, *fields_arg, **fields_kwarg):
        str_fields = ''
        if fields_arg is not None and fields_kwarg is not None:
            str_fields = self.__field_creator(*fields_arg, **fields_kwarg)

        if str_fields != '':
            str_fields += ','

        while True:
            answer = SQLite3.check_yes(input('do you want add a new field to this table?(yes, no)'), 'yes', 'no')
            if answer == 'yes':
                str_fields = str_fields + self.__interactive_field_creator() + ','
            else:
                break

        self.db.execute('''CREATE TABLE {0}({1})'''.format(table_name, str_fields[:-1]))

    def drop_table(self, table_name):
        self.db.execute('''DROP TABLE {0}'''.format(table_name))

    def select(self, table_name, fields, where=''):
        if where == '':
            where = 'WHERE ' + where
        result = self.db.execute('''SELECT {0} FROM {1} {2}'''.format(table_name, fields, where))
        return result

    def insert(self, table_name, fields, values):
        self.db.execute('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(table_name, fields, values))
        self.db.commit()

    def delete(self, table_name, where=''):
        if where == '':
            where = 'WHERE ' + where
        self.db.execute('''DELETE FROM {0} {1}'''.format(table_name, where))
        self.db.commit()

    def update(self, table_name, field_with_value, where=''):
        if where == '':
            where = 'WHERE ' + where
        self.db.execute('''UPDATE {0} SET {1} {2}'''.format(table_name, field_with_value, where))
        self.db.commit()

    @staticmethod
    def check_yes(answer, true_answer, false_answer=''):
        """
        this method check yes answers. if answer is yes return true_answer value, else return false_answer value
        if you don't send data for false_answer function work and for other answer of else return empty string

        :param answer: string
        :param true_answer: string
        :param false_answer: string
        :return: string
        """
        answer = answer.strip()
        if answer == 'yes' or answer == 'y':
            return true_answer
        else:
            return false_answer

    @staticmethod
    def __field_creator(*fields_arg, **fields_kwarg):
        str_fields = ''
        counter = 0

        if fields_arg:
            str_fields = ','.join(fields_arg)
        else:
            for i, j in fields_kwarg:
                if len(fields_kwarg) - 1 != counter:
                    str_fields += i + ' ' + j + ','
                else:
                    str_fields += i + ' ' + j
                counter += 1

        return str_fields

    @staticmethod
    def __interactive_field_creator():
        """
        this method use for create fields interactivity

        :return: string
        """
        field_name = input('Please enter name of field: ').strip()
        field_type = input('Please enter type of field:(INTEGER, NCHAR(..), NVARCHAR, ...) ').strip()
        is_primary = SQLite3.check_yes(input('Is this field a primary key?(yes,no) ').strip(), 'PRIMARY KEY')
        autoincrement = SQLite3.check_yes(input('Is autoincrement?(yse, no) ').strip(), 'AUTOINCREMENT')
        nullable = SQLite3.check_yes(input('The field can be null?(yes, no) ').strip(), 'NULL', 'NOT NULL')
        default = input('If you want set default value for this field input here:(If no, leave blank and press Enter) ')
        if default.strip() != '':
            default = 'DEFAULT' + default
        field = [field_name, field_type, is_primary, autoincrement, nullable, default]
        field = ' '.join(field)
        return field

    def have_table(self, table_name: str=''):
        if table_name == '':
            table_name = 'AND name = {0}'.format(table_name.strip())
        result = self.db.execute('''SELECT count(*) FROM sqlite_master WHERE type = 'table' {0}'''.format(table_name))
        if int(result.fetchone()[0]) != 0:
            return True
        else:
            return False

    def sql_code_create_table(self, table_name):
        result = self.db.execute(
            '''SELECT sql FROM sqlite_master WHERE type = 'table' AND name = {0}'''.format(table_name))
        print(result)
        return result

    def execute(self, query: str):
        self.db.execute(query)

        need_commit = ['insert', 'delete', 'update']
        for needed in need_commit:
            if query.lower().startswith(needed):
                self.db.commit()

    def commit(self):
        self.db.commit()

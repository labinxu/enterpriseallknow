# from functools import total_ordering
import sqlite3
import sys
if '../' not in sys.path:
    sys.path.append('../')


class DBOperator(object):
    def __init__(self, dbname):
        self.db = sqlite3.connect(dbname)

    def execute(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()

    def select(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def getdb(self):
        return self.db


class DBHelper(DBOperator):
    _instance = None

    @staticmethod
    def getInstance(dbname=None):
        if not DBHelper._instance:
            DBHelper._instance = DBHelper(dbname)
        return DBHelper._instance

    def __init__(self, dbname):
        super(DBHelper, self).__init__(dbname)

    @staticmethod
    def reset(dbname):
        DBHelper._instance = DBHelper(dbname)


class DBException(Exception):
    def __init__(self, msg):
        self.msg = msg


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})


class Empty(object):
    pass


class NOT_PROVIDED:
    pass


class DBField(object):
    """Base class for all field types"""
    def __init__(self, name=None, max_length=None, default=NOT_PROVIDED):
        self.name = name
        self.max_length = max_length


class CharField(DBField):
    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        # self.validators.append(validators.MaxLengthValidator(self.max_length))

    def __str__(self):
        return 'varchar(%s) ' % self.max_length

def transDBRecToObject(dbret, titles):
    result = []
    for item in dbret:
        attrs = dict(zip(titles, item))
        object = type('object', (), {})()
        object.__dict__.update(attrs)
        result.append(object)
    return result


def all(cls):
    def al():
        sql = 'select * from %s_table' % cls.modelname
        #dbret = DBHelper.getInstance().select(sql)
        return None
    return al()


class ModelBase(type):
    typeMap = {}
  
    def __new__(cls, name, bases, dct):
        super_new = super(ModelBase, cls).__new__
        if (name == 'NewBase' and dct == {}) or name == 'DBModel':
            return super_new(cls, name, bases, dct)

        attrs = dict((n, value) for n,
                     value in dct.items() if not n.startswith('__'))

        dct['__table_name__'] = '%s_table' % name
        sqlstr = 'create table "%s" (' % dct['__table_name__']
        sqlstr += '"id" integer PRIMARY KEY AUTOINCREMENT, '
        titles = ['id']
        for n, var in attrs.items():
            if isinstance(var, DBField):
                titles.append(n)
                sqlstr += '"%s" %s, ' % (n, var)

        dct['__init_table__'] = '%s);' % sqlstr[:-2]

        tmptype = type('Obj%s' % name, (), {})

        setattr(tmptype, 'modelname', name)
        setattr(tmptype, 'titles', titles)
        setattr(tmptype,
                'all',
                classmethod(all))

        ModelBase.typeMap[name] = tmptype

        return super(ModelBase, cls).__new__(cls,
                                             name,
                                             bases,
                                             dct)


class DBModel(with_metaclass(ModelBase)):
    
    @classmethod
    def objects(cls):
        def ob(): 
            return cls.typeMap[cls.__name__]
        return ob()

    @staticmethod
    def getDBHelper():
        try:
            return DBHelper.getInstance()
        except Exception as e:
            pass
            # print('get DB helper error %s' % str(e))

    def __init__(self, *args, **kwargs):
        for name, var in kwargs.items():
            self.__dict__[name] = var



class Enterp(DBModel):
    name = CharField(max_length=20)

class Task(DBModel):
    name= CharField(max_length=20)

s = 'a,'
print(s[:-1])


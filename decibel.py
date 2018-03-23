# Author: Hansheng Zhao <copyrighthero@gmail.com> (https://www.zhs.me)


# import directive
__all__ = (
  '__author__', '__license__',
  '__version__', 'Decibel'
)
# package metadata
__author__ = 'Hansheng Zhao'
__license__ = 'BSD-2-Clause + MIT'
__version__ = '1.0.1'


class Result(list):
  """ Result class for Decibel results """

  __slots__ = ('_rowcount', '_lastrowid')

  def __init__(self, cursor):
    """
    Initialize list like result object
    :param cursor: database cursor instance
    """
    # acquire row count and insert id
    self._rowcount = cursor.rowcount
    self._lastrowid = cursor.lastrowid
    # fetch all remaining rows from cursor
    try:
      result = cursor.fetchall()
    except Exception:
      result = []
    super(Result, self).__init__(result)

  @property
  def rowcount(self):
    """
    Get affect row count from cursor
    :return: int, affected row count
    """
    return self._rowcount

  @property
  def lastrowid(self):
    """
    Get last insert row id from cursor
    :return: int, last insert row id
    """
    return self._lastrowid


class Decibel(object):
  """ Decibel class for easy management """

  __slots__ = ('_database', '_cursor', '_statements')

  def __init__(self, database, statements = None):
    """
    Database class constructor
    :param database: the database instance
    """
    # initialize local variables
    self._database = database
    self._cursor = database.cursor()
    self._statements = statements \
      if isinstance(statements, dict) else {}

  def __getattr__(self, item):
    """
    Acquire database attributes
    :param item: str, attribute name
    :return: mixed, function or value
    """
    return self._database.__getattribute__(item)

  def __call__(self, statement, value = None, many = False):
    """
    Call method for executing single stmt
    :param statement: str, the statement
    :param value: list|tuple|None, the values
    :param many: bool, whether execute many
    :return: list, a list of results
    """
    # acquire database cursor
    cursor = self._cursor
    # check whether values provided
    if value is None:
      cursor.execute(statement)
      result = Result(cursor)
    # check whether execute many
    elif not many:
      cursor.execute(statement, value)
      result = Result(cursor)
    else:
      # build result list from each execution
      result = [
        Result(cursor) for item in value if cursor.execute(
          statement,
          item if isinstance(item, (tuple, list)) else (item,)
        ) or True
      ]
    # commit transaction
    self._database.commit()
    return result

  # alias for call method
  #execute = __call__

  def reg(self, stid = None, stmt = None, **kwargs):
    """
    Register statements in repository
    :param stid: str|dict|None, stmt id or stmts dict
    :param stmt: str|None, stmt corresponding to stid
    :param kwargs: keyword args as k-v pairs
    :return: None
    """
    # validate statements variable and update
    if stid is not None:
      if isinstance(stid, dict):
        self._statements.update(stid)
      elif isinstance(stmt, str):
        self._statements.update({stid: stmt})
    # always update kwargs
    self._statements.update(**kwargs)

  def run(self, key, value = None, many = False):
    """
    Execute a stored statement with value
    :param key: the statement id
    :param value: the optional values
    :param many: bool, whether execute many
    :return: list, a list of result instances
    """
    # check if key supplied and exist
    if key not in self._statements: return []
    # acquire statement from repo
    statement = self._statements[key]
    # invoke __call__ method
    return self(statement, value, many)

  def close(self):
    """
    Commit, sync and close database
    :return: None
    """
    # acquire database instance
    database = self._database
    # commit uncommitted changes
    database.commit()
    # sync database to disk
    if hasattr(database, 'sync'):
      database.sync()
    # close database connection
    if hasattr(database, 'close'):
      database.close()

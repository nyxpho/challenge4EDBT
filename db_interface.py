import psycopg2

import config

class DatabaseError(Exception):
	"""
	Any error related to *the content* of the database, for instance missing
	values or duplicates. *Should not* be used for technical errors such as
	failure to connect to the database.
	"""
	pass

class DatabaseInterface(object):
	"""
	Centralized communication with the database
		
	"""
	def __init__(self):
		self.connection = psycopg2.connect(
			database=config.POSTGRES_DATABASE,
			user=config.POSTGRES_USER,
			password=config.POSTGRES_PASS)
		self.cursor = self.connection.cursor()
	
	def commit(self):
		self.connection.commit()
	
	def release(self):
		"""
		Closes the connection to the database
		"""
		self.connection.commit()
		self.cursor.close()
		self.connection.close()
	
	def _execute(self, query, values=None):
		self.cursor.execute(query, values)
	
	def _get_one_item_query(self, query, values = None):
		"""
		Execute and returns the first result of a query expecting at least one
		result
		"""
		self.cursor.execute(query, values)
		potential = self.cursor.fetchone()
		
		if potential is not None:
			return potential[0]
		else:
			raise DatabaseError()
	
	def _get_special_cursor_iterator(self, query, values = None):
		"""
		Return an iterator over the result of a query, is thread safe
		"""
		special_cursor = self.connection.cursor()
		special_cursor.execute(query, values)
		for couple in special_cursor:
			yield couple
		special_cursor.close()


class WikipediaDatabaseInterface(DatabaseInterface):
	
	_select_text_body = ("SELECT body FROM " + config.BODY_TABLE +
		" WHERE index = %s")
	
	def get_body_text_by_index(self, index):
		"""
		Return the body of the article with this index (raise a DatabaseError otherwise)
		"""
		return self._get_one_item_query(self._select_text_body, (index,))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to interact with the database storing the Wikipedia data
"""

from os import path

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
	"""
	The interface to access the Wikipedia database
	"""
	
	def create_tables(self, autodrop=False):
		"""
		Creates the (empty) table to store the Wikipedia data
		"""
		#id - title
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.ARTICLE_ID_TABLE)
		self._execute("CREATE TABLE %s (index bigint PRIMARY KEY, title text)" %config.ARTICLE_ID_TABLE)
		self._execute("CREATE UNIQUE INDEX ON %s (title)" %config.ARTICLE_ID_TABLE)
		
		#body
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.BODY_TABLE)
		self._execute("CREATE TABLE %s (index bigint PRIMARY KEY, body text)" %config.BODY_TABLE)
		
		#links
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.LINK_TABLE)
		self._execute("CREATE TABLE %s (article_from text, article_to text)" %config.LINK_TABLE)
		self._execute("ALTER TABLE %s ADD CONSTRAINT "
			"chal4_link_pk PRIMARY KEY (article_from, article_to)" %config.LINK_TABLE)
		self._execute("CREATE INDEX ON %s (article_from)" %config.LINK_TABLE)
		self._execute("CREATE INDEX ON %s (article_to)" %config.LINK_TABLE)
		
		#category id - title
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.CATEGORY_ID_TABLE)
		self._execute("CREATE TABLE %s (cat_index bigint PRIMARY KEY, cat_title text)" %config.CATEGORY_ID_TABLE)
		self._execute("CREATE UNIQUE INDEX ON %s (cat_title)" %config.CATEGORY_ID_TABLE)
		
		#article - category
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.ARTICLE_CATEGORY_TABLE)
		self._execute("CREATE TABLE %s (index bigint NOT NULL, cat_index bigint NOT NULL)" %config.ARTICLE_CATEGORY_TABLE)
		self._execute("ALTER TABLE %s ADD CONSTRAINT "
			"chal4_art_cat_pk PRIMARY KEY (index, cat_index)" %config.ARTICLE_CATEGORY_TABLE)
		
		#subcategory - category
		if autodrop: self._execute("DROP TABLE IF EXISTS %s" %config.SUBCATEGORY_TABLE)
		self._execute("CREATE TABLE %s (sub_cat bigint NOT NULL, super_cat bigint NOT NULL)" %config.SUBCATEGORY_TABLE)
		self._execute("ALTER TABLE %s ADD CONSTRAINT "
			"chal4_subcat_pk PRIMARY KEY (sub_cat, super_cat)" %config.SUBCATEGORY_TABLE)
		
		self.commit()
	
	def populate_tables(self, csv_path):
		"""
		Use the csv files to populate the tables
		
		@Warning: this suppose that the files are correctl formated WHICH IS NOT
		THE CASE OF THE FILES IN THE ARCHIVES. YOU SHOULD PROBABLY s/\x00/ and
		article_body and then remove the lastline of each csv
		"""
		csv_path = path.abspath(csv_path)
		
		#id - title
		self._execute("COPY %s FROM '%s'DELIMITER ',' CSV"
			%(config.ARTICLE_ID_TABLE, path.join(csv_path,'articles_ids.csv'))
		)
		
		#TODO:continue
		##body
		#config.BODY_TABLE (index bigint PRIMARY KEY, body text)
		#
		##links
		# config.LINK_TABLE (article_from text, article_to text)
		#
		##category id - title
		#config.CATEGORY_ID_TABLE (cat_index bigint PRIMARY KEY, cat_title text)
		#
		##article - category
		# config.ARTICLE_CATEGORY_TABLE (index bigint NOT NULL, cat_index bigint NOT NULL)
		#
		##subcategory - category
		#config.SUBCATEGORY_TABLE (sub_cat bigint NOT NULL, super_cat bigint NOT NULL)
		
		self.commit()
	
	
	_select_random_article_query = ("SELECT , FROM %s OFFSET random() * "
		"(SELECT count(*) FROM %s) LIMIT 1 "
		%(config.ARTICLE_ID_TABLE, config.ARTICLE_ID_TABLE)
	)
	
	def get_random_article(self):
		"""
		Returns the (index, title) of a random article
		"""
		return self._get_one_item_query(self._select_random_article_query)
	
	
	_select_article_index_query = ("SELECT index FROM " + config.ARTICLE_ID_TABLE +
		" WHERE title = %s")
	
	def get_article_index_from_title(self, title):
		return self._get_one_item_query(self._select_article_index_query, (title,))
	
	
	_select_share_inlink_query = (
		"SELECT ln2.article_to FROM "+ config.LINK_TABLE + " ln1 "
		"JOIN " + config.LINK_TABLE + " ln2 ON ln1.article_from = ln2.article_from "
		"WHERE ln1.article_to = %s"
	)
	
	def get_share_inlink(self, index):
		"""
		Returns an iterator on articles that share an inlink with the article 'index'
		"""
		return self._get_special_cursor_iterator(self._select_share_inlink_query, (index,))
	
	
	_select_share_outlink_query = (
		"SELECT ln2.article_from FROM "+ config.LINK_TABLE + " ln1 "
		"JOIN " + config.LINK_TABLE + " ln2 ON ln1.article_to = ln2.article_to "
		"WHERE ln1.article_from = %s"
	)
	
	def get_share_outlink(self, index):
		"""
		Returns an iterator on articles that share an outlink with the article 'index'
		"""
		return self._get_special_cursor_iterator(self._select_share_outlink_query, (index,))
	
	
	_select_text_body_query = ("SELECT body FROM " + config.BODY_TABLE +
		" WHERE index = %s")
	
	def get_body_text_by_index(self, index):
		"""
		Returns the body of the article with this index (raise a DatabaseError otherwise)
		"""
		return self._get_one_item_query(self._select_text_body_query, (index,))

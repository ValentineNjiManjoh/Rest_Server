#!/urs/bin/env python3

import unittest
from app import search_movie

class MyTest(unittest.TestCase):
	def test(self):
		status=search_movie('titanic')
		self.assertEqual(status,1)


if(__name__ == '__app__'):
    	unittest.main()

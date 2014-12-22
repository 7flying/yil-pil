# -*- coding: utf-8 -*-
import os
import unittest
import coverage

COV = None
COV = coverage.coverage(branch=True, include='app/*')
COV.start()

def test(coverage=False):
	""" Runs the unit tests. """
	tests = unittest.TestLoader().discover('tests', pattern ='*.py')
	unittest.TextTestRunner(verbosity=2).run(tests)
	if COV:
		COV.stop()
		COV.save()
		print "Coverage Summary:"
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.html_report(directory=covdir)
		COV.erase()

if __name__ == '__main__':
	test(True)

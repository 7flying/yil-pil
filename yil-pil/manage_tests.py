# -*- coding: utf-8 -*-
import os
import unittest
import coverage

def test(cover=False):
    """ Runs the unit tests. """
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    if cover:
        cov = coverage.coverage(branch=True, include='app/*')
        cov.start()
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cover:
        cov.stop()
        cov.save()
        print "Coverage Summary:"
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        cov.erase()

if __name__ == '__main__':
    test(True)

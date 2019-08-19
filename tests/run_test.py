import unittest
from tests.HTMLTestRunner import HTMLTestRunner

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*test_*.py')

if __name__ == '__main__':
    with open('HtmlReport.html', 'wb') as f:
        runner = HTMLTestRunner(stream=f, title='test report', description='', verbosity=2)
        runner.run(discover)

    # with open('UnittestTextReport.txt', 'a') as f:
    #     runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #     runner.run(discover)

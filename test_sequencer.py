import sys

# "Test" is a function. It takes no arguments and returns any encountered errors.
# If there is no error, test should return 'None'. Tests shouldn't have any dependencies
# amongst themselves.


def run(tests):
    """If no arguments (sys.argv) are given, runs tests. If there are any arguments they are
       interpreted as names of tests to actually run, it will skip other tests"""

    filter = set(sys.argv[1:])
    if len(filter) > 0:
        to_run = []
        for test in tests:
            if test.__name__ in filter:
                to_run.append(test)
        tests = to_run

    print '=> Going to run {0} tests'.format(len(tests))
    ok = []
    fail = []
    for number, test in enumerate(tests):
        print '\t-> [{0}/{1}] {2} ({3})'.format(number, len(tests), test.__name__, test.__doc__)
        error = test()
        if error is None:
            ok.append((number, test))
        else:
            fail.append((number, test, error))

    print ''
    print 'RESULTS'
    print '\tOK: {0}'.format(len(ok))
    print '\tFAILED: {0}'.format(len(fail))
    if len(fail) > 0:
        print ''
        print '--- Failures ---'
        for number, test, error in fail:
            print 'Test {0} - {1} ({2})\n{3}'.format(number, test.__name__, test.__doc__, error)


def ask(question):
    answer = None
    while True:
        print '\t\t-? {0} [Y/N]'.format(question),
        answer = raw_input()
        if answer.strip().upper() == 'Y' or answer.strip().upper() == 'N':
            break
    return True if answer.strip().upper() == 'Y' else False

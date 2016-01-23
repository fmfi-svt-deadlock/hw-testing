import sys

# "Test" is a function. It takes no arguments and returns any encountered errors.
# If there is no error, test should return 'None'. Tests shouldn't have any dependencies
# amongst themselves.


def run(tests):
    """Runs appropriate tests.

    If no arguments (sys.argv) are given, runs all tests in `tests`.
    If there are any arguments they are interpreted as names of tests to
    actually run, it will skip other tests.
    """

    selected_tests = set(sys.argv[1:])
    if selected_tests:
        to_run = [t for t in tests if t.__name__ in selected_tests]
        tests = to_run

    print '=> Going to run {} tests'.format(len(tests))
    ok = []
    fail = []
    for number, test in enumerate(tests):
        print '\t-> [{num}/{total}] {name} ({doc})'.format(num=number+1, total=len(tests),
                                                           name=test.__name__, doc=test.__doc__.splitlines()[0])
        error = test()
        if error is None:
            ok.append((number, test))
        else:
            fail.append((number, test, error))

    print ''
    print 'RESULTS'
    print '\tOK: {}'.format(len(ok))
    print '\tFAILED: {}'.format(len(fail))
    if len(fail) > 0:
        print ''
        print '------------- FAILURES -------------'
        for number, test, error in fail:
            print '\nTest {number} - {name}\n{doc}\n{err}'.format(number=number+1, name=test.__name__,
                                                                 doc=test.__doc__, err=error)
            print '------------------------------------'


def ask_YN(question):
    answer = None
    while True:
        print '\t\t-? {0} [Y/N]'.format(question),
        answer = raw_input()
        if answer.strip().upper() in ['Y', 'N']:
            break
    return answer.strip().upper() == 'Y'


def ask(question):
    print '\t\t-? {0}:'.format(question),
    return raw_input()


def say(something):
    print '\t\t- {0}'.format(something)

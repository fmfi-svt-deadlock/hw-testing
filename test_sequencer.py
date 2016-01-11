def run(tests):
    print '=> Going to run', len(tests), 'tests'
    ok = []
    fail = []
    for number, test in enumerate(tests):
        print '\t-> [' + str(number) + '/' + str(len(tests)) + ']', test.__doc__
        error = test()
        if error is None:
            ok.append((number, test))
        else:
            fail.append((number, test, error))

    print ''
    print 'RESULTS'
    print '\tOK: ' + str(len(ok))
    print '\tFAILED: ' + str(len(fail))
    if len(fail) > 0:
        print ''
        print '--- Failures ---'
        for number, test, error in fail:
            print 'Test ' + str(number) + ' - ' + test.__name__ + ' (' + test.__doc__ + '):'
            print str(error)


def ask(question):
    answer = None
    while True:
        print '\t\t-?', question, '[Y/N]',
        answer = raw_input()
        if answer.strip().upper() == 'Y' or answer.strip().upper() == 'N':
            break
    return True if answer.strip().upper() == 'Y' else False

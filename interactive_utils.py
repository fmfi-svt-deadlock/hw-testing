import code


# TODO this will be rewritten as a part of the new register interface
def reg(number, flags_dict=None):
    print hex(number)
    print ''

    bits = [int(bit) for bit in bin(number)[2:]]
    flags = [(bit, '') for bit in bits]
    if len(flags) % 4 != 0:
        flags = ([(0, '')]*(4 - (len(flags) % 4))) + flags

    if flags_dict is not None:
        for flag, bit in flags_dict.items():
            try:
                if (len(flags) - bit - 1) >= 0:
                    val = flags[len(flags) - bit - 1][0]
                    flags[len(flags) - bit - 1] = (val, flag)
            except IndexError:
                pass

    flags_to_print = []
    max_length = 0

    for i, flag in enumerate(flags):
        bit_num = len(flags) - i - 1
        if len(flags_to_print) < (i/4)+1:
            flags_to_print.append([])
        flag_str = '[{bit}] ({flag_name}): {value}'.format(bit=bit_num, flag_name=flag[1],
                                                           value=flag[0])
        flags_to_print[i/4].append(flag_str)
        max_length = max(max_length, len(flag_str))

    space = max_length + 2

    print '0x ', ''.join(['{}{}'.format(x, ' '*(space-len(x))) for x in hex(number)[2:]])
    print '0b ', ''.join(['{}{}'.format(x, ' '*(space-len(x)))
                          for x in [''.join(str(f[0])
                                            for f in flags[y:y+4])
                                    for y in range(0, len(flags), 4)]])

    print ''

    for i in range(0, 4):
        print '   ',
        for line in flags_to_print:
            print line[i] + (' '*(space-len(line[i])-1)),
        print ''


vars = globals()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()

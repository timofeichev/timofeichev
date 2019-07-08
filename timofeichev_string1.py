# A. donuts
def donuts(count):
    if count >= 10:
        a = 'много'
    else:
        a = count
    return 'Количество пончиков:{}'.format(a)


# B. both_ends
def both_ends(s):
    if len(s) < 2:
        a = s[:0]
    else:
        a = s[:2] + s[-2:]
    return a


# C. fix_start
def fix_start(s):
    if len(s) >= 1:
        a = s[0]
        b = s[1:]
        if a in b:
            b = b.replace(a, '*')
    return a + b


# D. MixUp
def mix_up(a, b):
    if len(a) and len(b) >= 2:
        c = b[0:2] + a[2:] + ' ' + a[0:2] + b[2:]
    return c


# tests
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


def main():
    print('donuts')
    test(donuts(4), 'Количество пончиков:4')
    test(donuts(9), 'Количество пончиков:9')
    test(donuts(10), 'Количество пончиков:много')
    test(donuts(99), 'Количество пончиков:много')

    print('both_ends')
    test(both_ends('spring'), 'spng')
    test(both_ends('Hello'), 'Helo')
    test(both_ends('a'), '')
    test(both_ends('xyz'), 'xyyz')

    print('fix_start')
    test(fix_start('babble'), 'ba**le')
    test(fix_start('aardvark'), 'a*rdv*rk')
    test(fix_start('google'), 'goo*le')
    test(fix_start('donut'), 'donut')

    print('mix_up')
    test(mix_up('mix', 'pod'), 'pox mid')
    test(mix_up('dog', 'dinner'), 'dig donner')
    test(mix_up('gnash', 'sport'), 'spash gnort')
    test(mix_up('pezzy', 'firm'), 'fizzy perm')


if __name__ == '__main__':
    main()


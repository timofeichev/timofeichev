# 1
def donuts(count):
    if count >= 10:
        a = 'много'
    else:
        a = count
    return 'Количество пончиков:{}'.format(a)


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


def main():
    print('пончики')
    test(donuts(4), 'Количество пончиков:4')
    test(donuts(9), 'Количество пончиков:9')
    test(donuts(10), 'Количество пончиков:много')
    test(donuts(99), 'Количество пончиков:много')


if __name__ == '__main__':
    main()
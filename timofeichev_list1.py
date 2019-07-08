# A. match_ends
def match_ends(words):
    sum = 0
    for word in words:
        if len(word) >= 2 and word[0] == word[-1]:
            sum += 1
    return sum


# B. front_x
def front_x(words):
    words1 = []
    words2 = []
    for word in words:
        if 'x' in word[0]:
            words1.append(word)
            a = sorted(words1)
        elif 'x' not in word[0]:
            words2.append(word)
            b = sorted(words2)
    return a + b


# C.1 sort_last
def sort_last(tuples):
    def MyFn(s):
        return s[-1]

    a = sorted(tuples, key=MyFn)
    return a


# C.2 sort_last
# def sort_last(tuples):
# a = sorted(tuples, key = lambda x: x[-1])
# return a


# tests
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


def main():
    print('match_ends')
    test(match_ends(['aba', 'xyz', 'aa', 'x', 'bbb']), 3)
    test(match_ends(['', 'x', 'xy', 'xyx', 'xx']), 2)
    test(match_ends(['aaa', 'be', 'abc', 'hello']), 1)

    print('front_x')
    test(front_x(['bbb', 'ccc', 'axx', 'xzz', 'xaa']),
         ['xaa', 'xzz', 'axx', 'bbb', 'ccc'])
    test(front_x(['ccc', 'bbb', 'aaa', 'xcc', 'xaa']),
         ['xaa', 'xcc', 'aaa', 'bbb', 'ccc'])
    test(front_x(['mix', 'xyz', 'apple', 'xanadu', 'aardvark']),
         ['xanadu', 'xyz', 'aardvark', 'apple', 'mix'])

    print('sort_last')
    test(sort_last([(1, 3), (3, 2), (2, 1)]),
         [(2, 1), (3, 2), (1, 3)])
    test(sort_last([(2, 3), (1, 2), (3, 1)]),
         [(3, 1), (1, 2), (2, 3)])
    test(sort_last([(1, 7), (1, 3), (3, 4, 5), (2, 2)]),
         [(2, 2), (1, 3), (3, 4, 5), (1, 7)])


if __name__ == '__main__':
    main()



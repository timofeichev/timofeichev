import sys

filename = open('filename.txt', 'w')
filename.write('Копытные животные привет зимой поедают молодые еловые побеги. '
               'А между корней зеленой елки медведи привет выкапывают свои берлоги.'
               'Свои берлоги привлекают Грибы грибы лесных обитателей к елям еще грибы '
               'которым нравится животные расти рядом с корневой системой этих деревьев.')
filename.close()

def wordcount(filename):
    filename = open('filename.txt')
    filename1 = filename.read()
    filename2 = filename1.lower()
    filename3 = filename2.split()
    for words in filename3:
        c = filename3.count(words)
        yield words, c
    filename.close()


def print_words(filename):
    d = dict(wordcount(filename))
    for key in sorted(d.keys()):
        print(key, d[key])


def print_top(filename):
    d = dict(wordcount(filename))
    def MyFn(s):
        return s[-1]
    d1 = sorted(d.items(), key = MyFn, reverse = True)
    for item in d1[0:20]:
        print(item[0], item[1])


def main():
    if len(sys.argv) != 3:
        print ('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print ('unknown option: ' + option)
        sys.exit(1)

if __name__ == '__main__':
    main()
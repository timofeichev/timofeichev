import sys

def wordcount(filename):
    filename = open(filename)
    word_string = filename.read()
    word_list = word_string.lower().split()
    word_dict = {}
    for word in word_list:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] = word_dict[word] + 1
    filename.close()
    return word_dict


def print_words(filename):
    word_dict = wordcount(filename)
    for key in sorted(word_dict.keys()):
        print(key, word_dict[key])


def print_top(filename):
    word_dict = wordcount(filename)
    def my_count(s):
        return s[1]
    items = sorted(word_dict.items(), key = my_count, reverse = True)
    for item in items[0:20]:
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
import sys
import re

def extract_names(filename):
    names = []
    filename = open(filename)
    text = filename.read()
    match_year = re.search(r'(Popularity in)\s*(\d\d\d\d)', text)
    if match_year:
        names.append(match_year.group(2))
    else:
        print('Not found')
    match_names = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)', text)
    match_names_dict = {}
    for name in match_names:
        if name[1] not in match_names_dict:
            match_names_dict[name[1]] = name[0]
        if name[2] not in match_names_dict:
            match_names_dict[name[2]] = name[0]
    sorted_match_names = sorted(match_names_dict.keys())
    for name in sorted_match_names:
        names.append(name + ' ' + match_names_dict[name])
    return names


def main():
    args = sys.argv[1:]
    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]
    for filename in args:
        names = extract_names(filename)
        text = '\n'.join(names)
        if summary:
            outf = open(filename + '.summary', 'w')
            outf.write(text + '\n')
            outf.close()
        else:
            print(text)


if __name__ == '__main__':
    main()

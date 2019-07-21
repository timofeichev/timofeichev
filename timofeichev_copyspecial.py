import os
import sys
import re
import shutil
import commands


def get_special_paths(dirname):
    result = []
    paths = os.listdir(dirname)
    for fname in paths:
        match = re.search(r'__(\w+)__', fname)
        if match:
            result.append(os.path.abspath(os.path.join(dirname, fname)))
    return result


def copy_to(paths, to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    for path in paths:
        fname = os.path.basename(path)
        shutil.copy(path, os.path.join(to_dir, fname))
        #shutil.copy(path, to_dir)


def zip_to(paths, zipfile):
    cmd = 'zip -j ' + zipfile + ' ' + ' '.join(paths)
    print ("Command I'm going to do:" + cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        sys.stderr.write(output)
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args:
        print ("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print ("error: must specify one or more dirs")
        sys.exit(1)


    paths = []
    for dirname in args:
        paths.extend(get_special_paths(dirname))

    if todir:
        copy_to(paths, todir)
    elif tozip:
        zip_to(paths, tozip)
    else:
        print ('\n'.join(paths))


if __name__ == "__main__":
  main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser
import re

default_pattern = (
    'Thumbs.db',
    'desktop.ini',
    '.DS_Store',
    '__MACOSX',
    '.AppleDouble',
    '._*',
)

dirname = os.path.dirname(os.path.abspath(__file__))
config_filename = os.path.join(dirname, '.dtf.conf')

def run(mode):

    def scanning(target, patterns):
        files = os.listdir(target)
        for file in files:
            flag = 0
            for pattern in patterns:
                if pattern.find('*') != -1:
                    attern = pattern.replace('.', '\.')
                    pattern = pattern.replace('*', '(.*)')
                    result = re.match(pattern, file)
                    if result:
                        flag = 1
                else:
                    if pattern == file:
                        flag = 1
            filename = os.path.join(target, file)
            if flag == 1:
                print 'delete: %s' % filename
                if mode == 'preview':
                    continue
                if os.path.isdir(filename):
                    for root, dirs, files in os.walk(filename, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(filename)
                else:
                    os.remove(filename)
            else:
                if os.path.isdir(filename):
                    scanning(filename, patterns)

    if mode == 'show' or mode == 'list':
        mode = 'preview'
    patterns = default_pattern
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(os.path.join(dirname, '.dtf.conf'));
    except Exception, e:
        print 'error: ', e
        quit()
    try:
        pattern_str = config.get('config', 'pattern')
        patterns = pattern_str.split(',')
    except Exception, e:
        # config nothing. use default_pattern.
        pass
    scanning(dirname, patterns)
    return


def add_pattern(str):
    """
    add pattern
    """
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_filename)
    except Exception, e:
        print 'error: ', e
        quit()
    try:
        pattern = config.get('config', 'pattern')
    except Exception, e:
        print 'error: config file is broken.'
        quit()
    arr = pattern.split(',')
    if not str in arr:
        arr.append(str)
    config.set('config', 'pattern', ','.join(arr))
    config.write(open(config_filename, 'w'))
    print "##### pattern"
    print arr
    print "#####"


def del_pattern(str):
    """
    add pattern
    """
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_filename)
    except Exception, e:
        print 'error: ', e
        quit()
    try:
        pattern = config.get('config', 'pattern')
    except Exception, e:
        print 'error: config file is broken.'
        quit()
    arr = pattern.split(',')
    if str in arr:
        arr.remove(str)
    config.set('config', 'pattern', ','.join(arr))
    config.write(open(config_filename, 'w'))
    print "##### pattern"
    print arr
    print "#####"


def show_pattern():
    """
    show pattern
    """
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_filename)
    except Exception, e:
        print 'error: ', e
        quit()
    try:
        pattern = config.get('config', 'pattern')
    except Exception, e:
        print 'error: config file is broken.'
        quit()
    arr = pattern.split(',')
    print "##### pattern"
    print arr
    print "#####"


def init_config():
    f = open(config_filename, 'w')
    f.write("[config]\n")
    f.write('pattern = ' + ','.join(default_pattern))
    f.close()


def main():
    """
    main method
    """
    argv = sys.argv
    argc = len(argv)

    # configfile check
    if not os.path.isfile(config_filename):
        init_config()

    if argc == 1:
        run('')
        return

    if argv[1] == 'config' or argv[1] == 'pattern':
        show_pattern()
        quit()

    if argv[1] == 'show' or argv[1] == 'list' or argv[1] == 'preview':
        run('preview')
        return

    if argv[1] == 'add':
        if argc < 3:
            print 'Usage: # python %s [add] [pattern]' % argv[0]
            quit()
        add_pattern(argv[2])

    if argv[1] == 'del':
        if argc < 3:
            print 'Usage: # python %s [del] [pattern]' % argv[0]
            quit()
        del_pattern(argv[2])


if __name__ == '__main__':
    main()


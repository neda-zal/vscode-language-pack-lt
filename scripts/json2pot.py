#!/usr/bin/python3

import json
import sys

def main(source, target):
    with open(source) as fp:
        data = json.load(fp)
    with open(target, 'w') as fp:
        fp.write(r'''
msgid ""
msgstr ""
"Language: English\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
"X-Generator: PhraseApp (phraseapp.com)\n"

''')
        for key, value in data.items():
            fp.write('#: {}\n'.format(key))
            fp.write('msgctxt "{}"\n'.format(key))
            fp.write('msgid "{}"\n'.format(value))
            fp.write('msgstr ""\n\n')

if __name__ == '__main__':
    main(*sys.argv[1:])
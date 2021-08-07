#!/usr/bin/python

import json
import sys

def fix_msgstr(msgstr):
    if msgstr[0] == '"':
        msgstr = '„' + msgstr[1:]
    if msgstr[-1] == '"':
        msgstr = msgstr[:-1] + '“'
    msgstr = msgstr.replace(' \\"', ' „').replace(' "', ' „')
    msgstr = msgstr.replace('\\" ', '“ ').replace('" ', '“ ')
    return msgstr

def main(templace_file, po_file, target_file):
    with open(templace_file) as fp:
        template = json.load(fp)

    po_translations = {}
    with open(po_file) as fp:
        state = {}
        for line in fp:
            if line.isspace() or line == '\n':
                if 'loc' in state:
                    msgstr = ''.join(state['msgstr'])
                    if msgstr:
                        po_translations[state['loc']] = fix_msgstr(msgstr)
                state = {}
            elif line.startswith("#: "):
                state['loc'] = line[3:-1]
            elif line.startswith("msgctxt"):
                pass
            elif line.startswith("msgid"):
                state['current'] = 'msgid'
            elif line.startswith("msgstr"):
                state['current'] = 'msgstr'
                state['msgstr'] = [line[8:-2]]
            elif line.startswith('"'):
                if state['current'] == "msgstr":
                    state['msgstr'].append(line[1:-1])
            else:
                assert False, '„{}“ {}'.format(line, len(line))
        msgstr = ''.join(state['msgstr'])
        po_translations[state['loc']] = fix_msgstr(msgstr)

    translations = {}
    for key, value in template.items():
        if key in po_translations:
            translations[key] = po_translations[key]
        else:
            print("Warning: missing key", key)
            translations[key] = value

    with open(target_file, 'w') as fp:
        json.dump(translations, fp, indent='\t')


if __name__ == '__main__':
    main(*sys.argv[1:])

#!/usr/bin/python3

from glob import glob
import json
import os
from xml.etree import ElementTree

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SOURCE_DIR = os.path.join(REPO_ROOT, 'xliff')
OUTPUT_DIR = os.path.join(REPO_ROOT, 'translations')

def collect_sources(dir_name):
    pattern = os.path.join(SOURCE_DIR, dir_name, '*.xlf')
    return glob(pattern)

def generate(target_file, input_files):
    assert len(input_files) > 0
    input_files.sort()
    target_path = os.path.join(OUTPUT_DIR, target_file)
    contents = {}
    for input_file in input_files:
        print("Processing ", input_file)
        tree = ElementTree.parse(input_file)
        root = tree.getroot()
        assert root.tag == '{urn:oasis:names:tc:xliff:document:1.2}xliff'
        for file in root:
            assert file.tag == '{urn:oasis:names:tc:xliff:document:1.2}file'
            original = file.get('original')
            assert original.startswith('src/')
            location = original[4:]
            file_contents = {}
            for trans_unit in file.find('{urn:oasis:names:tc:xliff:document:1.2}body'):
                assert trans_unit.tag == '{urn:oasis:names:tc:xliff:document:1.2}trans-unit'
                translation = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}target')
                id = trans_unit.get('id')
                assert id not in file_contents
                if translation is not None:
                    file_contents[id] = translation.text
                else:
                    source = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}source')
                    file_contents[id] = source.text
            assert original not in contents
            contents[original] = file_contents
    data = {
	"version": "1.0.0",
	"contents": contents,
    }
    with open(target_path, 'w') as fp:
        json.dump(data, fp, indent='\t')

def main():
    generate(
        'main.i18n.json',
        collect_sources('vscode-editor') + collect_sources('vscode-workbench')
    )


if __name__ == "__main__":
    main()

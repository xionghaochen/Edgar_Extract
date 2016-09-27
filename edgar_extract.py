'''
Created on Sep 2, 2016

@author: walter
'''
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Walter Xiong'

import os
import shutil
import sys

def main():

    for dirpath, dirnames, filenames in os.walk(os.path.abspath('.')):

        for filename in filenames:

            if os.path.splitext(filename)[1] == '.idx':

                if os.path.splitext(filename)[0] in dirnames:
                    original_dir = os.path.join(os.path.abspath('.'), os.path.splitext(filename)[0] + '_CLEANED')
                    extracted_dir = os.path.join(os.path.abspath('.'), os.path.splitext(filename)[0] + '_EXTRACTED')

                    if os.path.isdir(extracted_dir):
                        shutil.rmtree(extracted_dir)

                    if not os.path.isdir(extracted_dir):
                        os.mkdir(extracted_dir)

                else:
                    sys.exit('Error: Original directory %r cannot found' % os.path.splitext(filename)[0])

    traverse_folders(original_dir, extracted_dir)

def traverse_folders(original_dir, extracted_dir):

    original_folders = os.listdir(original_dir)

    count = 0

    for f in original_folders:

        if f == '.DS_Store' or os.path.splitext(f)[1].lower() == '.swp':
            continue

        if os.path.splitext(f)[1].lower() == '.pdf' or os.path.splitext(f)[1].lower() == '.xml' or os.path.splitext(f)[1].lower() == '.paper':
            shutil.copy(os.path.join(original_dir, f), extracted_dir)
            continue

        if os.path.splitext(f)[1].lower() == '.txt':
            count = count + 1
            print f
            print str(count) + ' of ' + str(len(original_folders))

            extract_txt_file(original_dir, extracted_dir, f)

        else:
            print ' Processing ' + f + ' ...\n'

            if not os.path.isdir(os.path.join(extracted_dir, f)):
                os.mkdir(os.path.join(extracted_dir, f))
                os.mkdir(os.path.join(os.path.join(extracted_dir, f), 'Manual_Clean'))

            traverse_folders(os.path.join(original_dir,f),os.path.join(extracted_dir,f))


def extract_txt_file(original_dir, extracted_dir, f):

    text_content = open(os.path.join(original_dir,f))
    temp_file = open(os.path.join(extracted_dir, f), 'w')

    for i in range(0,4):
        content_line = text_content.readline()
        temp_file.write(content_line)

    temp_file.write('\n')
    content_line =text_content.readline()

    while content_line != '':

        item_check = content_line.lower().find('item')

        stop_signal = False

        if item_check != -1:

            if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1business\n', 'itemibusiness\n', 'item1descriptionofbusiness\n', 'item1descriptionofthebusiness\n', 'item1businessoverview\n', 'item1overviewofthebusiness\n', 'item1and2businessandproperties\n', 'item1and2businessandproperty\n', 'item1anditem2businessandproperties\n', 'item1anditem2businessandproperty\n', 'items1and2businessandproperties\n', 'items1and2businessandproperty\n', 'items1&2businessandproperties\n', 'items1&2businessandproperty\n', 'partiitem1business\n'):
                temp_line_first = content_line
                content_line = text_content.readline()

                # Skip catalog
                if content_line.lower().replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').rstrip('\n').replace('i', '').replace('[', '').replace(']', '').replace('page', '').replace(',', '').isdigit():
                    content_line = text_content.readline()

                elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1a\n', 'item2\n', 'item\n', 'item3\n', 'item1ariskfactors\n', 'item2properties\n', 'item2property\n', 'item2descriptionofproperties\n', 'item2descriptionofproperty\n', 'item3legalproceedings\n', 'partiitem1ariskfactors\n', 'partiitem1bunresolvedstaffcomments\n', 'partiitem2property\n', 'partiitem2properties\n'):
                    content_line = text_content.readline()

                elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('\n', ):
                    temp_line_second = content_line
                    content_line =text_content.readline()

                    if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1ariskfactors\n', 'item1bunresolvedstaffcomments\n', 'item2properties\n', 'item2property\n', 'item2descriptionofproperties\n', 'item2descriptionofproperty\n', 'item3legalproceedings\n', 'partiitem1ariskfactors\n', 'partiitem1bunresolvedstaffcomments\n', 'partiitem2property\n', 'partiitem2properties\n'):
                        content_line = text_content.readline()

                    else:
                        temp_file.write(temp_line_first)
                        temp_file.write(temp_line_second)
                        temp_file.write(content_line)
                        content_line = text_content.readline()

                        find_stop_character(content_line, text_content, temp_file)
                        break

                else:
                    temp_file.write(temp_line_first)
                    temp_file.write(content_line)
                    content_line = text_content.readline()

                    find_stop_character(content_line, text_content, temp_file)
                    break

            elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1\n', 'item\n', 'itemi\n', 'item1and2\n', 'items1and2\n'):
                temp_line_first = content_line
                content_line = text_content.readline()

                if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('business\n', 'descriptionofbusiness\n', 'descriptionofthebusiness\n', 'businessoverview\n', '1business\n', '1businessoverview\n', '1descriptionofbusiness\n', '1descriptionofthebusiness\n', '1and2businessandproperties\n', '1and2businessandproperty\n', 'businessandproperties\n', 'businessandproperty\n'):
                    temp_line_second = content_line
                    content_line = text_content.readline()

                    # Skip catalog
                    if content_line.lower().replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').rstrip('\n').replace('i', '').replace('[', '').replace(']', '').replace('page', '').replace(',', '').isdigit():
                        content_line = text_content.readline()

                    elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1a\n', 'item2\n', 'item\n', 'item3\n', 'item1ariskfactors\n', 'item2properties\n', 'item2property\n', 'item2descriptionofproperties\n', 'item2descriptionofproperty\n', 'item3legalproceedings\n'):
                        content_line = text_content.readline()

                    else:
                        temp_file.write(temp_line_first)
                        temp_file.write(temp_line_second)
                        temp_file.write(content_line)
                        content_line = text_content.readline()

                        find_stop_character(content_line, text_content, temp_file)
                        break

                elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('1\n'):
                    temp_line_second = content_line
                    content_line = text_content.readline()

                    if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('business\n', 'descriptionofbusiness\n'):
                        temp_line_third = content_line
                        content_line = text_content.readline()

                        if not content_line.lower().replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').rstrip('\n').replace('i', '').replace('[', '').replace(']', '').replace('page', '').replace(',', '').isdigit():
                            if not content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1a\n', 'item2\n', 'item\n', 'item3\n', 'item1ariskfactors\n', 'item2properties\n', 'item2property\n', 'item2descriptionofproperties\n', 'item2descriptionofproperty\n', 'item3legalproceedings\n'):
                                temp_file.write(temp_line_first)
                                temp_file.write(temp_line_second)
                                temp_file.write(temp_line_third)
                                temp_file.write(content_line)
                                content_line = text_content.readline()

                                find_stop_character(content_line, text_content, temp_file)
                                break

                        else:
                            content_line = text_content.readline()

                else:
                    target = ['business  ', 'descriptionofbusiness  ', 'description of business  ', '1business  ', '1 business  ', '1businessoverview  ', '1 businessoverview  ', '1descriptionofbusiness  ', '1 descriptionofbusiness  ', '1 description of business  ', 'businessandproperties  ', 'business and properties  ', 'businessandproperty  ', 'business and property  ']
                    count = 0;

                    for i in target:
                        if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lstrip().lower().startswith(i):
                            temp_file.write(temp_line_first)
                            temp_file.write(content_line)
                            content_line = text_content.readline()

                            find_stop_character(content_line, text_content, temp_file)
                            break

                        else:
                            count += 1

                            if count == len(target):
                                content_line =text_content.readline()

            # Skip catalog
            elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().startswith('item1business'):
                if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().lstrip('item1business').rstrip('\n').isdigit():
                    content_line = text_content.readline()
                else:
                    temp_file.write(content_line)
                    content_line = text_content.readline()

                    find_stop_character(content_line, text_content, temp_file)
                    break

            else:
                start_target = ['item 1 business  ', 'item1business  ', 'item1 business  ', 'item 1business  ', 'item 1  business  ', 'item1  business  ', 'item  1business  ', 'item 1 description of business  ', 'item1description of business  ', 'item1 description of business  ', 'item 1description of business  ', 'item 1  description of business  ', 'item1  description of business  ', 'item  1description of business  ', 'item1descriptionofbusiness  ', 'items 1 and 2 business and properties  ', 'items 1 & 2 business and properties  ']
                half_end_target = ['  item 1\n', '  item1\n']
                end_target = ['  item 1 business\n', '  item1business\n', '  item1 business\n', '  item 1business\n', '  item 1  business\n', '  item1  business\n', '  item  1business\n', '  item 1 description of business\n', '  item1description of business\n', '  item1 description of business\n', '  item 1description of business\n', '  item 1  description of business\n', '  item1  description of business\n', '  item  1description of business\n', '  item1descriptionofbusiness\n', '  items 1 and 2 business and properties\n', '  items 1 & 2 business and properties\n']
                middle_target = ['  item 1 business  ', '  item1business  ', '  item1 business  ', '  item 1business  ', '  item 1  business  ', '  item1  business  ', '  item  1business  ', '  item 1 description of business  ', '  item1description of business  ', '  item1 description of business  ', '  item 1description of business  ', '  item 1  description of business  ', '  item1  description of business  ', '  item  1description of business  ', '  item1descriptionofbusiness  ', '  items 1 and 2 business and properties  ', '  items 1 & 2 business and properties  ']
                count = 0

                for k in middle_target:
                    start_index = content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().find(k)
                    if start_index != -1:
                        temp_file.write(content_line[start_index:])
                        content_line = text_content.readline()

                        find_stop_character(content_line, text_content, temp_file)
                        stop_signal = True
                        break

                    else:
                        count += 1
                        if count == len(middle_target):
                            count =0

                            for i in start_target:
                                if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lstrip().lower().startswith(i):
                                    temp_file.write(content_line)
                                    content_line = text_content.readline()

                                    find_stop_character(content_line, text_content, temp_file)
                                    stop_signal = True
                                    break

                                else:
                                    count += 1
                                    if count == len(start_target):
                                        count = 0

                                        for h in end_target:
                                            if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().endswith(h):
                                                temp_file.write(content_line[content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().find(h):])
                                                content_line = text_content.readline()

                                                find_stop_character(content_line, text_content, temp_file)
                                                stop_signal = True
                                                break

                                            else:
                                                count += 1
                                                if count == len(end_target):
                                                    count = 0

                                                    for j in half_end_target:
                                                        if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().endswith(j):
                                                            temp_line = content_line[content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().find(j):]
                                                            content_line = text_content.readline()

                                                            if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lstrip().lower().startswith('business  '):
                                                                temp_file.write(temp_line)
                                                                temp_file.write(content_line)
                                                                content_line = text_content.readline()

                                                                find_stop_character(content_line, text_content, temp_file)
                                                                stop_signal = True
                                                                break

                                                            else:
                                                                count += 1
                                                                if count == len(half_end_target):
                                                                    content_line = text_content.readline()
                                                        else:
                                                            count += 1
                                                            if count == len(half_end_target):
                                                                content_line = text_content.readline()

        else:
            content_line = text_content.readline()

        if stop_signal == True:
            break

    temp_file.close()

    # Manual clean
    temp_content = open(os.path.join(extracted_dir, f))
    temp_lines =temp_content.readlines()

    if len(temp_lines) == 5:
        os.remove(os.path.join(extracted_dir, f))
        shutil.copy(os.path.join(original_dir,f), os.path.join(extracted_dir, 'Manual_Clean'))

def find_stop_character(content_line, text_content, temp_file):

    while content_line != '':

        item_check = content_line.lower().find('item')

        stop_signal = False

        if item_check != -1:

            if not content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item1bunresolvedstaffcomments\n', 'item2properties\n', 'item2property\n', 'item2descriptionofproperties\n', 'item2descriptionofproperty\n', 'item3legalproceedings\n', 'partiitem1bunresolvedstaffcomments\n', 'partiitem2property\n', 'partiitem2properties\n'):

                # Skip pagination
                if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').rstrip('\n').isdigit():
                    temp_file.write('\n')
                    content_line = text_content.readline()

                elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('item\n', 'item1b\n', 'item2\n', 'item3\n'):
                    temp_line_first = content_line
                    content_line = text_content.readline()

                    if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('1bunresolvedstaffcomments\n', 'unresolvedstaffcomments\n', '2properties\n', '2property\n', '2descriptionofproperties\n', '2descriptionofproperty\n', 'properties\n', 'property\n', 'descriptionofproperties\n', 'descriptionofproperty\n', 'facilities\n', 'legalproceedings\n', '3legalproceedings\n'):
                        stop_signal = True
                        break

                    elif content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('2\n'):
                        temp_line_second = content_line
                        content_line = text_content.readline()

                        if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower() in ('properties\n', 'property\n', 'descriptionofproperties\n', 'descriptionofproperty\n'):
                            stop_signal = True
                            break

                        else:
                            temp_file.write(temp_line_first)
                            temp_file.write(temp_line_second)
                            temp_file.write(content_line)
                            content_line = text_content.readline()

                    else:
                        target = ['unresolved staff comments  ', 'unresolvedstaffcomments  ', '1b unresolved staff comments  ', '1bunresolved staff comments  ', '1bunresolvedstaffcomments  ', 'properties  ', 'property  ', '2 properties  ', '2properties  ', '2 property  ', '2property  ', '2 description of properties  ', '2description of properties  ', '2descriptionofproperties  ', '2 description of property  ', '2description of property  ', '2descriptionofproperty  ', 'description of properties  ', 'descriptionofproperties  ', 'description of property  ', 'descriptionofproperty  ', '3 legal proceedings  ', '3legal proceedings  ', '3legalproceedings  ', 'legal proceedings  ', 'legalproceedings  ']
                        count = 0

                        for i in target:
                            if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lstrip().lower().startswith(i):
                                stop_signal = True
                                break

                            else:
                                count += 1

                                if count == len(target):
                                    temp_file.write(temp_line_first)
                                    temp_file.write(content_line)
                                    content_line = text_content.readline()

                else:
                    start_target = ['item 1b unresolved staff comments  ', 'item1bunresolved staff comments  ', 'item1b unresolved staff comments  ', 'item 1bunresolved staff comments  ', 'item 1b  unresolved staff comments  ', 'item1b  unresolved staff comments  ', 'item  1bunresolved staff comments  ', 'item 2 properties  ', 'item2properties  ', 'item2 properties  ', 'item 2properties  ', 'item 2  properties  ', 'item2  properties  ', 'item  2properties  ', 'item 2 property  ', 'item2property  ', 'item2 property  ', 'item 2property  ', 'item 2  property  ', 'item2  property  ', 'item  2property  ', 'item 2 description of properties  ', 'item2description of properties  ', 'item2 description of properties  ', 'item 2description of properties  ', 'item 2  description of properties  ', 'item2  description of properties  ', 'item  2description of properties  ', 'item 2 description of property  ', 'item2description of property  ', 'item2 description of property  ', 'item 2description of property  ', 'item 2  description of property  ', 'item2  description of property  ', 'item  2description of property  ', 'item 3 legal proceedings  ', 'item3legal proceedings  ', 'item3 legal proceedings  ', 'item 3legal proceedings  ', 'item 3  legal proceedings  ', 'item3  legal proceedings  ', 'item  3legal proceedings  ']
                    end_target = ['  item 1b unresolved staff comments\n', '  item1bunresolved staff comments\n', '  item1b unresolved staff comments\n', '  item 1bunresolved staff comments\n', '  item 1b  unresolved staff comments\n', '  item1b  unresolved staff comments\n', '  item  1bunresolved staff comments\n', '  item 2 properties\n', '  item2properties\n', '  item2 properties\n', '  item 2properties\n', '  item 2  properties\n', '  item2  properties\n', '  item  2properties\n', '  item 2 property\n', '  item2property', '  item2 property\n', '  item 2property\n', '  item 2  property\n', '  item2  property\n', '  item  2property\n', '  item 2 description of properties\n', '  item2description of properties\n', '  item2 description of properties\n', '  item 2description of properties\n', '  item 2  description of properties\n', '  item2  description of properties\n', '  item  2description of properties\n', '  item 2 description of property\n', '  item2description of property\n', '  item2 description of property\n', '  item 2description of property\n', '  item 2  description of property\n', '  item2  description of property\n', '  item  2description of property\n', '  item 3 legal proceedings\n', '  item3legal proceedings\n', '  item3 legal proceedings\n', '  item 3legal proceedings\n', '  item 3  legal proceedings\n', '  item3  legal proceedings\n', '  item  3legal proceedings\n']
                    middle_target = ['  item 1b unresolved staff comments  ', '  item1bunresolved staff comments  ', '  item1b unresolved staff comments  ', '  item 1bunresolved staff comments  ', '  item 1b  unresolved staff comments  ', '  item1b  unresolved staff comments  ', '  item  1bunresolved staff comments  ', '  item 2 properties  ', '  item2properties  ', '  item2 properties  ', '  item 2properties  ', '  item 2  properties  ', '  item2  properties  ', '  item  2properties  ', '  item 2 property  ', '  item2property  ', '  item2 property  ', '  item 2property  ', '  item 2  property  ', '  item2  property  ', '  item  2property  ', '  item 2 description of properties  ', '  item2description of properties  ', '  item2 description of properties  ', '  item 2description of properties  ', '  item 2  description of properties  ', '  item2  description of properties  ', '  item  2description of properties  ', '  item 2 description of property  ', '  item2description of property  ', '  item2 description of property  ', '  item 2description of property  ', '  item 2  description of property  ', '  item2  description of property  ', '  item  2description of property  ', '  item 3 legal proceedings  ', '  item3legal proceedings  ', '  item3 legal proceedings  ', '  item 3legal proceedings  ', '  item 3  legal proceedings  ', '  item3  legal proceedings  ', '  item  3legal proceedings  ']
                    count = 0

                    for k in middle_target:
                        end_index = content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().find(k)
                        if end_index != -1:
                            temp_file.write(content_line[:end_index])
                            stop_signal = True
                            break

                        else:
                            count += 1
                            if count == len(middle_target):
                                count = 0

                                for i in start_target:
                                    if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lstrip().lower().startswith(i):
                                        stop_signal = True
                                        break

                                    else:
                                        count += 1

                                        if count == len(start_target):
                                            count = 0

                                            for j in end_target:
                                                if content_line.replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').lower().endswith(j):
                                                    temp_file.write(content_line)
                                                    stop_signal = True
                                                    break

                                                else:
                                                    count += 1

                                                    if count == len(end_target):
                                                        temp_file.write(content_line.replace('\xb7', '  ').replace('\x92', '\'').replace('\x93', '').replace('\x8f', '  ').replace('\x95', '  '))
                                                        content_line = text_content.readline()

            else:
                stop_signal = True
                break

        else:
            if content_line.replace(' ', '').replace('.', '').replace('-', '').replace(':', '').replace('\t', '').replace(',', '').rstrip('\n').isdigit():
                temp_file.write('\n')
                content_line = text_content.readline()
            else:
                temp_file.write(content_line.replace('\xb7', '  ').replace('\x92', '\'').replace('\x93', '').replace('\x8f', '  ').replace('\x95', '  '))
                content_line = text_content.readline()

        if stop_signal == True:
            break



if __name__ == '__main__' :
    main()
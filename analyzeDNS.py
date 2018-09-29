#!/usr/bin/python3
import boto3
import datetime
#from subprocess import call
import os

debug_on = True

today = datetime.date.today()

bucket_name = 'halimer-dns-analytics'

log_folder_name = '/var/log/'
tmp_dir = '/tmp/'



prefix =  'd=' + str(today) + '/'

pihole_log_file = 'pihole.log'

clean_log_name = 'clean_dns.log'

#print clean_log_name

def debug(title,item):
    if(debug_on):
        print(title)
        print(item)
    return


def get_private_words():
    with open('donotanalyze.txt') as private_txt:
        private_txt.seek(0)
        private_raw = private_txt.read()
        print(private_raw)
        split_word_list = private_raw.split('\n')
        private_word_list =[]
        for word in split_word_list:
            if word != '':
                private_word_list.append(word)

        return private_word_list


def remove_private_words():
    words_to_scrub = get_private_words()
    current_log_file=pihole_log_file

    number_of_words = len(words_to_scrub)
    debug("Number of Blacklist Words",number_of_words)

    word_counter = 0
    grep_string="egrep -v '"
    for word in words_to_scrub:
        grep_string+=word
        word_counter += 1
        if(word_counter < len(words_to_scrub)):
            grep_string+='|'

    grep_string += "' " + log_folder_name + current_log_file +" > " + tmp_dir + clean_log_name
    print(grep_string)

    os.system(grep_string)

def delete_old_log_files():
    os.system('pihole -f')
    os.system('rm ' + tmp_dir + clean_log_name)



def upload_log_to_s3():
    client = boto3.client('s3')
    s3 = boto3.resource('s3')
    response = s3.meta.client.upload_file(tmp_dir + clean_log_name,bucket_name, prefix + clean_log_name)
    debug("Response is :", response)





words = get_private_words()
debug("Words",words)
number_of_words = len(words)
debug("Number of Blacklist Words",number_of_words)
debug("Prefix is: ", prefix)



remove_private_words()

upload_log_to_s3()

delete_old_log_files()


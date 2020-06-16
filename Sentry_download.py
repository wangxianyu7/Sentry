import json
import wget
import os, shutil
from subprocess import call 


def dowmload():

    # download sentry summary
    sentry_summary = 'sentry_summary.json'
    sentry_summary_url = 'https://ssd-api.jpl.nasa.gov/sentry.api'

    if not os.path.exists(sentry_summary):

        call(['wget', '-q', '-O', sentry_summary, sentry_summary_url ])
        print(sentry_summary, 'Downloaded!')


    # download data of all object
    i = 0
    query_header = 'https://ssd-api.jpl.nasa.gov/sentry.api?des='
    log = open('log.txt', 'w')

    with open(sentry_summary,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
        for line in json_data['data'][0:5]:

            i+= 1
            fullname = line['fullname'].replace('(', '').replace(')', '')
            no_space_fullname = line['fullname'].replace('(', '').replace(')', '').replace(' ', '%20')
            split_fullname = fullname.split()
            year_idx = split_fullname[0]

            if int(year_idx) > 2025:
                url = query_header+str(year_idx)
            else:
                url = query_header+no_space_fullname
            out_filename = fullname+'.json'
            if not os.path.exists(fullname+'.json'):
                try:
                    call(['wget', '-q', '-O', out_filename, url ])
                    print(i, fullname, 'Downloaded!')
                except:
                    # print(url)
                    print(fullname,'Failed!')
                    print('Failed:', fullname,url, file=log)

    log.close()                

def json2excel(json_filename):
    
    order = ['date', 'dist', 'width', 'sigma_imp', 'sigma_lov', 'stretch','ip','energy','ps', 'ts']

    csv_filename = json_filename.split('.')[0]+'.csv'

    csv = open(csv_filename, 'w')
    with open(json_filename,'r', encoding = 'UTF-8') as fr:

        json_data = json.load(fr)
        data_all = json_data['data']
        for i,data in enumerate(data_all):
            keys = data.keys()
            if i == 0:
                for key in order:
                    try:
                        print(key, end=',', file=csv)
                    except:
                        pass

            print(file=csv)

            for key in order:
                try:
                    print(data[key], end=',', file=csv)
                except:
                    pass

    csv.close()


def mv_file():
    dirs = ['json', 'csv']
    for dir_ in dirs:
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        file_list = [x for x in os.listdir(os.getcwd())
                    if dir_ in x and 'summary' not in x]
        for file in file_list:
            shutil.move(file, dir_)


if __name__ == '__main__':

    # dowmload part
    dowmload()

    # json2csv part
    json_list = [x for x in os.listdir(os.getcwd())
                  if '.json' in x and 'summary' not in x  ]
    for json_filename in json_list:
        print(json_filename, 'Json2csv Done!')
        json2excel(json_filename)

    mv_file()
import requests
import json
import csv
import sys
import os

initial_date = '2018-01-01'
final_date = '2018-10-01'
quote_page = 'https://npm-stat.com/api/download-counts?package=%s&from=%s&until=%s'


def get_downloads_from_package(package):
    package_response = requests.get(quote_page%(package, initial_date, final_date), verify=False)
    try:
        if (package_response.ok):
            jData = json.loads(package_response.content)
            num_downloads = 0 
            for each_date in jData[package]:
                num_downloads_date = jData[package][each_date]
                num_downloads = num_downloads + num_downloads_date
        return num_downloads
    except:
        e = sys.exc_info()[0]
        print(e)
        return None


def append_line_output_file(package, num_downloads):
    directory = sys.argv[1].split('/')[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open('%s_download_count.csv'%(sys.argv[1].split('.')[0]), 'a') as csv_file:
        csv_file.write("%s,%s\n"%(package, num_downloads))
    return


def main():
    append_line_output_file('package', 'num_downloads')
    with open(sys.argv[1], 'r') as csv_file:
        reader = csv.reader(csv_file)
        title_line = next(reader)
        for row in reader:
            if row[6] != 'T':
                break
            package = row[0]
            append_line_output_file(package, get_downloads_from_package(package))
    return 0


if __name__ == "__main__":
        sys.exit(main())
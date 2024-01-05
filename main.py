from reformatter import reformat as re
from reformatter import functions as fn
from reformatter import config
from google.cloud import storage
import os
import requests
import json
import datetime
import functions_framework

@functions_framework.http
def link_checker(request):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(CURRENT_DIR, 'app_key.json')
    # create a file in GCP bucket to use for logging
    #client = storage.Client()
    #bucket = client.get_bucket('sites.ramseysystems.co.uk')
    
    # get endpoints excel from GCP
    endpoints_wb = fn.get_excel_from_gcloud('link_checker', 'EndpointsForLinkChecking.xlsx')
    endpoints = fn.get_endpoints_from_excel(endpoints_wb)
    
    # get blob for logging
    #blob = bucket.blob('link_checker.log')
    #blob.upload_from_string('')
    
    standards = {}
    invalid_link_count = 0
    valid_link_count = 0
    total_link_count = 0
    
    #blob.upload_from_string('Starting link checker')
    
    for url in endpoints:
        
    #    blob.upload_from_string(f'Checking {url}')
        
        response = requests.get(url)
        if response.status_code != 200:
    #        blob.upload_from_string(f'Error: {response.status_code}')
            print(f'Error: {response.status_code}')
            continue
        
        data = response.json()
    #    blob.upload_from_string(f'JSON loaded')
        
        if type(data['dataset'][0]['name']) == str:
            standard_name = data['dataset'][0]['name']
        elif type(data['dataset'][0]['shortName']) == str:
            standard_name = data['dataset'][0]['shortName']
        elif type(data['dataset'][0]['name'][0]['#text']) == str:
            standard_name = data['dataset'][0]['name'][0]['#text']
        
        try:
            standards[standard_name] = {}
        except TypeError:
    #        blob.upload_from_string(f'Error: {standard_name}')
            print(f'Error: {standard_name}')
            continue
        
        clean_json = re.filter(data, True)
    #    blob.upload_from_string(f'JSON filtered')
        links, errors = re.extract_links(clean_json, config.expressions)
    #    if errors:
    #        [blob.upload_from_string(f'Error: {error}') for error in errors]
        invalid_links, errors = re.check_links(links)
    #    if errors:
    #        [blob.upload_from_string(f'Error: {error}') for error in errors]
        standards[standard_name] = invalid_links
            
        total_link_count += len(links)
        invalid_link_count += len(invalid_links)
        valid_link_count += len(links) - len(invalid_links)
        
            
    email = fn.render_email(f'{CURRENT_DIR}/reformatter/templates',
                            'email.jinja', 
                            standards,
                            total_link_count,
                            invalid_link_count,
                            valid_link_count)
    
    fn.send_email('URL Report',
                  email,
                  'frankiepaulhadwick@gmail.com',
                  'frankie@ramseysystems.co.uk',
                  os.environ.get('EMAIL_PASSWORD'))
    
    return email
            
            
        
        
        
        


if __name__ == '__main__':
    link_checker()
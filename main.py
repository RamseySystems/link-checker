from reformatter import reformat as re
from reformatter import functions as fn
from reformatter import config
import os
import requests
import json


def main():
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    #OUTPUT_DIR = f'{CURRENT_DIR}/output'
    
    standards = {}
    invalid_link_count = 0
    valid_link_count = 0
    total_link_count = 0
    
    
    for url in config.endpoints:
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            continue
        
        data = response.json()
        
        if type(data['dataset'][0]['name']) == str:
            standard_name = data['dataset'][0]['name']
        elif type(data['dataset'][0]['shortName']) == str:
            standard_name = data['dataset'][0]['shortName']
        elif type(data['dataset'][0]['name'][0]['#text']) == str:
            standard_name = data['dataset'][0]['name'][0]['#text']
        
        try:
            standards[standard_name] = {}
        except TypeError:
            print(f'Error: {standard_name}')
            continue
        
        clean_json = re.filter(data, True)
        links = re.extract_links(clean_json, config.expressions)
        invalid_links = re.check_links(links)
        standards[standard_name] = invalid_links
        
        '''
        save_path = f'{OUTPUT_DIR}/{standard_name}.clean.json'
        with open(save_path, 'w') as f:
            json.dump(clean_json, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{standard_name}.links.json'
        with open(save_path, 'w') as f:
            json.dump(links, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{standard_name}.invalid.links.json'
        with open(save_path, 'w') as f:
            json.dump(invalid_links, f, indent=4)
        '''
            
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
            
            
        
        
        
        


if __name__ == '__main__':
    main()
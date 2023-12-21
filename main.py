from reformatter import reformat as re
from reformatter import functions as fn
from reformatter import config
from password import password
import os
import json



def main():
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    INPUT_DIR = f'{CURRENT_DIR}/raw_art_decor'
    OUTPUT_DIR = f'{CURRENT_DIR}/output'
    
    standards = {}
    
    for file in os.listdir(INPUT_DIR):
        path_to_file = f'{INPUT_DIR}/{file}'
        file_name = file.split('.')[0]
        standards[file_name] = {}
        
        with open(path_to_file) as f:
            data = json.load(f)
            
        clean_json = re.filter(data, True)
        links = re.extract_links(clean_json, config.expressions)
        invalid_links = re.check_links(links)
        standards[file_name] = invalid_links
        
        save_path = f'{OUTPUT_DIR}/{file_name}.clean.json'
        with open(save_path, 'w') as f:
            json.dump(clean_json, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{file_name}.links.json'
        with open(save_path, 'w') as f:
            json.dump(links, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{file_name}.invalid.links.json'
        with open(save_path, 'w') as f:
            json.dump(invalid_links, f, indent=4)
            
    email = fn.render_email(f'{CURRENT_DIR}/reformatter/templates',
                            'email.jinja', 
                            standards,
                            'Failed URL\'s')
    
    fn.send_email('URL Report',
                  email,
                  'frankiepaulhadwick@gmail.com',
                  'frankie@ramseysystems.co.uk',
                  password)
            
            
        
        
        
        


if __name__ == '__main__':
    main()
from reformatter import reformat as fn
from reformatter import config
import os
import json



def main():
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    INPUT_DIR = f'{CURRENT_DIR}/raw_art_decor'
    OUTPUT_DIR = f'{CURRENT_DIR}/output'
    
    for file in os.listdir(INPUT_DIR):
        path_to_file = f'{INPUT_DIR}/{file}'
        file_name = file.split('.')[0]
        
        with open(path_to_file) as f:
            data = json.load(f)
            
        clean_json = fn.filter(data, True)
        links = fn.extract_links(clean_json, config.expressions)
        invalid_links = fn.check_links(links)
        
        save_path = f'{OUTPUT_DIR}/{file_name}.clean.json'
        with open(save_path, 'w') as f:
            json.dump(clean_json, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{file_name}.links.json'
        with open(save_path, 'w') as f:
            json.dump(links, f, indent=4)
            
        save_path = f'{OUTPUT_DIR}/{file_name}.invalid.links.json'
        with open(save_path, 'w') as f:
            json.dump(invalid_links, f, indent=4)
            
            
        
        
        
        


if __name__ == '__main__':
    main()
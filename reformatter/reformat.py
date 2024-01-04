import json
import os
from reformatter import functions as fn
import copy
import html
import re
from copy import copy
from jsonschema import validate
from jsonschema import Draft202012Validator
import requests
import sys

def save_obj_to_file(obj, save_path):
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)

def filter(node, implamentationGuidance: bool):
    if isinstance(node, dict):
        retVal = {}
        for key in node:
            if key == 'desc':
                if '#text' in node[key][0]:
                    retVal['description'] = html.unescape(node[key][0]['#text'])
            elif key == 'conformance':
                retVal['mro'] = node[key]
            elif key == 'shortName':
                retVal['name'] = node[key]
            elif key == 'operationalization':
                retVal['valueSets'] = re.sub(r'(?<=release=)[a-z][0-9]*', '', html.unescape(node[key][0]['#text'])).replace('&amp;','&')
            elif key == 'minimumMultiplicity':
                retVal[key] = node[key]
            elif key == 'maximumMultiplicity':
                retVal[key] = node[key]
            elif key == 'type': 
                retVal['type'] = node[key]
            elif key == 'valueDomain':
                if node[key][0]['type'] != 'code':
                    if node[key][0]['type'] != 'ordinal':
                        retVal[key] = copy(node[key])
            elif key == 'context':
                if implamentationGuidance:
                    retVal['implamentationGuidance'] = re.sub(r'(?<=release=)[a-z][0-9]*', '', html.unescape(node[key][0]['#text'])).replace('&amp;','&')
            elif isinstance(node[key], dict) or isinstance(node[key], list):
                if key not in ['relationship', 'implementation']:
                    child = filter(node[key], implamentationGuidance)
                    if child:
                        retVal[key] = child
            
        if retVal:
            return retVal
        else:
            return None


    elif isinstance(node, list):
        retVal = []
        for entry in node:
            if isinstance(entry, str):
                retVal.append(entry)
            elif isinstance(entry, dict) or isinstance(entry, list):
                child = filter(entry, implamentationGuidance)
                if child:
                    retVal.append(child)
        if retVal:
            return retVal
        else:
            return None


def validate(schema: dict, instance: dict):
    '''
    A function to validate the instance against a schema

    :param schema: the schema to validate against
    :param instance: the instance to validate
    '''
    validator = Draft202012Validator(schema)
    error_list = list(validator.iter_errors(instance))
    if error_list:
        return error_list
    else:
        return 'The instance is valid'



def extract_links(data, patterns, path=''):
    errors = []
    links = {}

    def get_readable_name(d):
        # Returns the 'name' from a dictionary, if available
        return d.get('name') if isinstance(d, dict) and 'name' in d else None

    def should_skip_key(key):
        # Skip 'dataset' and 'concept' keys in the path
        return key in ['dataset', 'concept']

    if not isinstance(data, (dict, list)):
        errors.append(f"Invalid data type: {type(data)}")
        return links, errors

    if not patterns:
        errors.append("No patterns provided for matching")
        return links, errors

    try:
        if isinstance(data, dict):
            for key, value in data.items():
                if should_skip_key(key):
                    new_path = path
                else:
                    readable_name = get_readable_name(value)
                    new_path = f"{path} > {readable_name}" if path and readable_name else f"{path} > {key}" if path else readable_name if readable_name else key

                if isinstance(value, str):
                    for pattern in patterns:
                        try:
                            match = re.search(pattern, value)
                            if match:
                                links[new_path] = match.group(0)  # Group 0 is the entire match
                        except re.error as regex_error:
                            errors.append(f"Regex error: {regex_error} for pattern {pattern}")
                else:
                    sub_links, sub_errors = extract_links(value, patterns, new_path)
                    links.update(sub_links)
                    errors.extend(sub_errors)

        elif isinstance(data, list):
            for index, item in enumerate(data):
                readable_name = get_readable_name(item)
                item_path = readable_name if readable_name else f"[{index}]"
                new_path = f"{path} > {item_path}" if path else item_path
                sub_links, sub_errors = extract_links(item, patterns, new_path)
                links.update(sub_links)
                errors.extend(sub_errors)
    except Exception as e:
        errors.append(f"Unexpected error: {e}")

    # Remove leading and trailing '>'
    cleaned_links = {k.strip(' >'): v for k, v in links.items()}
    return cleaned_links, errors

def check_links(links):
    """
    Checks if the links are valid (not resulting in a 404 error).

    Parameters:
    links (dict): A dictionary with paths as keys and links as values.

    Returns:
    Tuple[dict, list]: A tuple containing a dictionary of invalid links with their corresponding paths,
                        and a list of errors encountered.
    """
    invalid_links = {}
    errors = []
    for path, link in links.items():
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            if response.status_code != 200:
                invalid_links[path] = link
        except requests.RequestException as e:
            # If there's any request-related error, consider the link as invalid and log the error
            invalid_links[path] = link
            errors.append(f"Error with link {link}: {str(e)}")

    return invalid_links, errors
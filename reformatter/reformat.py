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



def extract_links(data, path=''):
    """
    Recursively extracts links from a nested JSON structure.

    Parameters:
    data (dict/list): The JSON data.
    path (str): The current path in the JSON structure.

    Returns:
    dict: A dictionary where the keys are paths to the links, and the values are the links themselves.
    """
    links = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, str) and 'href="' in value:
                # Extracting link using regular expression
                match = re.search(r'href="([^"]*)"', value)
                if match and ("snomed" in match.group(1) or "datadictionary.nhs.uk" in match.group(1)):
                    links[new_path] = match.group(1)
            else:
                links.update(extract_links(value, new_path))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            links.update(extract_links(item, new_path))

    return links

def check_links(links):
    """
    Checks if the links are valid (not resulting in a 404 error).

    Parameters:
    links (dict): A dictionary with paths as keys and links as values.

    Returns:
    dict: A dictionary of invalid links with their corresponding paths.
    """
    invalid_links = {}
    for path, link in links.items():
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            if response.status_code == 404:
                invalid_links[path] = link
        except requests.RequestException:
            # If there's any request-related error, consider the link as invalid
            invalid_links[path] = link

    return invalid_links
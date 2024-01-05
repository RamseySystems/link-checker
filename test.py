import json
from reformatter import functions as fn
import os

bucket = 'sites.ramseysystems.co.uk'
excel_name = 'EndpointsForLinkChecking.xlsx'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(CURRENT_DIR, 'app_key.json')

workbook = fn.get_excel_from_gcloud(bucket, excel_name)
endpoints = fn.get_endpoints_from_excel(workbook)

[print(url) for url in endpoints]
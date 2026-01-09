# Alation data dictionary
Api client and dictionary manager for storing, updating, and quickly accessing column-level records from Alation based on data governance approval criteria.

## Recommended usage
main.py provides a simple workflow which can be added to, adapted, or integrated into an existing workflow:
- initialize the dictionary
- initalize the Api client
- feed records from the Api response to the dictionary
- save the dictionary (write to dictionary file only if new records were added or existing records were updated)
- once the dictionary has been refreshed with the Api data, lookup columns to get info

## Api client
The Api client provided is for the integration/v2/column/ endpoint. Authentication is required via Alation Api token: https://developer.alation.com/dev/docs/authentication-into-alation-apis.

## Dictionary manager
The dictionary manager is responsible for handling file operations on the dictionary file, adding new records, updating existing records, and providing both direct and fuzzy lookup based on column name.

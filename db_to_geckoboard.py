#-------------------------------------------------------------------------------
# Name:        db_to_geckoboard
# Purpose:
#
# Author:      Kat Winter
#
# Created:     11/11/2016
#-------------------------------------------------------------------------------
import requests
import pymongo

# Query a MongoDB database collection for ZenDesk ticket information, and then
# insert that information into a Geckoboard dataset using the Geckoboard API.
def main():
    # Connect to database
    client = pymongo.MongoClient('mongodb://admin:XXXXX@ds055626.mlab.com:55626/zendesk')
    db = client.get_default_database()

    # Get tickets collection
    ticketsCollection = db["tickets"]

    # Create the dataset in case it doesn't exist.
    response = requests.put("https://api.geckoboard.com/datasets/tickets", json= {
        "fields": {
            "ticket_id": {
                "type": "string",
                "name": "Ticket ID"
            },
            "created": {
                "type": "datetime",
                "name": "Created"
            },
            "solved": {
                "type": "datetime",
                "name": "Solved"
            },
            "time": {
                "type": "number",
                "name": "Time"
            }
        },
        "unique_by": ["ticket_id"]
    }, auth=("XXXXX",""))

    # Insert each ticket from the database collection into the Geckoboard dataset
    # using the Geckoboard API.
    # Posting instead of Putting, because per the API, Post will update the dataset based on
    # the unique field (ticket_id in this case), whereas Put will overwrite the dataset.
    for ticket in ticketsCollection.find():
        id = ticket["ticket_id"]
        created = ticket["created"]
        solved = ticket["solved"]
        time = float(ticket["time"])

        response = requests.post("https://api.geckoboard.com/datasets/tickets/data", json= {
            "data" : [{
                "ticket_id": id,
                "created": created,
                "solved": solved,
                "time": time
            }]
        }, auth=("XXXXX",""))

    client.close()

main()

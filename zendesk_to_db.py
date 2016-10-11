#-------------------------------------------------------------------------------
# Name:        zendesk_to_db
# Purpose:
#
# Author:      Kat Winter
#
# Created:     10/11/2016
#-------------------------------------------------------------------------------
import requests
import urllib
import pymongo
from datetime import datetime
from datetime import timedelta

# Query the ZenDesk API for tickets I've solved between 9am yesterday
# and 9am today.
# Insert the results into a MongoDB database hosted on mlab.

# NOTE: There is no exception handling in this program, which horrifies me,
# especially around the database connection and inserts, but MongoDB is strangely
# obtuse (at least to me) when it comes to trying to find a list of possible
# exceptions that each function may throw.
def main():
    # API URL for search (takes additional parameters created below)
    urlBase = "https://ninite.zendesk.com/api/v2/search.json?"
    # Login info for Zendesk API
    user = "kat@ninite.com" + "/token"
    pwd = "sSq9JaQ4FJEwv4gPzqAEUFxYCknT04MnA8hkq8Sd"

    # I'll be using these more than once, so I'm saving them as variables
    # to avoid the traagedy of a typo later on.
    date_format = "%Y-%m-%d"
    time_string = "T09:00:00-05:00"

    # I want to search for tickets created between 9am yesterday and 9am today.
    # So first I'll grab today's date and append 9am (Eastern),
    # and then calculate yesterday's date from today's.
    today = datetime.today().date()
    str_today = today.strftime(date_format)
    solvedEnd = str_today + time_string

    yesterday = today - timedelta(days=1)
    str_yesterday = yesterday.strftime(date_format)
    solvedStart = str_yesterday + time_string

    # The query I want to use is to find tickets assigned to me that I have
    # solved between 9am yesterday to 9am today.
    queryParams = {"query" : "assignee:me status:solved type:ticket solved>" + solvedStart + " solved<" + solvedEnd }

    # HTTP encode the query string.
    encodedParams = urllib.urlencode(queryParams)

    # Send the request.
    response = requests.get(urlBase+encodedParams, auth=(user,pwd))

    # Got a response
    data = response.json()

    # Connect to database
    client = pymongo.MongoClient('mongodb://admin:z3nd3sK@ds055626.mlab.com:55626/zendesk')
    db = client.get_default_database()

    # Get tickets collection
    ticketsCollection = db["tickets"]
    # Clear out tickets collection because I only want the single day's data.
    # In the future, I might want to store all ticket data, which would allow me more flexibility
    # in terms of using that data from the database, but right now I just want to store a single
    # day's data, and then another app will consume that data and push to Geckoboard.
    ticketsCollection.delete_many({})

    # Again, want to avoid typos
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    # Loop through results and insert into database.
    # Specifically, create datetime objects for created_at and updated_at so that
    # the time spent on each can be calculated.
    # Then format that time spent so it only goes to one decimal place.
    # Finally, insert to the ticketsCollection collection in the database.
    for result in data["results"]:

        created_at = result["created_at"]
        dt_created_at = datetime.strptime(created_at, datetime_format)

        updated_at = result["updated_at"]
        dt_updated_at = datetime.strptime(updated_at, datetime_format)

        td_time_open = dt_updated_at-dt_created_at
        hours = td_time_open.total_seconds() / 3600
        str_hours = "%.1f" % hours

        ticketsCollection.insert({
            "ticket_id" : str(result["id"]),
            "created" : created_at,
            "solved" : updated_at,
            "time" : str_hours
        })

    client.close()

main()

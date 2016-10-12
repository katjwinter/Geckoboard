# Geckoboard
Moves data from zendesk to mlab and from mlab to Geckoboard.

This is a set of Python apps which as a whole are designed to take my ZenDesk data and move it to an mlab database collection,
from where it will then be moved to a Geckoboard dataset.

I chose to write it in Python because it's a language that I'm comfortable writing quickly in, so if I want to dash something out
as quickly as possible, it's usually my goto. I considered Node.js, because I'm also pretty comfortable in Node (and Javascript in general),
but because I didn't need any of the web stack aspect of it, I felt like Python made more sense.

I used MongoDB and mlab because although I'm very comfortable in MySQL, MongoDB is quick and easy for this kind of proof of concept app.
I'm probably equally fluent in MySQL and MongoDB, but I tend toward MySQL for apps where I'm really planning out a schema ahead of time,
and I tend toward MongoDB when I'm just playing around or throwing together an app as quickly as I can. 

There are actually two apps, one which is the producer that queries the ZenDesk API for the ticket data that I want and writes it to the
database, and the other which is a consumer that queries the database and then pushes the data up to a Geckoboard dataset using
the Geckoboard API.

One interesting aspect of using Python (over something like Node for example) is that there isn't an existing Geckoboard library to
support the API. This wasn't a problem for me, because it just meant looking at the curl references to get the necessary endpoint
information like PUT vs POST for overwriting vs updating, but it did require more time studying the API than would have been necessary
if I'd been able to use an existing library.

I'll be hosting the app(s) on Heroku so that I can use the scheduler add on to run each of them daily.

There is a lot of room for improvement, including but surely not limited to:

Privacy/Security: This is just GitHub specific and not relevant to code itself, but I'll need to blank out my ZenDesk token so that 
no one can use it to create tickets in my name or anything. I'll also want to do the same with my database credentials.
*I realize that changing this on github doesn't hide anything, but I mean for the purposes for code distribution. The zendesk token I originally posted has been changed on the zendesk side, and the admin credentials changed on the mongo database. Realized I should clarify that, considering we're talking about privacy and security!

Rigidity: I'm currently just grabbing a very select bit of ticket information to store in the database, but it would be more useful to
gather a lot more information, or to not recreate the database every day (currently I want the app to run once a day, so it just
recreates the collection every day so that there's only every 24 hours of data available in the collection).

Error Handling: I need to look deeper into Python exception handling. I'm used to C# and Microsoft, where you can look up the official
description of a library function, and it will tell you what exceptions can be thrown and under what circumstances. I have not found
the same with Python, so I'm not sure what exceptions I need to catch, but I also don't want to just catch general exceptions.

Streamlining for Geckoboard: The data I'm pushing to the Geckoboard dataset isn't really the most useful in terms of creating Geckoboard
widgets out of it. I would love to spend more time playing around to see what data I want to see, how I want it graphed out in a
Geckoboard widget, etc. I'll then probably modify what data I'm pulling from ZenDesk, or at least what data I'm pushing out to
Geckoboard.

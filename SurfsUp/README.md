# sqlalchemy-challenge

In order to complete this assignment I relied on the content covered in class, a tutoring session with Kourt Bailey, and some code that I found online via github. For the most part I was able to find the information that I needed in looking back over the different class activities we did. However, I had trouble with the last part of the flask portion of the assignment. I was hoping to cover this in my tutoring session, but we did not get through it fully. I couldn't figure out how to do the start and end date functions as a dictionary the way I wanted to. I found a snippet of code from this location: https://github.com/MThorpester/sqlalchemy-challenge/blob/main/app.py.

Specifically, the portion of the code that follows:

    trip_stats = []
    for min, avg, max in query_result:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Average"] = avg
        trip_dict["Max"] = max
        trip_stats.append(trip_dict)
        
I used that framework to come up with the last part of my flask code for this assignment. For the other routes I used the dict() function in Python to transform my query results into a dictionary, and then I used jsonify to get the output I was looking for. 
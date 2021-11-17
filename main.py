import server
import utils

'''
        MY COMMENTS:
        
            * NOTE: This is my first time implementing a server and doing web related coding. I am familiar with all the
                concepts, but I am also aware that there are probably some better, more efficient and novel ways and 
                practices for this type of coding. I did my best.
                
                
                                                    FLOW
            Daily Update:
             - I use the 'before_request_callback' function to check the validity of the database.
             - Based on the 'latest_update.txt' file that starts as an empty file and holds only the date of the latest
                update.
            - I thought about a different method - scheduling a daily check for update. Since it looked more complicated
                and involved libraries I don't know too well I decided to go with the simpler solution.
             
            GET:
             - check the txt file of latest update - if needed update the db (the txt file begins empty which invokes 
                the first data update.
            - ID requests: the format is given by: http://127.0.0.1:5000/drink?id=2055838. 
                Meaning the id is passed as a parameter and not by URL. My assumption.
            - Generate a pandas dataframe of the relevant needed fiels for each dish, and for the needed dishtypes.
            - Each get request simply utilizes the pandas framework for the relevant lookups.

            POST:
            - Since I didn't have the experience I decided to go with the post json format, implement by the function 
                and assuming the order is given in a json format with a dictionary formatter like BODY,
                given in the instructions.
            - I attached a sample json file to demonstrate the expected behaviour.
            - to test the post run in terminal :
                curl -H "Content-Type: application/json" --data @order_sample.json http://127.0.0.1:5000/order
            - I did not have time to handle the POST errors such as unknowd ID's or badly formatted data.
                So my assumption is that an empty order or non-existent Id's or strings will just be ignored and 
                not notification will be given.

        * My error handling is not working as I'd like it to work. I'm not sure how represent the error page with a
            costum message so I left strings in the functions.

        * I don't really have the knowledge to 'Suggest a simple way to demonstrate the service functionality'.
            So I'm leaving this one blank. Most of my experience is working locally on machines with 
            machine learning algorithms.

'''

if __name__ == '__main__':

    # Create the update log file
    utils.start_log('latest_update.txt')

    database = utils.get_db()
    server.run_server(database)
    ''' daily update - save the first update date as global, then everytime some function runs check the date for update'''

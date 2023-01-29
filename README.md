# mp-stats-parser
A demonstration of how you can use Python to get lots of useful data from API. This script overcomes the limitations 
of default server settings, and is flexible enough to choose what category you want to download, 
as well as the date range that you are interested in.

The logic and the process of the project is as follows:

1. Get the cURL from the web page of interest;
2. Use Insomnia app to generate client code, which wll be used in Python
3. Construct a function that is able to:
- update the `querystring` parameter, which is responsible for choosing the category of interest and defining a date range
- use a `for loop` that overcomes the server limitations in terms of max number of rows fetched in one call to API
- on each iteration `for loop` adds a product info to a list
- at the end, the function returns a dataframe

As of now, the script lacks the `async` functionality, which would reduce the script running time, and increase the amount of API calls.

Note: the script only runs when the subscription is active, otherwise, it throws a `500` error

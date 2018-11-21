Calendar Sync
=

Sync your personal and work Gmail calendars using IFTTT and Amazon Lambda.


Setup python environment
-
Run the following commands to set up your environment:

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


Auth Google Calendar
-
First, we will set up a new Google API project, authorize your work account, and get an OAuth token using a poor man's OAuth.

1. Create a new Google API project on your work Google apps account in the [Google API Console](https://console.developers.google.com/apis/dashboard)
2. In your Google API project, set the Authorized Redirect URL to a domain you own or control
3. Run `CLIENT_ID=<client-id> CLIENT_SECRET=<client-secret> REDIRECT_URI=<redirect-uri> python auth.py`
4. The script will output a Google apps authentication URL then wait for further input, copy the URL and paste it into your browser.
5. After accepting the OAuth permissions on Google, you should be redirected to your domain.
6. Copy the `code` parameter in the URL (the value after the `=` sign), and enter it as the input for the `python auth.py` script
7. If successful, the `auth.py` script should output the JSON credentials which we will use in the next step.


Test Event Creation
-

Run the following command:

```
CLIENT_ID=<client-id> CLIENT_SECRET=<client-secret> REDIRECT_URI=<redirect-uri> CREDENTIALS=<json-credentials> python index.py
```

If successful, you should see the event created in JSON, and you should have an event that says "Busy" on your calendar (NOTE: It will be created in New York timezone, important for the IFTTT integration).


Upload to Amazon Lambda
-

Package a zip file with all of the python dependencies by running:
```
./package.sh
```

You can upload the resulting `./src.zip` file directly to Amazon Lambda.

Your runtime will be Python 2.7, the Handler should be `index.lambda_handler`, and include the environment variables for your `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI`, and `CREDENTIALS`.



Create API Gateway for Lambda Function
-

I won't go into too much detail here, but you should be able to create a new API, add a resource (e.g. /create), create a GET method, and link your Lambda function on the GET request. I originally tried this with a POST request, which I think would have been more appropriate, but had some trouble when integrating with IFTTT and it was difficult to debug.


IFTTT Applet
-

Go to [create a new applet](https://ifttt.com/create)
For the "this", choose Google Calendar "New event added" trigger. (NOTE: You want to authorize IFTTT to use your personal calendar)
For the "that", choose Webhook.
For the URL, you'll want to use the following format:

`https://<api-gateway-domain>/<api-gateway-resource>?starts={{Starts}}&ends={{Ends}}`

You can find the `api-gateway-domain` under the "Dashboard" tab of your API in AWS API Gateway. The resource is the endpoint created by you (e.g. `/create` in the example above). The `starts` and `ends` parameter values are coming from the IFTTT trigger, and will be used as input to create the calendar event.


Test!
-

After your IFTTT applet is setup, create an event on your personal calendar, and you should have a corresponding "Busy" event on your work calendar.

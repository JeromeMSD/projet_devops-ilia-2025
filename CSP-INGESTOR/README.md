
## More info from the teacher
The docker isn't supposed to stop EVER.
So no optimisation
When the application is launched by the user, our machine will run non-stop,
So we must run it every so ofter, left to decide what, when and with what frequency

Also, we have to make our own Reddis, so that means keeping an eye on our own databases and everything with communication in between

## Launching the docker 
cd CSP-INGESTOR
docker build -t csp-ingestor:latest .
docker run --rm csp-ingestor:latest

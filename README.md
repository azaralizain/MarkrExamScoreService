# MarkrExamScoreService

- Project design created in LucidCharts, uploaded in git under Design folder
- The webserver code is written in python, and the DB is a MySQL db as a docker container
- Docker compose file works fine. It fires up the db and have marked it as a dependency in the webserver container
- Data ingestion is done in a very basic way, but the app was able to fire up the webserver and listen to POST request with XML data


- App is unfinished:
-- Error handling isn't done per se
-- Test cases not written
-- Code commenting is not done

Assumptions:
- Path handling (either by pureposixURL handler or otherwise) is not implemented, so the application might behave abnormally if URLs are not worked nicely
- MySQL DB's cleanup after the container is killed (even if gently) might not work, and the port might stay hooled - so kill the listener if needed to re-fire the containers
- Not saving any irrelevant info (names etc) as there seem to be no use

This is a work in progress project mapping all the player histories in Dota 2 liquipedia, as well as recreating the database in mongodb, as it appears there is not one.

Thoughts on what needs to be done
 - Improve data quality/robustness of parsing logic
 	- Currently 270 player history entries appear as None due to non standard data representaitons
 - May establish black list for personality pages, as they have no player history, may create new db for them
 - Unparseable data may have to be hand corrected
 - Need to establish convention for dates with ??, as there are a large number of them 
 - Need to set refresh convention, check update times on webpages
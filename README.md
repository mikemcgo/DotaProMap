This is a work in progress project mapping all the player histories in Dota 2 liquipedia, as well as recreating the database in mongodb, as it appears there is not one.

Thoughts on what needs to be done

 # General Notes on project
 - Creating a local instance of mongodb from https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
 - Code only runs on full version of ubuntu 16.04 in virtualbox for some reason
 - Pimpmuckl's askfm link is formatted as ask.fm, which cannot be inserted into mongo as a field name, so it has been edited manually
 - On machine restart, be sure to restart mongod service

 LOOK AT THE FUCKING paS file becuase fuck that guy. fucking ?? going into the db becuase fuck me

 # Immediate Concerns 
 - Establish convention for ?? in data before database entry (this is some bad stuff)
 - Improve data quality/robustness of parsing logic
  - Currently 122 player history entries appear as None due to non standard data representaitons, after accounting for hyphen and dash
  - Take notes of data changes
 - Convert the unchanged dates to ints

 # Good Things To Do
 - May establish black list for personality pages, as they have no player history, may create new db for them
 - Establish refresh convention, check update time on webapges, have cached data to fix data quality errors
 - Not accounting for Dota1/Starcraft histories
 - 22 entires have ???? for years, needs to be accounted for

 # Things that will probably never get done
 - Fix Birthdays (last priority honestly)

# Obsidian LiveSync

## Resources

* https://github.com/vrtmrz/obsidian-livesync/tree/main
* https://syslog.space/obsidian-notes/

## Setup

### Dev

1. `docker-compose -f docker-compose.couch-db.yaml up` to start the container
2. Export your `COUCHDB_USER` and `COUCHDB_PASSWORD` to your local shell and execute the `setup_couchdb.sh` setup script (this inits CouchDB)
3. Setup LiveSync plugin in Obsidian and use following settings:
   * URI: `localhost:5984`
   * Username: Get from docker-compose file
   * Password: Get from docker-compose file


### Setup `Self-hosted LiveSync` Plugin in Obsidian

1. Install and enable plugin
2. Open options
3. Under `Setup Wizard`:
   1. Choose `Minimal Setup`
   2. URI: Chosen domain
   3. Username: Same as set in docker-compose file
   4. Password: Same as set in docker-compose file
   5. Database name: Choose an arbitrary name
   6. Enable encryption and choose an encryption password
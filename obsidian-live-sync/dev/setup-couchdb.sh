#!/bin/bash
if [[ -z "$COUCHDB_USER" ]]; then
    echo "ERROR: Username missing"
    exit 1
fi

if [[ -z "$COUCHDB_PASSWORD" ]]; then
    echo "ERROR: Password missing"
    exit 1
fi

echo "-- Configuring CouchDB through REST API -->"

until (curl -X POST "localhost:5984/_cluster_setup" -H "Content-Type: application/json" -d "{\"action\":\"enable_single_node\",\"username\":\"${COUCHDB_USER}\",\"password\":\"${COUCHDB_PASSWORD}\",\"bind_address\":\"0.0.0.0\",\"port\":5984,\"singlenode\":true}" --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/chttpd/require_valid_user" -H "Content-Type: application/json" -d '"true"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/chttpd_auth/require_valid_user" -H "Content-Type: application/json" -d '"true"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/httpd/WWW-Authenticate" -H "Content-Type: application/json" -d '"Basic realm=\"couchdb\""' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/httpd/enable_cors" -H "Content-Type: application/json" -d '"true"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/chttpd/enable_cors" -H "Content-Type: application/json" -d '"true"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/chttpd/max_http_request_size" -H "Content-Type: application/json" -d '"4294967296"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/couchdb/max_document_size" -H "Content-Type: application/json" -d '"50000000"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/cors/credentials" -H "Content-Type: application/json" -d '"true"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done
until (curl -X PUT "localhost:5984/_node/nonode@nohost/_config/cors/origins" -H "Content-Type: application/json" -d '"app://obsidian.md,capacitor://localhost,http://localhost"' --user "${COUCHDB_USER}:${COUCHDB_PASSWORD}"); do sleep 5; done

echo "<-- Configuring done!"
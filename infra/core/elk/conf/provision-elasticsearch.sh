#!/bin/bash

echo "Update kibana_system's password"
curl --fail -POST ${ELASTIC_HOST}/_security/user/kibana_system/_password \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"password\": \"${KIBANA_SYSTEM_PASSWORD}\"}"

# update beats_system user's password
echo
echo "Update beats_system's password"
curl --fail -POST ${ELASTIC_HOST}/_security/user/beats_system/_password \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"password\": \"${BEATS_SYSTEM_PASSWORD}\"}"

# create user for filebeats
echo
echo "Create filebeat_writer role"
curl --fail -POST ${ELASTIC_HOST}/_security/role/filebeat_writer \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"cluster\": [\"monitor\", \"read_ilm\", \"read_pipeline\"], \"indices\": [{\"names\": [\"filebeat-*\", \"logs-*\"], \"privileges\": [\"create_doc\", \"view_index_metadata\", \"create_index\"]}]}"

echo "Create filebeat_monitoring role"
curl --fail -POST ${ELASTIC_HOST}/_security/role/filebeat_monitoring \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"cluster\": [\"monitor\"], \"indices\": [{\"names\": [\".monitoring-beats-*\"], \"privileges\": [\"create_doc\", \"create_index\"]}]}"

echo
echo "Create filebeat user"
curl --fail -POST ${ELASTIC_HOST}/_security/user/filebeats \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"password\": \"${BEATS_SYSTEM_PASSWORD}\", \"roles\": [\"filebeat_writer\", \"filebeat_monitoring\"]}"

# create kibana users
echo
echo "Create yomain user"
curl --fail -POST ${ELASTIC_HOST}/_security/user/yomain \
     --user elastic:${ELASTIC_PASSWORD} \
     --header "Content-Type: application/json" \
     --data "{\"password\": \"${KIBANA_YOMAIN_PASSWORD}\", \"roles\": [\"kibana_admin\", \"monitoring_user\", \"editor\"]}"

echo

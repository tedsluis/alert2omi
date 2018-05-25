RECEIVER=https://omi-receiver:30005/bsmc/rest/events/omi

echo -e "\n## XML post test message to receiver\n"
curl -v -k -X POST -d @testxml.xml -H 'Content-Type: text/xml' $RECEIVER/post


curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer 65A3ED66E48E0414085A730B713B70A9DF41FC7A1E7573490353BD691CEED554" \
     -X POST "https://a765f340-7836-4b30-9876-beadf29c5b52.pushnotifications.pusher.com/publish_api/v1/instances/a765f340-7836-4b30-9876-beadf29c5b52/publishes" \
     -d '{"interests":["hello"],"fcm":{"notification":{"title":"[Notification] Registration Was Successful!", "body":"Thank you for registering with us. Now you will receive email updates. Congratulations on a step towards saving energy!"}}}'

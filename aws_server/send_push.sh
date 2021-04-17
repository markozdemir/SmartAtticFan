curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer 65A3ED66E48E0414085A730B713B70A9DF41FC7A1E7573490353BD691CEED554" \
     -X POST "https://a765f340-7836-4b30-9876-beadf29c5b52.pushnotifications.pusher.com/publish_api/v1/instances/a765f340-7836-4b30-9876-beadf29c5b52/publishes" \
     -d '{"interests":["hello"],"fcm":{"notification":{"title":"[Alert] Your Attic Fan", "body":"Your attic fan appears no longer be working. Please check it as soon as you can."}}}'

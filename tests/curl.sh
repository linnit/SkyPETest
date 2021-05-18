#!/bin/bash

# Send GET request
curl http://localhost:8080

# Send HEAD request
curl -I http://localhost:8080

# Send POST request
curl -d "name=Ryan" http://localhost:8080/formsubmit



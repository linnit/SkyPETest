# Sky Performance Engineer Test

## Simple Python Web Server

```bash
./server.py [<port>]
```

The port argument is optional and by default will run on 8080.

The `/` endpoint contains the form to submit your name. The URL, for example, would be:

http://localhost:8080/

When the form is submitted, it is via a POST request to `/formsubmit`


# Performance Test

Set the URL of the web server

```bash
export MITE_CONF_url=http://localhost:8080
```

## Test individual journeys

```bash
mite journey test mite.sws:get_homepage
mite journey test mite.sws:post_form mite.sws:datapool
```

## Test the scenario

```bash
mite scenario test mite.sws:scenario
```

### Other Testing

[tests/curl.sh](tests/curl.sh) contains some curl commands I used to test functionality throughout and were useful without having to set up a full test scenario. 

---

## Things to improve

 - If further functionality was required, I would put the HTML into seperate files. That would make the code cleaner and stop the mixing of HTML and Python. It would also allow for the addition of CSS etc.
 - In the performance test, instead of populating the datapool via the `names.txt` file, use [data creation scenarios](https://sky-uk.github.io/mite/journeys.html#data-creation-scenarios).
 - Handle a wider range of errors. I.E.
    - None ascii characters produce a `UnicodeDecodeError`, can be tested with `$ curl -d "name=蘷" http://localhost:8080/formsubmit`
    - Client can cause an out-of-memory error as there's no check in the server regarding payload size. Can be tested with the following commands:
    ```bash
    dd if=/dev/zero of=testfile bs=1024 count=1024000
    curl -X POST --data-binary @testfile http://localhost:8080/formsubmit
    ```
"""
A package for testing the stress load on the server.

Since the httpx test client and pytest do not allow multiple requests
to be run asynchronously, stress tests are written in a separate package,
and tests are performed with the FastAPI application running.

Stress tests stress_get and stress_post cannot be considered objective tests
for high load, as they are done in a slightly tricky way.
They take as parameters the number of all requests and the number of wallets
to which requests will be made. After that, requests are sent asynchronously
to each wallet, but for each wallet, until a response from the previous request arrives,
a new one is not sent. That is, roughly speaking, several users are emulated,
who quickly but, most importantly, consistently send requests.
1000 requests with 1000 wallets can be considered the most reliable tests.
In this case, an average of 1 request is received from each user,
so roughly we can talk about 1000 rps.

The stress test stress_random allows you to test the code under higher load.
This test is more objective than others. It runs random queries in separate threads.
With this testing, we managed to test a load of 1000 requests in 2 seconds
(the application runs without problems).

The test results can be viewed in the results folder.

"""

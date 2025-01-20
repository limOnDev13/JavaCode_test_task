"""
A package for testing the stress load on the server.

Since the httpx test client and pytest do not allow multiple requests
to be run asynchronously, stress tests are written in a separate package,
and tests are performed with the FastAPI application running.
"""

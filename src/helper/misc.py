from fastapi import FastAPI, Request

app = FastAPI()


def host_address(request: Request):
    scheme = request.url.scheme
    hostname = request.url.hostname
    port = request.url.port  # Get the port from the request URL

    # Check if the hostname is a local address
    if hostname in ["localhost", "127.0.0.1"]:
        # Customize the local address URL with port if available
        port_str = f":{port}" if port else ""
        domain = f"{scheme}://localhost{port_str}"
    else:
        # Use the public hostname and include port if applicable
        port_str = f":{port}" if port else ""
        domain = f"{scheme}://{hostname}{port_str}"

    return domain

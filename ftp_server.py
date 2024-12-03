from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def start_ftp_server():
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Create an authorizer
    authorizer = DummyAuthorizer()
    
    # Add user with write permissions to uploads directory
    # Replace these credentials with secure ones
    authorizer.add_user("user", "password", upload_dir, perm="elradfmw")

    # Create handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create and start server
    server = FTPServer(("127.0.0.1", 21), handler)
    print(f"FTP server started. Upload directory: {upload_dir}")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()

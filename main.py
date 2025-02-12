import package.redfish_client as rf

if 1:
    # Configuration
    SERVER_IP = "10.0.0.28"
    SERVER_ENDPOINT = "redfish/v1/"
    SERVER_PORT_HTTP = "8000"
    SERVER_PORT_HTTPS = "8443"
    CLIENT_ID = "APT_123"
    CLIENT_PRIVATE_KEY_PATH = f"client_private_{CLIENT_ID}.pem"
    HTTPS_CERT_PATH = "fullchain.pem"  # HTTPS certificate path


if True:
    if True:
        # Load the ECDSA private key
        print("Loading ECDSA private key...")
        private_key = rf.load_ecdsa_private_key(CLIENT_PRIVATE_KEY_PATH)
        print("Private key loaded successfully.")

        if 1:
            if 1:
                if 1:
                    # HTTPS GET test
                    https_url: str = (
                        f"https://{SERVER_IP}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
                    )
                    print("Sending HTTPS GET request...")
                    response = rf.send_get_https(
                        https_url,
                        private_key,
                        CLIENT_ID,
                        verify_cert=True,
                        cert_path=HTTPS_CERT_PATH,
                    )
                    print(f"HTTPS GET Status Code: {response.status_code}")
                    print(f"HTTPS GET Response: {response.text}")

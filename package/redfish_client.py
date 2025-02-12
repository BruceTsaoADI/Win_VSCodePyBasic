import os
import json
import time
import base64
import hashlib
import requests
from ecdsa import VerifyingKey, SigningKey, NIST256p

# Configuration
SERVER_IP = "10.0.0.21"
# SERVER_IP = "127.0.0.1"
SERVER_ENDPOINT = "redfish/v1/"
SERVER_PORT_HTTP = "8000"
SERVER_PORT_HTTPS = "8443"
CLIENT_ID = "APT_123"
CLIENT_PRIVATE_KEY_PATH = f"client_private_{CLIENT_ID}.pem"
HTTPS_CERT_PATH = "fullchain.pem"  # Ensure HTTPS verification

# Protocol
IS_HTTPS = 0

# Normal Process
NORMAL_TEST = 1
DO_GET = 1
DO_PATCH = 1

# Configure attack types (Set True to enable specific attack tests)
ATTACK_TEST = 0  # Luanch Attack Test
ATTACK_NULL = 0  # Null Attack (Missing Headers)
ATTACK_MALICIOUS_INPUT = 1  # Malicious Input Attack (Invalid Timestamp)
ATTACK_REPLAY = 0  # Replay Attack (Reuse Nonce)
ATTACK_TIMESTAMP_FUTURE = 0  # Future Timestamp Attack
ATTACK_TIMESTAMP_PAST = 0  # Expired Timestamp Attack


def load_ecdsa_private_key(key_path):
    """Load ECDSA private key"""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Private key file not found: {key_path}")

    with open(key_path, "r") as f:
        return SigningKey.from_pem(f.read())  # Return ECDSA SigningKey object


def generate_nonce():
    """Generate a random nonce"""
    return base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")


def sign_message(private_key, message):
    """Sign the message using ECDSA"""
    message_bytes = message.encode("utf-8")
    message_hash = hashlib.sha256(message_bytes).digest()
    signature = private_key.sign(message_hash)
    return base64.b64encode(signature).decode("utf-8")


def send_get(
    server_ip: str,  # Server IP (e.g., "10.0.0.21")
    client_private_key: str,  # Client's ECDSA private key (PEM)
    client_id: str,  # Client ID
    verify_cert: bool,  # Whether to verify HTTPS certificate
    cert_path: str = None,  # Path to the certificate (used if verify_cert=True)
):
    """Send a GET request with ECDSA signature"""
    timestamp = int(time.time())
    nonce = generate_nonce()

    # **Sign only the timestamp and nonce for GET**
    sign_data = json.dumps(
        {"timestamp": str(timestamp), "nonce": nonce}, separators=(",", ":")
    )

    # Generate signature
    signature = sign_message(client_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    # Determine protocol based on verify_cert and send GET request
    if verify_cert:
        url = f"https://{server_ip}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
        response = requests.get(url, headers=headers, verify=cert_path)
    else:
        url = f"http://{server_ip}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"
        response = requests.get(url, headers=headers, verify=False)

    return response


def send_patch(
    server_ip: str,  # Server IP (e.g., "10.0.0.21")
    client_private_key: str,  # Client's ECDSA private key (PEM)
    client_id: str,  # Client ID
    data: dict,  # Data to be sent in the PATCH request
    verify_cert: bool,  # Whether to verify HTTPS certificate
    cert_path: str = None,  # Path to the certificate (used if verify_cert=True)
):
    """Send a GET request with ECDSA signature"""
    timestamp = int(time.time())
    nonce = generate_nonce()

    # **Sign only the timestamp and nonce for GET**
    sign_data = json.dumps(data, separators=(",", ":"))

    # Generate signature
    signature = sign_message(client_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    # Determine protocol based on verify_cert and send GET request
    if verify_cert:
        url = f"https://{server_ip}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
        response = requests.patch(url, headers=headers, json=data, verify=cert_path)
    else:
        url = f"http://{server_ip}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"
        response = requests.patch(url, headers=headers, json=data, verify=False)

    return response


# Simple test script
if __name__ == "__main__":

    def attack_test(
        server_ip, client_private_key, client_id, verify_cert, cert_path=None
    ):
        """Perform different types of attack tests based on enabled attack flags."""

        timestamp = int(time.time())
        nonce = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")

        print("\n=============================================")
        print("Starting Attack Test...")

        # Modify timestamp/nonce based on attack types
        if ATTACK_NULL:
            print(
                "[ATTACK] Null Attack: Sending request with missing security headers."
            )
            headers = {}  # Send request without security headers
        else:
            if ATTACK_MALICIOUS_INPUT:
                print(
                    "[ATTACK] Malicious Input Attack: Injecting an invalid timestamp."
                )
                timestamp = "INVALID_TIMESTAMP"  # Inject invalid timestamp

            if ATTACK_REPLAY:
                print("[ATTACK] Replay Attack: Using a fixed nonce for replay attack.")
                nonce = "FIXED_NONCE"  # Use a constant nonce for replay attack

            if ATTACK_TIMESTAMP_FUTURE:
                print(
                    "[ATTACK] Future Timestamp Attack: Setting timestamp too far in the future."
                )
                timestamp = int(time.time()) + 999999  # Set timestamp far in the future

            if ATTACK_TIMESTAMP_PAST:
                print("[ATTACK] Expired Timestamp Attack: Using an expired timestamp.")
                timestamp = int(time.time()) - 999999  # Use an expired timestamp

            # Generate signed message
            sign_data = json.dumps(
                {"timestamp": str(timestamp), "nonce": nonce}, separators=(",", ":")
            )
            signature = sign_message(client_private_key, sign_data)

            headers = {
                "Content-Type": "application/json",
                "X-Timestamp": str(timestamp),
                "X-Nonce": nonce,
                "X-Client-ID": client_id,
                "X-Signature": signature,
            }

        # Determine protocol based on verify_cert
        if verify_cert:
            url = f"https://{server_ip}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
        else:
            url = f"http://{server_ip}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"

        # Send GET request
        print("\nSending attack test request to:")
        print(f"{url}")
        print("\nHeaders:")
        print(json.dumps(headers, indent=4))

        if verify_cert:
            response = requests.get(url, headers=headers, verify=cert_path)
        else:
            response = requests.get(url, headers=headers, verify=False)

        # Print the response
        print("\nAttack Test Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print("=============================================\n")

    try:
        # Load client ECDSA private key
        print("Loading ECDSA private key...")
        private_key = load_ecdsa_private_key(CLIENT_PRIVATE_KEY_PATH)
        print(" Private key loaded successfully.")

        ########################### Normal Request ###########################
        if NORMAL_TEST:
            if DO_GET:
                # Send Get
                print(f"Sending {'HTTPS' if IS_HTTPS else 'HTTP'} GET request...")
                response = send_get(
                    server_ip=SERVER_IP,
                    client_private_key=private_key,
                    client_id=CLIENT_ID,
                    verify_cert=IS_HTTPS,
                    cert_path=HTTPS_CERT_PATH,
                )
                print(f" GET Status Code: {response.status_code}")
                print(f" GET Response: {response.text}")

            if DO_PATCH:
                # Send Patch
                print(f"Sending {'HTTPS' if IS_HTTPS else 'HTTP'} PATCH request...")
                patch_data = {"temperature": 25.5, "humidity": 60}
                response = send_patch(
                    server_ip=SERVER_IP,
                    client_private_key=private_key,
                    client_id=CLIENT_ID,
                    data=patch_data,
                    verify_cert=IS_HTTPS,
                    cert_path=HTTPS_CERT_PATH,
                )
                print(f" GET Status Code: {response.status_code}")
                print(f" GET Response: {response.text}")
        #################################################################################

        ########################### ATTACK TEST ###########################
        # Attack test
        if ATTACK_TEST:
            print(f"\n\nATTACK!! ATTACK!!")
            attack_test(
                server_ip=SERVER_IP,
                client_private_key=private_key,
                client_id=CLIENT_ID,
                verify_cert=IS_HTTPS,
                cert_path=HTTPS_CERT_PATH,
            )
        #################################################################################

    except FileNotFoundError as e:
        print(f" Error: {e}")
    except requests.exceptions.SSLError:
        print(" SSL Error: Invalid HTTPS certificate.")
    except requests.exceptions.ConnectionError:
        print(" Connection Error: Unable to reach the server.")
    except Exception as e:
        print(f" Unexpected Error: {e}")

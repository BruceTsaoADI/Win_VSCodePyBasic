#!/usr/bin/env python3
"""
Program: redfish_client.py
Description: This program provides utility functions to send HTTP and HTTPS GET and PATCH requests with ECDSA signatures.
             It supports normal operations as well as various attack tests by modifying request parameters (e.g., invalid timestamps,
             missing headers, etc.). The program demonstrates how to sign messages using an ECDSA private key, generate a nonce,
             and send secure requests to a Redfish service endpoint.
Usage: Configure the server IP, ports, client ID, and certificate paths below. Then run the script to perform GET/PATCH requests
       and optional attack tests.
"""

import os
import json
import time
import base64
import hashlib
import requests
from ecdsa import SigningKey
from typing import Optional, Dict, Any


def load_ecdsa_private_key(key_path: str) -> SigningKey:
    """Load the ECDSA private key from a PEM file."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Private key file not found: {key_path}")
    with open(key_path, "r") as f:
        return SigningKey.from_pem(f.read())


def generate_nonce() -> str:
    """Generate a random nonce."""
    return base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")


def sign_message(private_key: SigningKey, message: str) -> str:
    """Sign the message using ECDSA and return the base64 encoded signature."""
    message_bytes = message.encode("utf-8")
    message_hash = hashlib.sha256(message_bytes).digest()
    signature = private_key.sign(message_hash)
    return base64.b64encode(signature).decode("utf-8")


def send_get_http(
    server_url: str, client_ecdsa_private_key: SigningKey, client_id: str
) -> requests.Response:
    """
    Send a GET request over HTTP with an ECDSA signature.

    :param server_url: The complete HTTP URL (e.g., "http://10.0.0.21:8000/redfish/v1/")
    :param client_ecdsa_private_key: The loaded ECDSA private key (SigningKey object)
    :param client_id: Client ID
    :return: The response object returned by the requests library
    """
    timestamp = int(time.time())
    nonce = generate_nonce()
    sign_data = json.dumps(
        {"timestamp": str(timestamp), "nonce": nonce}, separators=(",", ":")
    )
    signature = sign_message(client_ecdsa_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    response = requests.get(server_url, headers=headers, verify=False)
    return response


def send_get_https(
    server_url: str,
    client_ecdsa_private_key: SigningKey,
    client_id: str,
    verify_cert: bool,
    cert_path: str,
) -> requests.Response:
    """
    Send a GET request over HTTPS with an ECDSA signature.

    :param server_url: The complete HTTPS URL (e.g., "https://10.0.0.21:8443/redfish/v1/")
    :param client_ecdsa_private_key: The loaded ECDSA private key (SigningKey object)
    :param client_id: Client ID
    :param verify_cert: Whether to verify the certificate (True/False)
    :param cert_path: Path to the certificate file
    :return: The response object returned by the requests library
    """
    timestamp = int(time.time())
    nonce = generate_nonce()
    sign_data = json.dumps(
        {"timestamp": str(timestamp), "nonce": nonce}, separators=(",", ":")
    )
    signature = sign_message(client_ecdsa_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    response = requests.get(
        server_url, headers=headers, verify=cert_path if verify_cert else False
    )
    return response


def send_patch_http(
    server_url: str,
    client_ecdsa_private_key: SigningKey,
    client_id: str,
    data: Dict[str, Any],
) -> requests.Response:
    """
    Send a PATCH request over HTTP with an ECDSA signature, using the provided data as the signing content.

    :param server_url: The complete HTTP URL (e.g., "http://10.0.0.21:8000/redfish/v1/")
    :param client_ecdsa_private_key: The loaded ECDSA private key (SigningKey object)
    :param client_id: Client ID
    :param data: The JSON data to be sent (dictionary)
    :return: The response object returned by the requests library
    """
    timestamp = int(time.time())
    nonce = generate_nonce()
    sign_data = json.dumps(data, separators=(",", ":"))
    signature = sign_message(client_ecdsa_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    response = requests.patch(server_url, headers=headers, json=data, verify=False)
    return response


def send_patch_https(
    server_url: str,
    client_ecdsa_private_key: SigningKey,
    client_id: str,
    data: Dict[str, Any],
    verify_cert: bool,
    cert_path: str,
) -> requests.Response:
    """
    Send a PATCH request over HTTPS with an ECDSA signature, using the provided data as the signing content.

    :param server_url: The complete HTTPS URL (e.g., "https://10.0.0.21:8443/redfish/v1/")
    :param client_ecdsa_private_key: The loaded ECDSA private key (SigningKey object)
    :param client_id: Client ID
    :param data: The JSON data to be sent (dictionary)
    :param verify_cert: Whether to verify the certificate (True/False)
    :param cert_path: Path to the certificate file
    :return: The response object returned by the requests library
    """
    timestamp = int(time.time())
    nonce = generate_nonce()
    sign_data = json.dumps(data, separators=(",", ":"))
    signature = sign_message(client_ecdsa_private_key, sign_data)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
        "X-Client-ID": client_id,
        "X-Signature": signature,
    }

    response = requests.patch(
        server_url,
        headers=headers,
        json=data,
        verify=cert_path if verify_cert else False,
    )
    return response


# ---------------------------------------------------------------------------
# The following section is the test code.
# From here on, the code sets configuration parameters and executes tests.
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # Configuration
    SERVER_IP = "10.0.0.28"
    SERVER_ENDPOINT = "redfish/v1/"
    SERVER_PORT_HTTP = "8000"
    SERVER_PORT_HTTPS = "8443"
    CLIENT_ID = "APT_123"
    CLIENT_PRIVATE_KEY_PATH = f"client_private_{CLIENT_ID}.pem"
    HTTPS_CERT_PATH = "fullchain.pem"  # HTTPS certificate path

    # Protocol
    HTTPS = 1

    # Normal Process settings
    NORMAL_TEST = 1
    DO_GET = 1
    DO_PATCH = 1

    # Configure attack types (attack test settings)
    ATTACK_TEST = 1  # Launch Attack Test
    ATTACK_NULL = 0  # Null Attack (missing headers)
    ATTACK_MALICIOUS_INPUT = 1  # Malicious Input Attack (invalid timestamp)
    ATTACK_REPLAY = 0  # Replay Attack (reuse nonce)
    ATTACK_TIMESTAMP_FUTURE = 0  # Future Timestamp Attack
    ATTACK_TIMESTAMP_PAST = 0  # Expired Timestamp Attack

    def attack_test(
        server_url: str,
        client_ecdsa_private_key: SigningKey,
        client_id: str,
        verify_cert: bool,
        cert_path: Optional[str] = None,
    ) -> None:
        """
        Perform various attack tests based on the configured attack flags (same logic as the original program).

        Global attack flags (ATTACK_NULL, ATTACK_MALICIOUS_INPUT, etc.) should be defined in the test section.
        """
        timestamp = int(time.time())
        nonce = generate_nonce()

        print("\n=============================================")
        print("Starting Attack Test...")

        if ATTACK_NULL:
            print(
                "[ATTACK] Null Attack: Sending request with missing security headers."
            )
            headers = {}  # Do not send security headers
        else:
            if ATTACK_MALICIOUS_INPUT:
                print(
                    "[ATTACK] Malicious Input Attack: Injecting an invalid timestamp."
                )
                timestamp = "INVALID_TIMESTAMP"  # Invalid timestamp
            if ATTACK_REPLAY:
                print("[ATTACK] Replay Attack: Using a fixed nonce for replay attack.")
                nonce = "FIXED_NONCE"
            if ATTACK_TIMESTAMP_FUTURE:
                print(
                    "[ATTACK] Future Timestamp Attack: Setting timestamp too far in the future."
                )
                timestamp = int(time.time()) + 999999
            if ATTACK_TIMESTAMP_PAST:
                print("[ATTACK] Expired Timestamp Attack: Using an expired timestamp.")
                timestamp = int(time.time()) - 999999

            sign_data = json.dumps(
                {"timestamp": str(timestamp), "nonce": nonce}, separators=(",", ":")
            )
            signature = sign_message(client_ecdsa_private_key, sign_data)

            headers = {
                "Content-Type": "application/json",
                "X-Timestamp": str(timestamp),
                "X-Nonce": nonce,
                "X-Client-ID": client_id,
                "X-Signature": signature,
            }

        print("\nSending attack test request to:")
        print(server_url)
        print("\nHeaders:")
        print(json.dumps(headers, indent=4))

        response = requests.get(
            server_url, headers=headers, verify=cert_path if verify_cert else False
        )
        print("\nAttack Test Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print("=============================================\n")

    try:
        # Load the ECDSA private key
        print("Loading ECDSA private key...")
        private_key = load_ecdsa_private_key(CLIENT_PRIVATE_KEY_PATH)
        print("Private key loaded successfully.")

        if NORMAL_TEST:
            if DO_GET:
                if HTTPS:
                    # HTTPS GET test
                    https_url = (
                        f"https://{SERVER_IP}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
                    )
                    print("Sending HTTPS GET request...")
                    response = send_get_https(
                        https_url,
                        private_key,
                        CLIENT_ID,
                        verify_cert=True,
                        cert_path=HTTPS_CERT_PATH,
                    )
                    print(f"HTTPS GET Status Code: {response.status_code}")
                    print(f"HTTPS GET Response: {response.text}")
                else:
                    # HTTP GET test
                    http_url = (
                        f"http://{SERVER_IP}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"
                    )
                    print("Sending HTTP GET request...")
                    response = send_get_http(http_url, private_key, CLIENT_ID)
                    print(f"HTTP GET Status Code: {response.status_code}")
                    print(f"HTTP GET Response: {response.text}")

            if DO_PATCH:
                patch_data = {"temperature": 25.5, "humidity": 60}
                if HTTPS:
                    # HTTPS PATCH test
                    https_url = (
                        f"https://{SERVER_IP}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
                    )
                    print("Sending HTTPS PATCH request...")
                    response = send_patch_https(
                        https_url,
                        private_key,
                        CLIENT_ID,
                        patch_data,
                        verify_cert=True,
                        cert_path=HTTPS_CERT_PATH,
                    )
                    print(f"HTTPS PATCH Status Code: {response.status_code}")
                    print(f"HTTPS PATCH Response: {response.text}")
                else:
                    # HTTP PATCH test
                    http_url = (
                        f"http://{SERVER_IP}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"
                    )
                    print("Sending HTTP PATCH request...")
                    response = send_patch_http(
                        http_url, private_key, CLIENT_ID, patch_data
                    )
                    print(f"HTTP PATCH Status Code: {response.status_code}")
                    print(f"HTTP PATCH Response: {response.text}")

        # Attack test (same logic as the original program)
        if ATTACK_TEST:
            if HTTPS:
                test_url = f"https://{SERVER_IP}:{SERVER_PORT_HTTPS}/{SERVER_ENDPOINT}"
            else:
                test_url = f"http://{SERVER_IP}:{SERVER_PORT_HTTP}/{SERVER_ENDPOINT}"
            attack_test(
                test_url,
                private_key,
                CLIENT_ID,
                verify_cert=True,
                cert_path=HTTPS_CERT_PATH,
            )

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except requests.exceptions.SSLError:
        print("SSL Error: Invalid HTTPS certificate.")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Unable to reach the server.")
    except Exception as e:
        print(f"Unexpected Error: {e}")

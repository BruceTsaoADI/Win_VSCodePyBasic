from security_utils import validate_timestamp_nonce, verify_ecdsa_signature


def do_PATCH(self):
    """Handle PATCH request with replay attack prevention and ECDSA signature verification"""

    logger.info("   PATCH: Headers: {}".format(self.headers))
    ctype, pdict = multipart.parse_options_header(
        self.headers.get("content-type", None)
    )
    logger.info("   PATCH: Content: type={} and params={}".format(ctype, pdict))
    self.try_to_sleep("PATCH", self.path)

    # 讀取 Body
    data_received = None
    if "content-length" in self.headers:
        lenn = int(self.headers["content-length"])
        try:
            data_received = json.loads(self.rfile.read(lenn).decode("utf-8"))
        except ValueError:
            logger.error("Decoding JSON has failed, sending 400")
            self.send_response(400)
            self.end_headers()
            return

    if data_received:
        logger.info("   PATCH: Data: {}".format(data_received))

        # **防重播攻擊 (檢查 timestamp & nonce)**
        is_valid, error_response = validate_timestamp_nonce(self.headers)
        if not is_valid:
            logger.error(f"Replay attack detected: {error_response}")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
            return

        # **ECDSA 簽章驗證**
        client_id = self.headers.get("X-Client-ID")
        if client_id not in self.server.client_public_keys:
            logger.error(f"Invalid Client ID: {client_id}")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid client ID"}).encode())
            return

        client_public_key = self.server.client_public_keys[client_id]
        is_valid, error_response = verify_ecdsa_signature(
            self.headers, data_received, client_public_key
        )
        if not is_valid:
            logger.error(f"ECDSA verification failed: {error_response}")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
            return

        # **繼續執行 PATCH 操作**
        fpath = self.construct_path(self.path, "index.json")
        success, payload = self.get_cached_link(fpath)

        if success:
            # 如果是 Collection，返回 405
            if payload.get("Members") is not None:
                self.send_response(405)
            else:
                logger.info(self.headers.get("content-type"))
                logger.info(data_received)
                logger.info(payload)
                dict_merge(payload, data_received)
                logger.info(payload)
                self.patchedLinks[fpath] = payload
                self.send_response(204)
        else:
            self.send_response(404)
    else:
        self.send_response(400)

    self.end_headers()


###############################################################################################################

from security_utils import validate_timestamp_nonce, verify_ecdsa_signature


def do_PUT(self):
    """Handle PUT requests with replay attack prevention and ECDSA verification"""

    logger.info("   PUT: Headers: {}".format(self.headers))

    # Parse content-type
    ctype, pdict = multipart.parse_options_header(
        self.headers.get("content-type", None)
    )
    logger.info("   PUT: Content: type={} and params={}".format(ctype, pdict))

    self.try_to_sleep("PUT", self.path)

    # Read JSON body
    data_received = None
    if "content-length" in self.headers:
        lenn = int(self.headers["content-length"])
        try:
            data_received = json.loads(self.rfile.read(lenn).decode("utf-8"))
        except ValueError:
            logger.error("Decoding JSON failed")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

    logger.info("   PUT: Data: {}".format(data_received))

    # ✅ Step 1: Validate Timestamp & Nonce (防重播攻擊)
    is_valid_nonce, nonce_response = validate_timestamp_nonce(self.headers)
    if not is_valid_nonce:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(nonce_response).encode())
        return

    # ✅ Step 2: Verify ECDSA Signature
    client_id = self.headers.get("X-Client-ID")
    if client_id not in self.server.client_public_keys:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"error": f"Invalid client ID: {client_id}"}).encode()
        )
        return

    client_public_key = self.server.client_public_keys[client_id]
    is_valid_signature, signature_response = verify_ecdsa_signature(
        self.headers, data_received, client_public_key
    )
    if not is_valid_signature:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(signature_response).encode())
        return

    # ✅ If all checks pass, proceed with 405 (as PUT is not supported)
    self.send_response(405)
    self.end_headers()


###########################################################################
from security_utils import validate_timestamp_nonce, verify_ecdsa_signature

# 在 server 啟動時載入所有 client public keys
KEY_PATH = "/etc/keys"
CLIENT_PUBLIC_KEYS = load_client_public_keys(KEY_PATH)


def do_POST(self):
    """Handle POST request with replay attack prevention and ECDSA verification"""

    logger.info("   POST: Headers: {}".format(self.headers))
    ctype, pdict = multipart.parse_options_header(
        self.headers.get("content-type", None)
    )
    logger.info("   POST: Content: type={} and params={}".format(ctype, pdict))

    if "content-length" in self.headers:
        lenn = int(self.headers["content-length"])
        if lenn == 0:
            data_received = {}
        else:
            try:
                data_received = json.loads(self.rfile.read(lenn).decode("utf-8"))
            except ValueError:
                logger.error("Decoding JSON has failed, sending 400")
                self.send_response(400)
                self.end_headers()
                return
    else:
        self.send_response(411)
        self.end_headers()
        return

    self.try_to_sleep("POST", self.path)

    # 🔹 防重播攻擊檢查
    is_valid, error_response = validate_timestamp_nonce(self.headers)
    if not is_valid:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(error_response).encode())
        return

    # 🔹 取得 client_id 並進行 ECDSA 簽章驗證
    client_id = self.headers.get("X-Client-ID")
    if client_id not in CLIENT_PUBLIC_KEYS or CLIENT_PUBLIC_KEYS[client_id] is None:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"error": f"Invalid client ID: {client_id}"}).encode()
        )
        return

    client_public_key = CLIENT_PUBLIC_KEYS[client_id]
    is_valid, error_response = verify_ecdsa_signature(
        self.headers, data_received, client_public_key
    )

    if not is_valid:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(error_response).encode())
        return

    # 🔹 簽章驗證成功，繼續執行原始 do_POST() 邏輯
    logger.info("   POST: Data: {}".format(data_received))
    fpath = self.construct_path(self.path, "index.json")
    success, payload = self.get_cached_link(fpath)

    if success:
        if payload.get("Members") is None:
            self.send_response(405)
        else:
            logger.info(data_received)
            newpath = self.add_new_member(payload, data_received)
            newfpath = self.construct_path(newpath, "index.json")
            self.patchedLinks[newfpath] = data_received
            self.patchedLinks[fpath] = payload
            self.send_response(204)
            self.send_header("Location", newpath)
            self.send_header("Content-Length", "0")
            if "SessionService/Sessions" in self.path:
                self.send_header("X-Auth-Token", "1234567890ABCDEF")
            self.end_headers()
    else:
        self.send_response(400)
        self.end_headers()

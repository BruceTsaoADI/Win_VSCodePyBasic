<<<<<<< HEAD
import time

def c2py_macro_read(macro: str) -> tuple:
    macro_name = ''
    macro_exp = ''
    segments = macro.split(' ')
    macro_name = segments[1]
    for s in segments[2:]:
        if s.startswith('"'):
            macro_exp = s
            break
        elif s.startswith('0x'):
            macro_exp = int(s, 0)
            break
        elif s.isdigit():
            macro_exp = int(s)
            break
    return macro_name, macro_exp




def c2py_collect_macro(path: str) -> dict:
    ''' To collect all macro in the C or H file and save as Python dictionary.'''
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_macro = {}
    dict_key = ''
    dict_val = ''
    for line in lines:
        line = line.replace('\n', '')
        if line.startswith('#define') and line.find('__') == -1:
            dict_key, dict_val = c2py_macro_read(line)
            dict_macro[dict_key] = dict_val
    return dict_macro


def c2py_collect_array(path: str) -> dict:
    """ To collect all array in the C or H file and save as Python dictionary."""
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_array = {}
    dict_key = ''
    dict_val = []
    array_start = False
    for line in lines:
        if line.startswith('ADI_REG_TYPE'):
            array_name = line.split(' ')[1]
            index_name_end = array_name.find('[')
            dict_key = array_name[:index_name_end]
            dict_val = []
            array_start = True

        if array_start:
            if line.startswith('0x'):
                if line.find(',') == -1:
                    dict_val.append(int(line, 0))
                else:
                    for i in line.split(', '):
                        if i.startswith('0x'):
                            dict_val.append(int(i, 0))
            elif line.startswith('};'):
                array_start = False
                dict_array[dict_key] = dict_val
    return dict_array


def c2py_collect_func(path: str) -> dict:
    """ To collect all array in the C or H file and save as Python dictionary."""
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_func = {}
    dict_key = ''
    dict_val = ''
    func_start = False
    for line in lines:
        # line = line.replace('\n', '')

        if line.startswith('void'):
            func_name = line.split(' ')[1]
            index_name_end = func_name.find('(')
            dict_key = func_name[:index_name_end]
            func_val = []
            func_start = True
            subfun_name = ''
            subfun_devaddr = ''
            subfun_regaddr = ''
            subfun_regbyte = ''
            subfun_regvalue = ''

        if func_start:
            line = line.strip('\t')
            if line.startswith('SIGMA_WRITE_REGISTER_BLOCK'):
                subfun_name = 'SIGMA_WRITE_REGISTER_BLOCK'
                line = line.split('(')[1]
                line = line.split(');')[0]
                argus = line.split(',')
                subfun_devaddr = argus[0].strip()
                subfun_regaddr = argus[1].strip()
                subfun_regbyte = argus[2].strip()
                subfun_regvalue = argus[3].strip()
                func_val.append([subfun_name, subfun_devaddr, subfun_regaddr, subfun_regbyte, subfun_regvalue])
            elif line.startswith('SIGMA_WRITE_DELAY'):
                subfun_name = 'SIGMA_WRITE_DELAY'
                line = line.split('(')[1]
                line = line.split(');')[0]
                argus = line.split(',')
                subfun_devaddr = argus[0].strip()
                subfun_regbyte = argus[1].strip()
                subfun_regvalue = argus[2].strip()
                func_val.append([subfun_name, subfun_devaddr, subfun_regbyte, subfun_regvalue])
            if line.startswith('}'):
                func_start = False
                dict_func[dict_key] = func_val

    return dict_func


file_paths = [
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA_REG.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA_PARAM.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST_REG.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST_PARAM.h',
    ]
c2py_macro = {}
for path in file_paths:
    c2py_macro.update(c2py_collect_macro(path))
# print(c2py_macro)
# print(c2py_macro['R5_MBIAS1_EN_IC_1_Sigma_SHIFT'])

c2py_array = {}
for path in file_paths:
    c2py_array.update(c2py_collect_array(path))
# print(c2py_array)
# print(c2py_array['R1_FDSP_RUN_IC_1_Fast_Default'])

c2py_func = {}
for path in file_paths:
    c2py_func.update(c2py_collect_func(path))
#print(c2py_func)
# print(c2py_func['SEQ_MUTELEFT_download'])
=======
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
>>>>>>> dev_text_search

    logger.info("   POST: Headers: {}".format(self.headers))
    ctype, pdict = multipart.parse_options_header(
        self.headers.get("content-type", None)
    )
    logger.info("   POST: Content: type={} and params={}".format(ctype, pdict))

<<<<<<< HEAD
dict_marco_array = {}
dict_marco_array.update(c2py_macro)
dict_marco_array.update(c2py_array)

str = time.time()
print('Start download.')
for f in c2py_func:
    for i in c2py_func[f]:
        func_name = i[0]
        if func_name == 'SIGMA_WRITE_REGISTER_BLOCK':
            dev_addr = dict_marco_array[i[1]]
            reg_addr = dict_marco_array[i[2]]
            reg_byte = dict_marco_array[i[3]]
            reg_value = dict_marco_array[i[4]]
            [print(hex(i)) for i in reg_value if i > 5]
            # print(dev_addr, reg_addr, reg_byte, reg_value)
            # gmsl_reg_write(I2C_BUS_01, dev_addr, reg_addr, reg_value)

        if func_name == 'SIGMA_WRITE_DELAY':
            dev_addr = dict_marco_array[i[1]]
            reg_byte = dict_marco_array[i[2]]
            reg_value = dict_marco_array[i[3]]

            delay_ms = 0
            for i in range(reg_byte):
                delay_ms = (delay_ms << 8) + reg_value[i]
            time.sleep(delay_ms/1000)
            print(f'Delay {delay_ms} ms')
print('End download.')
print(f'Elapse: {time.time() - str}')
=======
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
>>>>>>> dev_text_search

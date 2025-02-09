import ecdsa

# Configuration
CLIENT_ID = "APT_123"
PRIVATE_KEY_NAME = "client_private_" + CLIENT_ID + ".pem"
PUBLIC_KEY_NAME = "client_public_" + CLIENT_ID + ".pem"


def generate_ecdsa_keys(
    private_path="private_key.pem", public_path="public_key.pem", curve=ecdsa.NIST256p
):
    """
    產生 ECDSA 金鑰對（預設使用 SECP256r1，也就是 NIST256p），
    並將私鑰和公鑰以 PEM 格式分別儲存到指定的檔案中。

    Args:
        private_path (str): 儲存私鑰的檔案路徑，預設 "private_key.pem"。
        public_path (str): 儲存公鑰的檔案路徑，預設 "public_key.pem"。
        curve: 橢圓曲線參數，預設為 ecdsa.NIST256p（即 SECP256r1）。

    Returns:
        tuple: (SigningKey, VerifyingKey)，分別為生成的私鑰和公鑰物件。
    """
    # 產生私鑰及對應的公鑰
    sk = ecdsa.SigningKey.generate(curve=curve)
    vk = sk.get_verifying_key()

    # 將金鑰轉換成 PEM 格式後寫入檔案
    with open(private_path, "wb") as f:
        f.write(sk.to_pem())
    with open(public_path, "wb") as f:
        f.write(vk.to_pem())

    print(f"已生成金鑰並儲存到：\n  私鑰 -> {private_path}\n  公鑰 -> {public_path}")
    return sk, vk


def load_pem_key(file_path, key_type="private"):
    """
    根據指定檔案路徑讀取 PEM 格式的金鑰。

    Args:
        file_path (str): PEM 格式金鑰所在的檔案路徑。
        key_type (str): 指定讀取的金鑰類型，可選 "private" 或 "public"（不區分大小寫）。

    Returns:
        ecdsa.SigningKey 或 ecdsa.VerifyingKey：根據 key_type 返回對應的金鑰物件。

    Raises:
        ValueError: 如果 key_type 不是 "private" 或 "public" 則拋出例外。
    """
    with open(file_path, "rb") as f:
        pem_data = f.read()

    if key_type.lower() == "private":
        return ecdsa.SigningKey.from_pem(pem_data)
    elif key_type.lower() == "public":
        return ecdsa.VerifyingKey.from_pem(pem_data)
    else:
        raise ValueError("key_type 必須是 'private' 或 'public'")


# 範例使用
if __name__ == "__main__":
    # 產生金鑰並儲存到本機
    sk, vk = generate_ecdsa_keys(
        private_path=PRIVATE_KEY_NAME, public_path=PUBLIC_KEY_NAME
    )

    # 從檔案讀取 PEM 格式的私鑰與公鑰
    loaded_sk = load_pem_key(PRIVATE_KEY_NAME, key_type="private")
    loaded_vk = load_pem_key(PUBLIC_KEY_NAME, key_type="public")

    # 驗證讀取的金鑰是否正確（簽章驗證）
    message = b"test msg"
    signature = loaded_sk.sign(message)

    try:
        if loaded_vk.verify(signature, message):
            print("讀取的金鑰簽章驗證成功！")
    except ecdsa.BadSignatureError:
        print("讀取的金鑰簽章驗證失敗！")

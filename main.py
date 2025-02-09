import ecdsa

# 1. 產生 ECDSA 私鑰對，使用 NIST256p（即 SECP256r1）
sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
vk = sk.get_verifying_key()

# 2. 將私鑰與公鑰轉換為 PEM 格式
pem_private = sk.to_pem()
pem_public = vk.to_pem()

# 3. 將 PEM 格式的金鑰儲存到本機檔案中
with open("private_key.pem", "wb") as f:
    f.write(pem_private)

with open("public_key.pem", "wb") as f:
    f.write(pem_public)

print(
    "已生成 SECP256r1 (NIST256p) 的公私鑰，分別儲存於 private_key.pem 和 public_key.pem"
)

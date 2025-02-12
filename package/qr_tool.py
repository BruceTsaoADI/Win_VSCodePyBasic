import qrcode
import cv2
from pyzbar.pyzbar import decode


def generate_qr(data, output_file="qrcode.png"):
    """生成 QR Code 並儲存為圖片"""
    qr = qrcode.QRCode(
        version=1,  # 控制 QR Code 的尺寸（1~40，數字越大，尺寸越大）
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 容錯率：L 7%，M 15%，Q 25%，H 30%
        box_size=10,  # 每個方塊的像素大小
        border=4,  # 邊框大小
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(output_file)
    print(f"✅ QR Code 已生成並儲存為 {output_file}")


def decode_qr(image_path):
    """讀取並解碼 QR Code 圖片"""
    image = cv2.imread(image_path)
    decoded_objects = decode(image)

    if not decoded_objects:
        print("❌ 無法在圖片中找到 QR Code。")
        return None

    for obj in decoded_objects:
        decoded_text = obj.data.decode("utf-8")
        print(f"✅ QR Code 內容: {decoded_text}")
        return decoded_text


if __name__ == "__main__":
    # 測試用數據
    test_data = "https://www.example.com"
    test_qr_file = "test_qrcode.png"

    # 1. 生成 QR Code
    generate_qr(test_data, test_qr_file)

    # 2. 解析剛剛生成的 QR Code
    decoded_result = decode_qr(test_qr_file)

    # 驗證是否正確解碼
    if decoded_result == test_data:
        print("🎉 測試成功！QR Code 生成與解碼匹配！")
    else:
        print("⚠️ 測試失敗，解碼內容與原始數據不符。")

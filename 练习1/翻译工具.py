import uuid
import requests
import hashlib
import time



#wenzi=input('请输入文字：')

# ====================== 请修改这里 ======================
YOUDAO_URL = "https://openapi.youdao.com/api"
APP_KEY = "you_apikey"  # 替换成你创建应用后得到的 appKey
APP_SECRET = "XfVPqY4BhMNTiTHHMgIkDklLCaNOo9bh"  # 替换成你创建应用后得到的 appSecret


# =======================================================

def encrypt(sign_str: str) -> str:
    """
    使用 SHA-256 算法生成签名，用于 API 安全验证
    :param sign_str: 待加密的签名字符串
    :return: 加密后的十六进制签名
    """
    hash_alg = hashlib.sha256()
    hash_alg.update(sign_str.encode("utf-8"))
    return hash_alg.hexdigest()


def truncate(q: str) -> str:
    """
    对长文本进行截断，避免参与签名的文本过长
    :param q: 待翻译的文本
    :return: 截断后的文本（≤20字符）
    """
    if q is None:
        return ""
    size = len(q)
    return q if size <= 20 else q[:10] + str(size) + q[-10:]


def do_request(data: dict) -> requests.Response:
    """
    向有道翻译 API 发送 POST 请求
    :param data: 请求参数字典
    :return: 服务器响应对象
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(text: str, from_lang: str = "auto", to_lang: str = "zh-CHS") -> dict:
    """
    调用有道翻译 API 执行翻译
    :param text: 要翻译的文本
    :param from_lang: 源语言（默认 auto 自动检测）
    :param to_lang: 目标语言（默认 en 英文）
    :return: 翻译结果字典
    """
    data = {}
    data["q"] = text
    data["from"] = from_lang
    data["to"] = to_lang
    data["appKey"] = APP_KEY
    data["signType"] = "v3"
    data["curtime"] = str(int(time.time()))
    data["salt"] = str(uuid.uuid1())

    # 拼接签名字符串并加密
    sign_str = APP_KEY + truncate(text) + data["salt"] + data["curtime"] + APP_SECRET
    data["sign"] = encrypt(sign_str)

    # 发送请求并解析结果
    response = do_request(data)
    response.raise_for_status()  # 自动抛出 HTTP 错误
    return response.json()


if __name__ == "__main__":
    # 示例：翻译 "你好，世界" 从中文到英文
    result = translate("wenzi", from_lang="en", to_lang="zh-CHS")
    print("翻译结果：", result)

    # 提取翻译后的文本（如果请求成功）
    if result.get("errorCode") == "0":
        print("翻译后的文本：", result["translation"][0])
    else:
        print("翻译失败，错误码：", result.get("errorCode"))

import webview
import json


class JSBridge:


    def post_message(self, message):
        # 这里会收到从 JS 传过来的消息
        print("Received message from JS:", message)

    def send_data(self, data):
        # 发送数据给 JS
        print("Sending data to JS:", data)


def start_webview():
    # 创建 Python 端的 JSBridge 实例
    bridge = JSBridge()

    with open('captcha.html','r',encoding="UTF-8") as f:
        ht=f.read()
    # 创建 webview 窗口，并通过 js_api 参数暴露 bridge 对象给 JavaScript
    webview.create_window('Tencent Captcha',
                          html=ht,
                          js_api=bridge)

    # 启动 webview
    webview.start()


if __name__ == "__main__":
    start_webview()

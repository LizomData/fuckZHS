import webview


class JSBridge:


    def post_message(self, message):
        # 这里会收到从 JS 传过来的消息
        print("Received message from JS:", message)

    def send_data(self, data):
        # 发送数据给 JS
        print("Sending data to JS:", data)
def evaluate_js(window):
    result = window.evaluate_js(
        r"""
         var captchaIns;
    initNECaptcha({
      element: '#captcha',
      captchaId: '4da3050565514a35a50541b0e1f54538',
      mode: 'popup',
      width: '320px',
      closeEnable: true,
      apiVersion: 2,
      popupStyles: {
        position: 'fixed',
        top: '20%'
      },
      onClose: function () {
        // 弹出关闭结束后将会触发该函数
      },
      onVerify: function (err, data) {
        if (!err) {
          // 验证成功后，调用 close 方法关闭弹框
          captchaIns.close()
          // TODO: 验证成功后继续进行业务逻辑
          console.log(data)
          pywebview.api.post_message(data)
        }
      }
    }, function (instance) {
      // 初始化成功后得到验证实例 instance，可以调用实例的方法
      captchaIns = instance
      captchaIns.verify()
    }, function (err) {
      // 初始化失败后触发该函数，err 对象描述当前错误信息
    })
        """
    )

    print(result)

def start_webview():

    window=webview.create_window('Captcha',
                          'captcha.html'
                          )
    webview.start(evaluate_js,window,private_mode=False)


if __name__ == "__main__":
    start_webview()

import time

import requests
import webview
import json
from http.cookies import SimpleCookie


class JSBridge:

    def post_message(self, message):
        print("Received message from JS:", message)


    def send_data(self, data):
        # 发送数据给 JS
        print("Sending data to JS:", data)

class myWebView:
    def __init__(self):
        self.curWin=None



    def close_curWin(self):
        if self.curWin is not None:
            self.curWin.destroy()

    def display_image(self,img_base64):
        img_base64 =img_base64

        html_content = f"""
               <!DOCTYPE html>
               <html lang="en">
               <head>
                   <meta charset="UTF-8">
                   <meta name="viewport" content="width=device-width, initial-scale=1.0">
                   <title>Image Display</title>
               </head>
               <style>
               </style>
               <body>
                   <div style="display: flex;width: 600px; flex-direction: column;align-items: center; ">
                       <div>打开知到APP扫一扫登录</div>
                       <img style=" width: 70%; height: auto;" src="data:image/png;base64,{img_base64}" alt="Sample Image">
                   </div>
               </body>
               </html>
               """

        self.curWin=webview.create_window("Image Viewer", html=html_content, width=600, height=600)
        webview.start()



    def read_cookies(self,window):
        cookie_list = []
        isLogin = False


        while(True):
            cookies = window.get_cookies()
            for cookie in cookies:
                for key, morsel  in cookie.items():
                    cookie_dict = {}

                    cookie_dict['name']=morsel.key
                    cookie_dict['value']=morsel.value
                    if morsel.key =='jt-cas':
                        isLogin=True
                    for k,v in morsel.items():
                        cookie_dict[k]=v


                    cookie_list.append(cookie_dict)

            if isLogin :
                cookie_json = json.dumps(cookie_list, indent=4)
                print(cookie_json)
                self.cookie_jar = requests.cookies.RequestsCookieJar()
                for cookie_dict in cookie_list :
                    self.cookie_jar.set(
                        cookie_dict['name'],
                        cookie_dict['value'],
                        domain=cookie_dict['domain'],
                        path=cookie_dict['path'],
                        secure=cookie_dict['secure'],
                        rest={'HttpOnly': cookie_dict['httponly'], 'SameSite': cookie_dict['samesite']}
                    )
                break





            # print('\n-----------------------------------------------------------')
            #
            # for c in cookies:
            #     print(c.output())
            # print('-----------------------------------------------------------')

            time.sleep(2)
        self.close_curWin()

    def display_html_url(self,url):
        self.curWin=webview.create_window("Web Viewer", url=url)
        webview.start(self.read_cookies , self.curWin ,  private_mode=False)



if __name__ == "__main__":

    web_view=myWebView()
    web_view.display_html_url('https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin')

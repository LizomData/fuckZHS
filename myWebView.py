import base64
import re
import time
import requests
import webview
import json



class myWebView:


    def close_curWin(self):
        for win in webview.windows:
            win.destroy()


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

        webview.create_window("Image Viewer", html=html_content, width=600, height=600)
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
        windwow = webview.create_window("Web Viewer", url=url)
        webview.start(self.read_cookies , windwow ,  private_mode=False)


    def verify_captcha(self,imgUrl, extra):
        b = base64.b64encode(requests.get(url=imgUrl, verify=False).content).decode()  ## 图片二进制流base64字符串

        with open('YmServerConfig.json','r',encoding='UTF-8') as f:
            config=json.loads(f.read())

        url = "http://api.jfbym.com/api/YmServer/customApi"
        data = {
            ## 关于参数,一般来说有3个;不同类型id可能有不同的参数个数和参数名,找客服获取
            "token": f"{config['token']}",
            "type": "30109",
            "image": b,
            'extra': extra,
        }
        _headers = {
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, headers=_headers, json=data, verify=False)
        response_json = json.loads(response.text)
        match(response_json['code']):
            case "10000":
                pos = re.split(',', response_json['data']['data'])
                # print(response.text)
                return {'x': pos[0], 'y': pos[1]}
            case "10007":   #图片未识别成功
                return {'x': 50, 'y': 50}




    def post_captcha_validate(self, validate):
        # print("Received validate from JS:", validate)
        self.validate= validate
        self.close_curWin()
    def display_video_captcha(self):
        webview.create_window('Captcha',  url='captcha.html',js_api=self)
        webview.start()


if __name__ == "__main__":

    web_view=myWebView()
    web_view.display_video_captcha()
    # web_view.display_html_url('https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin')

import requests
import time
import ssl
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'fangling@outlook.com'
email_addr = '2449891969@qq.com'



def mail():
    ret = True
    import traceback
    try:
        msg = MIMEText(
            "你要购买的CARRYALL 小号手袋有货了\n 购买地址: https://www.louisvuitton.cn/zhs-cn/products/carryall-pm-monogram-nvprod3770016v/M46203",
            "plain", 'utf-8')
        msg["From"] = formataddr(("LV通知", my_sender))
        msg["To"] = formataddr(("蕾蕾姐", email_addr))
        msg["Subject"] = "到货通知"

        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls(context=context)
            server.login(my_sender, "11111111")
            server.sendmail(my_sender, [email_addr, ], msg.as_string())
    except Exception as e:
        print(e)
        traceback.print_exc()
        ret = False

    return ret


def do_it():
    url = "https://api-cn.louisvuitton.cn/api/zhs-cn/catalog/availability/nvprod3770016v"

    payload = {}
    headers = {
        'authority': 'api-cn.louisvuitton.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'AKA_A2=A; bm_sz=F272E23BA182BBAED55FB4D973DC6E0B~YAAQeBTSPBDvfPOEAQAAqY09nxL6skY33hGWO5XhqKzHp6ea5QmFrbUo3upeDDVv+YGnJEHnkGvBPwMTg2vQ8mHHnFzVaUORInM3QsXSg3ybLn0BrgXkwq24gJSZyR6+S9FzK3F9dKbWxPDuRjRdDosHPwnTXpgmUR3U9LDwWm3KuSIv8bzcEJGUh1Y0ud4I5i1yEEqfvK64VggYk0yLkXf+lpiV29GNOSP0xLAkXFcSnOZn8EDp8LEygo4h4dA3emQBKBCx6ePH0Bjw4BetmxbLCxJyyhVuVebTfldOVKB23Qwaza6GOQ==~4469827~4337721; PIM-SESSION-ID=tpJZLB5EbBtGhEx2; lv-dispatch=zhs-cn; ak_cc=CN; ak_bmsc=94430685573C5189CC125E4E731A0661~000000000000000000000000000000~YAAQeBTSPCzvfPOEAQAAYZQ9nxLgFdpuvJtKXKKZnLbY7nHUP96IEvW0WGk7foPkucIGw7Bu5cK66YY8d0h4DA+J/2uLzEM9wyZEkzBWnijyQuLnDv8kQTcU64soxClgh1W8A0HwzfdHZufIn28b5WtcXjVysqtobx4XGJLI5bzV5NI/SE4SKtMDFoLE44KqqLSTnMyWVjH08bfGSlIOohS1Zyr52uoGPqtyTgauuOR+vWoaESPObMFuMmkNm2Epb9L+n/Cy/qFKThckFiZ3/bUzh1NSjLdazbit+j76/ZCMqSJ0u5ysxaNdk/0FiX1972sczb0zioWMJl2KEo1r4wRWEXxkmR4o+fvU1LpFnzpQY8vUz0Jm9mN+FXQwKwnnu9iOPanqz+UP5fSntEk9h0QPlchz+HTDlEIUF6LBZD7liR1XDmMQtLaety75unU8HAKJArAMwwdofEYskZQI40LUGkn/PT2kiNadVjcTKX3guKUPfZfXzFfMViVF; gtm_cookie_consent=functional:1|analytics:1|customization:1|advertising:1; _cs_mk=0.4034746170413135_1673413898197; Qs_lvt_187854=1673413898; _gid=GA1.2.374819165.1673413898; _qubitTracker=b4nys6d6ccg-0lcr7ffsm-yh5bq1c; qb_generic=:YWfPbC0:.louisvuitton.cn; _gcl_au=1.1.1919913003.1673413899; _cs_c=1; ATGID=anonymous; SGID=sb.springboot51-p1c; SGID=.springboot51-p1c; lv-dispatch-url=https://www.louisvuitton.cn/zhs-cn/products/precious-rabbit-reykjavik-scarf-s00-nvprod3980133v/M78165; Qs_pv_187854=3294152883428238000%2C2540140543543818000; _ga=GA1.1.1287461827.1673413898; _dynSessConf=9006676419548752213; JSESSIONID=g7cQk0O73dwTY4kWFNEn5tXM.front51-p1c; ATG_SESSION_ID=mOz1fmSNm5LklXRc5-flvRqn.front71-prd; order_CN="H4sIAAAAAAAAAKtWyi9KSS1SslLKK8s3NTIysbCwNDJTqgUAl9QaCxgAAAA="; orderSize_CN=1; anonymous_session=false; _abck=9317B37730CD68D4392EDBC0A9450112~0~YAAQDhTSPNaYcXGFAQAA2jZInwkrBkObGrCSX4OKPdbuVi41gjTyQI/X6ki6wweE0wnAkTrkD96Dt72xn8vdmpu+8nYjIY+gHZvMghRwNTuCyZP778g14fPlb1Clc0+k2GyGf2rZhEE7IWzEEQy186INZcXz332YT+bLu4qqeJpLNWt2ODUj20uQeIE4yvdYXwhkgwrr4uKIKgTynF3Yvj8wcHbQoYbM29ugNSbOnHPoaOjloqcJW0M6FPTH88peiyQzO3EI4voyXth9u7q6dcIUzQ+naK8JnQ6WRD8Rai2joEYuF5yI6xgY/qOvmK2Tj8urfhC7EN97EC4WR5Rd72I1fVKVi5/9Tw9XqW/I4WtS/m6FOOEvOhjwS2Oi66VTinmYRxROyZWfdDKmXCvUsPQCBWzIN10AwmnV/CY=~-1~-1~-1; _cs_id=a7da4c42-fe5f-a39b-ed8b-7847bad429b4.1673413898.1.1673414704.1673413898.1.1707577898699; _cs_s=22.0.0.1673416504043; qb_permanent=b4nys6d6ccg-0lcr7ffsm-yh5bq1c:22:22:1:1:0::0:1:0:BjvkUL:Bjvkgw:::::112.80.59.82:suzhou:39132:china:CN:31.31:120.61:suzhou:156078:jiangsu%20sheng:35603:migrated|1673413901942:Fv3O==L=Co1X=8::YWfSgK4:YWfPbSB:0:0:0::0:0:.louisvuitton.cn:0; qb_session=22:1:52:Fv3O=L:0:YWfPbSB:0:0:0:0:.louisvuitton.cn; bm_sv=8C8572DE553C028B6645FEA758481100~YAAQDhTSPPutcXGFAQAAToJNnxIYa1aQ1aKSyxlbE4E4N/9xgE8GzZ/UJELgqbYLkypUkCEKD8c5xZjKq6uPwN+7wRESg4W6Wkp247EQyVX5GIZOhDoJ6pWckMHa8jPz1Qe59pVwomtexo8HtnF0ip6QiOUUkayVR248JgdvB2zZt3sPHcfuChroztH1tpOMd7cWXxm83HD9OCfNSIYk/vW0nXzl8ev/DnBailQF0uNz3Iiyx6nABqlwxJYBk4/Mt6QeMv4=~1; _ga_S6ED35NYJQ=GS1.1.1673413898.1.1.1673414935.60.0.0; utag_main=v_id:01859f3d92160016c9e22c7765640506f008506700978$_sn:1$_se:77$_ss:0$_st:1673416736392$ses_id:1673413890582%3Bexp-session$_pn:23%3Bexp-session$dc_visit:1$dc_event:63%3Bexp-session$dc_region:eu-central-1%3Bexp-session; OPTOUTMULTI=0:0%7Cc1:0%7Cc2:0%7Cc4:0%7Cc3:0; _abck=9317B37730CD68D4392EDBC0A9450112~-1~YAAQDhTSPN27cXGFAQAAYXNRnwmMveYQS9KgANnc48kUB7Y0SbuLFtKwj8Soo0RZr0uzQqKMl/FWUWamVMXcNfgGqLaqCCQ9psxyJ8ZYdyItt6vE5sD6ytqBTdVnh/yLJGuXd9b9KHEQIDs0hl/71pkJ7raiNDzTJt4DLtCLuCDI7kAwLmY3O4lRPHT7LzTMwpBprkq94SGwZHU5yoSWCaCurWvppcsrt17DLyQPmfCNh98+xnW1H4hQ3sdlv24HYxHG8r1XRP9IK5f0tYt79nb9BH7j71/d6ER3y9ttfWwbQHVNHtd3Foh4VUPUIoQOjgTrMUNTiRZQLIxId18EP91arohFLchyQuwPBKDkPHDnM7Eyoyqp262bcKJALBBf4cG/yf70Rni+iHPtFSr7wLy8r0K9u0elWx6S2Lw=~0~-1~-1',
        'origin': 'https://www.louisvuitton.cn',
        'referer': 'https://www.louisvuitton.cn/zhs-cn/products/carryall-pm-monogram-nvprod3770016v/M46203',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    if data.get("skuAvailability")[0].get("inStock"):
        if mail():
            print("邮件发送成功")
    else:
        print("没货")


if __name__ == '__main__':
    for i in range(12):
        do_it()
        time.sleep(60*5)
        

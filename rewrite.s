#!name=Rewrite
#!desc= URL Rewrite AND Header Rewrite 重定向
#!MANAGED-CONFIG https://raw.githubusercontent.com/caaby/w/surge/rewrite.s


[URL Rewrite]
# Redirect Google Maps Service
^https?:\/\/(ditu|maps)\.google\.cn https://maps.google.com 302
(^https?:\/\/.+\.googlevideo\.com\/.+)(&ctier=[A-Z])(&.+) $1$3 302

# >> 此规则可以将 Wikipedia 的请求跳转至 Wikiwand 以达到 Wikipedia 排版优化的目的。重新排版后的语言将与原页面语言保持一致。
^https?:\/\/zh.(m.)?wikipedia\.org\/(zh(-\w)?) http://www.wikiwand.com/$2 302
^https?:\/\/(\w*).(m.)?wikipedia\.org\/wiki http://www.wikiwand.com/$1 302

# >> 12306
^https?+:\/\/mobile\.12306\.cn\/otsmobile\/app\/mas\/loggw\/(logUpload.do|logConfig.do) - reject

# Redirect HTTP to HTTPS
^https?:\/\/(www.)?taobao\.com\/ https://taobao.com/ 302
^https?:\/\/(www.)?jd\.com\/ https://www.jd.com/ 302
^https?:\/\/(www.)?mi\.com\/ https://www.mi.com/ 302
^https?:\/\/you\.163\.com\/ https://you.163.com/ 302
^https?:\/\/(www.)?suning\.com\/ https://suning.com/ 302
^https?:\/\/(www.)?yhd\.com\/ https://yhd.com/ 302

# Redirect False to True
# > Firefox - www.firefox.com.cn
^https?:\/\/(www.)?firefox\.com\.cn\/(download\/)?$ https://www.mozilla.org/zh-CN/firefox/new/ 302

# > Fake Website Made By C&J Marketing
^https?:\/\/(www.)?abbyychina\.com\/ https://www.abbyy.cn/ 302
^https?:\/\/(www.)?officesoftcn\.com\/ https://www.microsoft.com/zh-cn/microsoft-365 302

# AbeamTV - api.abema.io
^https?:\/\/api\.abema\.io\/v\d\/ip\/check - reject

# AICoin
^http:\/\/(www.)?aicoin\.cn\/$ https://www.aicoin.com/ 302


[Header Rewrite]
# >> 手机端使用知乎网页版
^https?:\/\/www\.zhihu\.com\/question\/ header-replace User-Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.120 Safari/537.36

# >> 百度知道
^https?:\/\/zhidao\.baidu\.com header-replace User-Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15

[MITM]
hostname = %APPEND%  www.zhihu.com, www.zhidao.com, *.google.cn, *.googlevideo.com, www.officesoftcn.com, wwww.abbyychina.com, mobile.12306.cn, *.wikipedia.org, *.googlevideo, www.firefox.com.cn, api.abema.io
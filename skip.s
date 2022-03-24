#!name=skip proxy list
#!desc=跳过部分应用的代理检测
#!system=ios
#!url=https://raw.githubusercontent.com/caaby/w/surge/skip.s

[General]
# >> 百度搜索 - www.baidu.com
# >> 建行    - ccb.*
# >> 苹果抓包 - captive.apple.com
skip-proxy = %INSERT% www.baidu.com, captive.apple.com, *.ccb-life.com.cn, ccb-life.com.cn,*.ccb.cn, ccb.cn,*.ccb.com,ccb.com,*.ccb.com.cn,ccb.com.cn,*.ccbcos.com,ccbcos.com,*.ccbfund.cn,ccbfund.cn,*.ccbfutures.com,ccbfutures.com,*.ccbhome.cn, ccbhome.cn, *.ccbhome.net,ccbhome.net,*.ccbintl.com.hk,ccbintl.com.hk,*.ccbleasing.com, ccbleasing.com,*.ccbseoul.com,ccbseoul.com,*.ccbtrust.com.cn, ccbtrust.com.cn

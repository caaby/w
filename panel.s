#!name=Panels
#!desc=自用panel收集

[Panel]
# << 节假日倒计时, 节日当天早上有提醒
# >> 节假日倒计时 = script-name=节假日倒计时, update-interval=3600

# >> 网络信息面板
网络信息面板 = script-name=网络信息面板, title="网络状态", content="请刷新", style=info, update-interval=3600


[Script]
# >> 节假日倒计时 = type=generic, timeout=10, script-path=https://raw.githubusercontent.com/TributePaulWalker/Profiles/main/JavaScript/Surge/Timecard.js
网络信息面板 = type=generic, timeout=600, script-path=https://raw.githubusercontent.com/caaby/w/surge/ip.js

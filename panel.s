#!name=Panels
#!desc=自用panel收集

[Panel]
# >> Surge Pro标题,可显示启动时间,点击刷新为重载配置
SurgePro = script-name=SurgePro_ReloadProfile,update-interval=1
# >> 节假日查询
Timecard = script-name=timecard,update-interval=3600
# >> 网络信息面板
NET_info = script-name=网络信息面板, title="网络状态", content="请刷新", style=info, update-interval=3600
# >> 机场信息
Sub_info = script-name=Sub_info,update-interval = 43200

[Script]
SurgePro = type=generic,timeout=10,script-path= https://raw.githubusercontent.com/fishingworld/something/main/PanelScripts/surgepro_reloadprofile.js ,argument=icon=crown.fill&color=#f6c970
Timecard = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/smartmimi/conf/master/surge/timecard.js
NET_info = type=generic, timeout=20, script-path=https://raw.githubusercontent.com/caaby/w/surge/ip.js
Sub_info = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/mieqq/mieqq/master/sub_info_panel.js ,script-update-interval=0,argument=url=https%3A%2F%2Fsubscribe.gacloudltd.store%2Flink%2FjeSFjhzquavecr1t&reset_day=19&title=GaCloud&icon=opticaldisc&color=#5AC8FA


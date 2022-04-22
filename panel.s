#!name=Panels
#!desc=自用panel收集

[Panel]
# >> Surge Pro标题,可显示启动时间,点击刷新为重载配置
SurgePro = script-name=SurgePro,update-interval=1
# >> 节假日查询
Timecard = script-name=Timecard,update-interval=3600
# >> 网络信息面板
NET_info = script-name=NET_info,title="网络状态",content="请刷新",style=info,update-interval=3600
# >> 机场信息
Sub_info = script-name=Sub_info,update-interval=43200
# >> 策略组面板 可重复配置 注意修改相应字段
#groupPanel= script-name=groupPanel,update-interval=5

[Script]
SurgePro = type=generic,timeout=10,script-path= https://raw.githubusercontent.com/fishingworld/something/main/PanelScripts/surgepro_reloadprofile.js ,argument=icon=crown.fill&color=#f6c970
Timecard = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/smartmimi/conf/master/surge/timecard.js
NET_info = type=generic, timeout=20, script-path=https://raw.githubusercontent.com/caaby/w/surge/ip.js
Sub_info = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/mieqq/mieqq/master/sub_info_panel.js ,script-update-interval=0,argument=url=https%3A%2F%2Fsubscribe.gacloudltd.store%2Flink%2FjeSFjhzquavecr1t&reset_day=19&title=GaCloud&icon=opticaldisc&color=#5AC8FA
#策略组面板 可重复配置 注意修改相应字段
#必须更改的字段：group 填写需要显示的策略组名称
#groupPanel = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/fishingworld/something/main/groupPanel.js ,argument=icon=network&color=#86abee&group=proxy

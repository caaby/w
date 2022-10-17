#!name=Panels
#!desc=自用panel收集

[Panel]
# 网络信息面板
net-info-panel=title="网络状态",content="请刷新",style=info,script-name=net-info-panel
# >> 流量统计 点击以切换网络界面
TrafficStatistics = script-name=TrafficStatistics,update-interval=1
# >> Surge Pro标题,可显示启动时间,点击刷新为重载配置
# SurgePro = script-name=SurgePro,update-interval=1
# >> 节假日查询
Timecard = script-name=Timecard,update-interval=3600
# >> 策略组面板 可重复配置 注意修改相应字段
#groupPanel= script-name=groupPanel,update-interval=5

[Script]
Timecard = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/smartmimi/conf/master/surge/timecard.js,argument=color=#4169E1
net-info-panel=type=generic,timeout=10,script-path=https://raw.githubusercontent.com/Peng-YM/QuanX/master/Tools/Panels/NetInfo/net-info-panel.js,argument=color=#4169E1
TrafficStatistics = type=generic,timeout=10,script-path= https://raw.githubusercontent.com/fishingworld/something/main/PanelScripts/trafficstatistics.js ,argument=icon=arrow.up.arrow.down.circle&color=#4169E1

# SurgePro = type=generic,timeout=10,script-path= https://raw.githubusercontent.com/fishingworld/something/main/PanelScripts/surgepro_reloadprofile.js,argument=icon=crown.fill&color=#4169E1
#策略组面板 可重复配置 注意修改相应字段
#必须更改的字段：group 填写需要显示的策略组名称
#groupPanel = type=generic,timeout=10,script-path=https://raw.githubusercontent.com/fishingworld/something/main/groupPanel.js ,argument=icon=network&color=#86abee&group=proxy

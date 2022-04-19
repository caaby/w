#!name=surge official module
#!desc=官方内置模块
#!system=ios

# > 阻止所有UDP流量到端口443，使HTTP3请求退回到TCP流量
[Rule]
AND,((PROTOCOL,UDP), (DEST-PORT,443)),REJECT-NO-DROP

# > 通过访问浏览器 http://route.com 来访问路由器配置网页，URL将始终重定向到当前网络中的网关地址
[General]
force-http-engine-hosts=%APPEND% route.com, www.route.com

[URL Rewrite]
^https?://(|www\.)route\.com http://{{{GATEWAY_ADDRESS}}} 302

[MITM]
hostname = %INSERT% route.com, www.route.com
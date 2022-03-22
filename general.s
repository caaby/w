#! name=General
#! desc=通用配置 包含General，Replica，MitM
#! MANAGED-CONFIG https://raw.githubusercontent.com/caaby/w/surge/general.s

[General]
# >> HTTP API 配置
http-api = Fang@0.0.0.0:2222

# >> HTTP-API TLS设置
# >> http-api-tls = true

# >> HTTP API 网页控制台启用
http-api-web-dashboard = true

# >> 日志等级 warning, notify, info, verbose (默认值: notify)
loglevel = warning

# >> TLS Provider: default, secure-transport, network-framework, openssl (默认值: default)
tls-provider = openssl

# >> 隐藏 VPN 图标
hide-vpn-icon = true

# >> 当开启时，如果在 [Host] 段有为某主机名指定 IP，在使用代理访问该主机名时，将使用该 IP 地址进行代理请求，不再依赖远端解析。
use-local-host-item-for-proxy = true

# >> UDP IP 防泄漏
# >> 如果没有代理服务器支持 UDP 转发，可修改为「 direct 」或注释下条，但需注意同一目标主机名 TCP 请求与 UDP 请求的源地址不同所造成的隐私及安全风险。
# >> udp-policy-not-supported-behaviour = reject

# >> IPv6 支持（默认关闭
ipv6 = false

# >> Wi-Fi Assist 开启时，支持使用数据网络进行后备 DNS 查询
wifi-assist = true

# >> 允许 Wi-Fi 网络下其它设备访问
allow-wifi-access = true

# >> 允许热点共享
allow-hostspot-access = true

# >> iOS 端 HTTP 代理服务端口（默认为"6152"）
wifi-access-http-port = 7000

# >> iOS 端 SOCKS5 代理服务端口（默认为"6153"）
wifi-access-socks5-port = 7001

# >> MacOS 端 HTTP 代理服务端口（默认为"6152"）
http-listen = 0.0.0.0:7002

# >> MacOS 端 SOCKS5 代理服务端口（默认为"6153"）
socks5-listen = 0.0.0.0:7003

# >> 从 /etc/hosts 读取 DNS 记录
read-etc-hosts = true

# >> 启用 Network.framework
# >> 启动 Network.framework 以开启用户态网络协议栈，可提高吞吐量，降低延迟并开启 MPTCP。（需手动重启 Surge) 实验性功能可能导致 Surge 不稳定，甚至引起系统崩溃。
# >> 默认开启：true ，可根据自己的需求选择关闭：false 。
network-framework = false

# >> 排除简单主机名
exclude-simple-hostnames = true

# >> 外部控制器
# >> external-controller-access = Fang@0.0.0.0:5555

# >> 兼容模式（默认为"0/禁用"）
compatibility-mode = 0

# >> 错误警告显示页
show-error-page-for-reject = true

# >> 测速超时（秒）
test-timeout = 3

# >> 网络测试 URL
internet-test-url = http://wifi.vivo.com.cn/generate_204
internet-test-url = http://captive.apple.com

# >> 代理测速 URL
proxy-test-url = http://www.gstatic.com/generate_204

# >> Hijack DNS
hijack-dns = 8.8.8.8:53, 8.8.4.4:53

# >> 公共Wi-Fi下的默认策略启用
use-default-policy-if-wifi-not-primary = true


# >> Always Real IP Hosts
always-real-ip = *.msftconnecttest.com, *.msftncsi.com, *.srv.nintendo.net, *.stun.playstation.net, xbox.*.microsoft.com, *.xboxlive.com, *.logon.battlenet.com.cn, *.logon.battle.net, stun.l.google.com

# >> 跳过代理
skip-proxy = localhost, *.local, 0.0.0.0/8, 10.0.0.0/8, 17.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.168.0.0/16, 192.88.99.0/24, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 240.0.0.0/4, 255.255.255.255/32

# >> 强制http引擎主机
force-http-engine-hosts = 123.59.31.1, 119.18.193.135, 122.14.246.33, 175.102.178.52, 192.30.*, 143.55.*, 140.82.*

# >> 默认情况下，Surge VIF 接口会声明自己是默认路由。但是，由于 Wi-Fi 接口的路由较小，有些流量可能不会通过 Surge VIF 接口。使用此选项可以添加一条较小的路由。
tun-included-routes = 192.168.2.12/32

# >> Surge VIF 只能处理 TCP 和 UDP 协议。使用此选项可以绕过特定的 IP 范围，允许所有流量通过。
tun-excluded-routes = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12

# >> 路由防火墙
# > 包含所有的网络请求
include-all-networks = false

# > 包含本地网络请求
include-local-networks = false

# > 代理请求本地DNS映射
use-local-host-item-for-proxy = false

[Replica]
# >> 抓取流量 => 过滤器
# >> 隐藏 Apple 请求
hide-apple-request = false

# >> 隐藏 Crash Reporter 请求
hide-crash-reporter-request = true

# >> 隐藏 UDP 会话
hide-udp = false

# >> 关键词过滤器
keyword-filter-type = none
keyword-filter = icloud, ocsp, logs, analytic

#### 个人使用
1. 订阅文件  
    https://raw.githubusercontent.com/caaby/w/surge/c.conf
2. 国内以及广告规则  
    https://raw.githubusercontent.com/caaby/w/surge/china_rule.s
3. host  
    https://raw.githubusercontent.com/caaby/w/surge/host.s
4. 通用配置  
    https://raw.githubusercontent.com/caaby/w/surge/general.s
5. 重定向URL  
    https://raw.githubusercontent.com/caaby/w/surge/rewrite.s
6. 腾讯 doh-query  
    https://raw.githubusercontent.com/caaby/w/surge/tencent_doh.s
7. DNS 解析服务  
   https://raw.githubusercontent.com/caaby/w/surge/dns.s
8. break wifi  
    https://raw.githubusercontent.com/caaby/w/surge/break.s

### 模块
#### Detached Profile Section 功能用于将单个配置文件拆分为多个文件，而模块是配置文件的补丁，每个模块文件用于调整配置文件的各个部分以实现特定任务。

模块可以是：

灵活开启和关闭。
调整同一文件中的多个段。
通过 URL 安装并保持最新。
然而

模块无法调整【代理】、【代理组】、【规则】部分的内容。
模块无法调整 MITM 的 CA 证书。
模块的设置会覆盖主配置文件，因此无法通过 UI 进行调整。
模块描述位于：https ://manual.nssurge.com/others/module.html
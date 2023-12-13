#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
backup_source(){
if [ -f "/usr/bin/yum" ];then
    \cp -rp /etc/yum.repos.d/ /etc/yum.repos.ftpd_backup
elif
    [ -f "/usr/bin/apt" ]; then
    \cp -rp /etc/apt/sources.list /etc/apt/sources.list_backup
fi
}
_info(){
    sleep 1
    echo -e "\n\e[1;31m#####安装源已经设置完成，请重新安装软件#####\e[0m\n"
}
while :
    do
        echo "==================================================================="
        echo -e "\n请根据下面的指示选择对应的yum|apt安装源"
        echo "==================================================================="
        echo "1) 阿里云服务器CentOS7     2) 腾讯云服务CentOS7"
        echo "3)清华源Ubuntu18.04 LTS   4) 清华源Ubuntu20.04 LTS"
        echo "5)清华源Ubuntu21.04    6) 清华源Debian bullseye发行版"
        echo "7)退出                  8) ========================="
        echo "==================================================================="
        echo "由于CentOS8 CentOS官方已经停止维护，不再提供安装源"
        echo "设置安装源后还是无法安装软件的，请联系服务器运营商解决"
        read -p "请输入对应数字尝试自动修复[1-8]:" input
        case ${input} in
        [1]*)
        #阿里云CentOS7安装源
            backup_source
            curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
            yum clean all
            yum makecache
            _info
            break
            ;;
        [2]*)
        #腾讯云CentOS7安装源
            backup_source
            curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo
            yum clean all
            yum makecache
            _info
            break
            ;;

        [3]*)
        #清华源Ubuntu18
            backup_source
            #\cp -rp   /etc/apt/sources.list /etc/apt/sources.list_back
            echo "" >/etc/apt/sources.list
            cat >/etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
EOF
            apt-get update -y 
            break
            ;;
             

        [4]*)
        #清华源Ubuntu20
            backup_source
            echo "" >/etc/apt/sources.list
            cat > /etc/apt/sources.list<<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
EOF
            apt-get update -y
            break
            ;;  
              
        [5]*)
        #清华源Ubuntu21
            backup_source
            echo "" >/etc/apt/sources.list
            cat >/etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ hirsute-security main restricted universe multiverse
EOF
            apt-get update -y 
            break
            ;;  
                                                                
        
        [6]*)
        #清华源Ubuntu21
            backup_source
            echo "" >/etc/apt/sources.list
            cat >/etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
EOF
            apt-get update -y 
            break
            ;;  
        [7]*)
            break
            ;;
        *)                                                              
        
            echo -e "\n\e[1;31m输入有误,请重新选择正确的选项!\e[0m\n"
            ;;
        esac
    done

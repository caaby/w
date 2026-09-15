#!/bin/sh
set -eu

file="./target/linux/ramips/dts/mt7621_tplink_archer-ax23-v1.dts"

if [ ! -f "$file" ] || [ ! -r "$file" ]; then
    printf '文件不存在或不可读：%s\n' "$file" >&2
    exit 1
fi

# 所有数量检查通过后才修改文件。
check_count() {
    text="$1"
    expected="$2"
    actual=$(grep -oF "$text" "$file" | wc -l)

    if [ "$actual" -ne "$expected" ]; then
        printf '%s：预期 %s 处，实际 %s 处；未修改文件。\n' \
            "$text" "$expected" "$actual" >&2
        exit 1
    fi
}

if ! grep -qF 'ethphy4' "$file" && ! grep -qF 'port@0' "$file"; then
    # 允许再次运行，以便继续处理 safeloader。
    check_count "ethphy0" 2
    check_count "port@1" 1
    check_count "port@2" 1
    check_count "port@3" 1
    check_count "port@4" 1
    printf 'DTS 已修改，跳过：%s\n' "$file"
else
    check_count "ethphy4" 2
    check_count "port@0" 1
    check_count "port@1" 1
    check_count "port@2" 1
    check_count "port@3" 1

    # 端口从大到小替换，避免新名称再次被替换。
    sed -i '
        s/ethphy4/ethphy0/g
        s/port@3/port@4/g
        s/port@2/port@3/g
        s/port@1/port@2/g
        s/port@0/port@1/g
    ' "$file"

    printf '修改完成：%s\n' "$file"
fi

# 从当前工作目录查找固件工具源码。
host_dir="build_dir/host"
old_entry='{product_name:Archer AX23,product_ver:1.0,special_id:52550000}'
new_entry='{product_name:Archer AX23V,product_ver:1.0,special_id:4A500000}'

if [ ! -d "$host_dir" ]; then
    printf 'DTS 已修改，但找不到 %s；请在固件项目根目录运行脚本。\n' "$host_dir" >&2
    exit 1
fi

sources=$(find "$host_dir" -type f -path '*/src/tplink-safeloader.c' -print)
if [ -z "$sources" ]; then
    printf 'DTS 已修改，但未找到 tplink-safeloader.c。\n' >&2
    exit 1
fi

printf '%s\n' "$sources" | while IFS= read -r source; do
    if grep -qF "$new_entry" "$source"; then
        printf 'AX23V 条目已存在，跳过：%s\n' "$source"
    else
        count=$(grep -oF "$old_entry" "$source" | wc -l)
        if [ "$count" -ne 1 ]; then
            printf '原 AX23 条目应有 1 处，实际 %s 处；未修改：%s\n' \
                "$count" "$source" >&2
            exit 1
        fi

        # 保留原行缩进，并在它下面添加 AX23V 条目。
        sed -i '
            /{product_name:Archer AX23,product_ver:1\.0,special_id:52550000}/ {
                p
                s/Archer AX23,/Archer AX23V,/
                s/special_id:52550000/special_id:4A500000/
            }
        ' "$source"

        printf '已添加 AX23V 条目：%s\n' "$source"
    fi

    old_ax1800='{product_name:Archer AX1800,product_ver:1.20,special_id:45550000}'
    new_ax1800='{product_name:Archer AX1800,product_ver:2.0,special_id:4A500000}'

    if grep -qF "$new_ax1800" "$source"; then
        printf 'AX1800 2.0 条目已存在，跳过：%s\n' "$source"
    else
        count=$(grep -oF "$old_ax1800" "$source" | wc -l)
        if [ "$count" -ne 1 ]; then
            printf '原 AX1800 1.20 条目应有 1 处，实际 %s 处；未添加 AX1800 2.0：%s\n' \
                "$count" "$source" >&2
            exit 1
        fi

        # 保留原行，在下面添加 AX1800 2.0 条目。
        sed -i '
            /{product_name:Archer AX1800,product_ver:1\.20,special_id:45550000}/ {
                p
                s/product_ver:1\.20,special_id:45550000/product_ver:2.0,special_id:4A500000/
            }
        ' "$source"

        printf '已添加 AX1800 2.0 条目：%s\n' "$source"
    fi

    grep -n -A5 -B5 -e 'product_name:Archer AX23' -e 'product_name:Archer AX1800' "$source"
done

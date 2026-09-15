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
    # 已经处理过 DTS，跳过。
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

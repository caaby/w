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


# ============================================================
# 修改 tplink-safeloader.c
# ============================================================

host_dir="build_dir/host"

if [ ! -d "$host_dir" ]; then
    printf '找不到 %s；请在固件项目根目录运行脚本。\n' "$host_dir" >&2
    exit 1
fi

sources=$(find "$host_dir" \
    -type f \
    -path '*/src/tplink-safeloader.c' \
    -print)

if [ -z "$sources" ]; then
    printf '未找到 tplink-safeloader.c。\n' >&2
    exit 1
fi


AX23V_ENTRY='{product_name:Archer AX23V,product_ver:1.0,special_id:4A500000}'
AX23_ENTRY='{product_name:Archer AX23,product_ver:1.0,special_id:52550000}'

AX1800_OLD='{product_name:Archer AX1800,product_ver:1.20,special_id:45550000}'
AX1800_NEW='{product_name:Archer AX1800,product_ver:2.0,special_id:4A500000}'


printf '%s\n' "$sources" | while IFS= read -r source; do

    printf '\n======================================\n'
    printf 'Safeloader: %s\n' "$source"
    printf '======================================\n'


    # --------------------------------------------------------
    # AX23V
    # --------------------------------------------------------

    if grep -qF "$AX23V_ENTRY" "$source"; then

        printf 'AX23V 条目已存在，跳过添加。\n'

    else

        count=$(grep -oF "$AX23_ENTRY" "$source" | wc -l)

        if [ "$count" -ne 1 ]; then
            printf 'AX23 原始条目应有 1 处，实际 %s 处。\n' \
                "$count" >&2
            printf '未修改 AX23V：%s\n' "$source" >&2
            exit 1
        fi

        # 在 AX23 原条目下面插入 AX23V。
        #
        # 注意：
        # p = 保留原来的 AX23 行
        # a = 在原行后面追加 AX23V 行
        #
        # 不再修改原 AX23 条目。

        sed -i \
            "/{product_name:Archer AX23,product_ver:1\\.0,special_id:52550000}/a\\
			\"$AX23V_ENTRY\\\\n\"" \
            "$source"

        printf '已添加 AX23V 条目。\n'
    fi


    # --------------------------------------------------------
    # 验证 AX23V 源码
    # --------------------------------------------------------

    if grep -qF "$AX23V_ENTRY" "$source"; then
        printf 'OK: 源码中已找到 AX23V 条目。\n'
    else
        printf 'ERROR: 源码中没有 AX23V 条目！\n' >&2
        exit 1
    fi


    # --------------------------------------------------------
    # AX1800 2.0
    # --------------------------------------------------------

    if grep -qF "$AX1800_NEW" "$source"; then

        printf 'AX1800 2.0 条目已存在，跳过。\n'

    else

        count=$(grep -oF "$AX1800_OLD" "$source" | wc -l)

        if [ "$count" -ne 1 ]; then
            printf '原 AX1800 1.20 条目应有 1 处，实际 %s 处。\n' \
                "$count" >&2
            printf '未添加 AX1800 2.0：%s\n' "$source" >&2
            exit 1
        fi

        sed -i \
            "/{product_name:Archer AX1800,product_ver:1\\.20,special_id:45550000}/a\\
			\"$AX1800_NEW\\\\n\"" \
            "$source"

        printf '已添加 AX1800 2.0 条目。\n'
    fi


    # --------------------------------------------------------
    # 验证 AX1800
    # --------------------------------------------------------

    if grep -qF "$AX1800_NEW" "$source"; then
        printf 'OK: 源码中已找到 AX1800 2.0 条目。\n'
    else
        printf 'ERROR: 源码中没有 AX1800 2.0 条目！\n' >&2
        exit 1
    fi


    # --------------------------------------------------------
    # 最终显示
    # --------------------------------------------------------

    printf '\n--- AX23 / AX23V / AX1800 entries ---\n'

    grep -n \
        -A2 \
        -B2 \
        -e 'product_name:Archer AX23' \
        -e 'product_name:Archer AX1800' \
        "$source"

done

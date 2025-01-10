#!/bin/bash

# 源目录
SOURCE_DIR="/www/backup/database"

# 目标目录
TARGET_DIR="/mnt/backup/quark/desktop/database"

# 删除旧文件的天数（可以根据需求修改，默认30）
DAYS_TO_KEEP=30

# 日志文件
#LOG_FILE="/var/log/backup_and_move.log"

# 压缩包文件名（带时间戳）
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
ARCHIVE_NAME="database_backup_$TIMESTAMP.tar.gz"

# 确保目标目录存在
mkdir -p "$TARGET_DIR"

# 压缩文件
if tar -czf "/tmp/$ARCHIVE_NAME" -C "$SOURCE_DIR" .; then
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Files compressed successfully into /tmp/$ARCHIVE_NAME" >> "$LOG_FILE"
     echo "$(date +'%Y-%m-%d %H:%M:%S') - Files compressed successfully into /tmp/$ARCHIVE_NAME"
else
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to compress files from $SOURCE_DIR"
     echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to compress files from $SOURCE_DIR"
    exit 1
fi

# 移动压缩包
if mv "/tmp/$ARCHIVE_NAME" "$TARGET_DIR"/; then
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Archive moved successfully to $TARGET_DIR/$ARCHIVE_NAME" >> "$LOG_FILE"
     echo "$(date +'%Y-%m-%d %H:%M:%S') - Archive moved successfully to $TARGET_DIR/$ARCHIVE_NAME"
else
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to move archive to $TARGET_DIR" >> "$LOG_FILE"
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to move archive to $TARGET_DIR"
    exit 1
fi

# 删除目标目录中 DAYS_TO_KEEP 天之前的压缩包
find "$TARGET_DIR" -type f -name "*.tar.gz" -mtime +$DAYS_TO_KEEP -exec rm -f {} \;
if [ $? -eq 0 ]; then
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Deleted archives older than $DAYS_TO_KEEP days from $TARGET_DIR" >> "$LOG_FILE"
     echo "$(date +'%Y-%m-%d %H:%M:%S') - Deleted archives older than $DAYS_TO_KEEP days from $TARGET_DIR"
else
#    echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to delete old archives from $TARGET_DIR" >> "$LOG_FILE"
     echo "$(date +'%Y-%m-%d %H:%M:%S') - Failed to delete old archives from $TARGET_DIR"
    exit 1
fi

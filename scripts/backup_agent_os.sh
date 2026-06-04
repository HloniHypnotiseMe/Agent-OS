#!/bin/bash
# Agent-OS Backup Script (inspired by C6Group.AiOS real deployment)
# Run daily via cron or Task Scheduler.

BACKUP_DIR="$HOME/agent-os-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "Backing up Agent-OS at $TIMESTAMP..."

# Core files
cp -r /home/user/agent-os/memory* "$BACKUP_DIR/memory_$TIMESTAMP" 2>/dev/null || true
cp -r /home/user/agent-os/projects "$BACKUP_DIR/projects_$TIMESTAMP" 2>/dev/null || true
cp /home/user/agent-os/*.json "$BACKUP_DIR/" 2>/dev/null || true
cp /home/user/agent-os/*.yaml "$BACKUP_DIR/" 2>/dev/null || true

# Logs and state
cp -r /home/user/agent-os/logs "$BACKUP_DIR/logs_$TIMESTAMP" 2>/dev/null || true

# Keep only last 7 backups
find "$BACKUP_DIR" -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true

echo "Backup complete: $BACKUP_DIR"
ls -lh "$BACKUP_DIR" | tail -5
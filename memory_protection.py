#!/usr/bin/env python3
"""
贾维斯模式 - 记忆保护与自动备份系统
功能：防止记忆丢失，自动增量备份，永远保存所有历史
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from shutil import copy2, rmtree

class MemoryProtection:
    def __init__(self):
        self.base_path = Path("/Users/dave/clawd")
        self.memory_path = self.base_path / "memory"
        self.backup_path = self.base_path / "backup"
        self.backup_path.mkdir(exist_ok=True)
        
    def create_checksum(self, file_path):
        """创建文件校验和"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def verify_integrity(self, file_path):
        """验证文件完整性"""
        if not file_path.exists():
            return False
        # 简单检查文件可读
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return True
        except:
            return False
    
    def auto_backup(self, file_path):
        """自动增量备份"""
        if not file_path.exists():
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = file_path.name
        backup_file = self.backup_path / f"{timestamp}_{filename}"
        
        # 创建备份
        copy2(file_path, backup_file)
        
        # 记录备份日志
        log_file = self.backup_path / "backup_log.json"
        log = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                log = json.load(f)
        
        log.append({
            "timestamp": datetime.now().isoformat(),
            "file": str(file_path),
            "backup": str(backup_file),
            "checksum": self.create_checksum(file_path)
        })
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        
        return backup_file
    
    def prevent_reset(self):
        """防止重置的机制"""
        # 创建保护标记
        protection_file = self.memory_path / ".protection_enabled"
        protection_file.write_text(datetime.now().isoformat())
        
        # 记录所有重要文件
        manifest = {
            "created": datetime.now().isoformat(),
            "files": [],
            "version": "1.0.0"
        }
        
        for md_file in self.memory_path.glob("*.md"):
            manifest["files"].append({
                "name": md_file.name,
                "size": md_file.stat().st_size,
                "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                "checksum": self.create_checksum(md_file)
            })
        
        manifest_file = self.memory_path / ".memory_manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return manifest
    
    def check_manifest(self):
        """检查记忆清单"""
        manifest_file = self.memory_path / ".memory_manifest.json"
        if not manifest_file.exists():
            return None
            
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        current_files = []
        for md_file in self.memory_path.glob("*.md"):
            current_files.append({
                "name": md_file.name,
                "size": md_file.stat().st_size,
                "checksum": self.create_checksum(md_file)
            })
        
        # 检查是否有新文件或修改
        new_files = []
        modified_files = []
        
        manifest_names = {f["name"]: f for f in manifest["files"]}
        
        for cf in current_files:
            if cf["name"] not in manifest_names:
                new_files.append(cf["name"])
            elif cf["checksum"] != manifest_names[cf["name"]]["checksum"]:
                modified_files.append(cf["name"])
        
        return {
            "new_files": new_files,
            "modified_files": modified_files,
            "total_files": len(current_files)
        }

# 主程序
if __name__ == "__main__":
    protector = MemoryProtection()
    
    # 启用记忆保护
    result = protector.prevent_reset()
    print(f"✅ 记忆保护已启用")
    print(f"   受保护文件数：{len(result['files'])}")
    
    # 检查完整性
    check = protector.check_manifest()
    print(f"   当前文件数：{check['total_files']}")

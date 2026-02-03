#!/usr/bin/env python3
"""
Clawdbot API 健康检查与自动修复脚本
功能：
1. 检查 API 健康状态
2. 检测 rate limit 错误
3. 自动重启 Gateway 修复
4. 发送告警通知

使用方法：
python3 api_health_check.py
"""

import subprocess
import json
import time
import os
from datetime import datetime

class APIHealthChecker:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        self.auth_path = os.path.expanduser("~/.openclaw/agents/main/agent/auth-profiles.json")
        
    def run_command(self, cmd):
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def check_models(self):
        """检查模型配置"""
        code, stdout, stderr = self.run_command("openclaw-cn models 2>&1")
        if code == 0:
            return True, "OK"
        return False, stderr
    
    def check_auth_profiles(self):
        """检查认证配置"""
        try:
            with open(self.auth_path, 'r') as f:
                auth = json.load(f)
            
            issues = []
            for name, profile in auth.get('profiles', {}).items():
                cooldown_until = profile.get('cooldownUntil')
                if cooldown_until:
                    now = int(time.time())
                    if cooldown_until > now:
                        remaining = cooldown_until - now
                        issues.append(f"{name}: cooldown {remaining}s")
            
            if issues:
                return False, "; ".join(issues)
            return True, "OK"
        except Exception as e:
            return False, str(e)
    
    def restart_gateway(self):
        """重启 Gateway"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 重启 Gateway...")
        self.run_command("openclaw-cn gateway restart")
        time.sleep(3)
        return True
    
    def fix_rate_limit(self):
        """修复 rate limit 问题"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 检测到 rate limit，开始修复...")
        
        # 步骤 1: 重启 Gateway
        self.restart_gateway()
        
        # 步骤 2: 再次检查
        time.sleep(2)
        ok, msg = self.check_auth_profiles()
        if not ok:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 认证问题仍存在: {msg}")
            return False
        
        # 步骤 3: 检查模型
        ok, msg = self.check_models()
        if ok:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 修复成功！")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 修复失败: {msg}")
            return False
    
    def run_full_check(self):
        """运行完整检查"""
        print("="*60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API 健康检查")
        print("="*60)
        
        # 检查 1: 模型配置
        print("\n[1/2] 检查模型配置...")
        ok, msg = self.check_models()
        if ok:
            print("  ✅ 模型配置正常")
        else:
            print(f"  ⚠️ 模型配置异常: {msg}")
            self.fix_rate_limit()
        
        # 检查 2: 认证配置
        print("\n[2/2] 检查认证配置...")
        ok, msg = self.check_auth_profiles()
        if ok:
            print("  ✅ 认证配置正常")
        else:
            print(f"  ⚠️ 认证配置异常: {msg}")
            self.fix_rate_limit()
        
        print("\n" + "="*60)
        print("检查完成")
        print("="*60)

def main():
    checker = APIHealthChecker()
    checker.run_full_check()

if __name__ == "__main__":
    main()

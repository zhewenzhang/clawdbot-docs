#!/usr/bin/env python3
"""
Gmail API 测试脚本
用于验证 Gmail API 连接是否正常
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API 权限范围
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def test_gmail():
    """测试 Gmail API 连接"""
    print("=" * 60)
    print("📧 Gmail API 连接测试")
    print("=" * 60)
    
    creds = None
    
    # 检查是否有已保存的 token
    if os.path.exists('/Users/dave/clawd/token_gmail.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_gmail.json', SCOPES)
    
    # 如果没有有效的凭据，需要登录
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 刷新 Gmail token...")
            creds.refresh(Request())
        else:
            print("⚠️ 需要用户授权 Gmail")
            print("\n步骤：")
            print("1. 运行此脚本后，会自动打开浏览器")
            print("2. 登录 Google 账号")
            print("3. 点击'允许'授权")
            print("4. token 会自动保存到 /Users/dave/clawd/token_gmail.json")
            print("\n运行命令：")
            print("python3 /Users/dave/clawd/scripts/test_gmail_api.py")
            
            # 启动授权流程
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/dave/clawd/gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 保存凭据
        with open('/Users/dave/clawd/token_gmail.json', 'w') as token:
            token.write(creds.to_json())
    
    # 测试 API
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().getProfile(userId='me').execute()
        print(f"\n✅ Gmail API 连接成功！")
        print(f"   邮箱: {results['emailAddress']}")
        print(f"   用户ID: {results['id']}")
        
        # 获取最近邮件
        messages = service.users().messages().list(
            userId='me', maxResults=5).execute()
        print(f"   最近邮件数: {len(messages.get('messages', []))}")
        
        return True
    except Exception as e:
        print(f"❌ Gmail API 连接失败: {e}")
        return False

if __name__ == '__main__':
    test_gmail()

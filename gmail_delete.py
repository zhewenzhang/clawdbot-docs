#!/usr/bin/env python3
"""
Gmail 邮件管理工具 - 带删除权限
"""

import os
from datetime import datetime

CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_credentials.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_token.json")
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'  # 删除权限
]

def get_gmail_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(CREDENTIALS_PATH):
            print("🔐 正在请求完整权限...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
            print("✅ 权限已更新")
        else:
            return None
    
    return build('gmail', 'v1', credentials=creds)

def delete_recent_emails(service, count=10):
    """删除最近邮件"""
    results = service.users().messages().list(userId='me', maxResults=count).execute()
    messages = results.get('messages', [])
    
    deleted = 0
    for msg in messages:
        try:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
            deleted += 1
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    
    return deleted

def main():
    print(f"\n🗑️ Gmail 清理 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    service = get_gmail_service()
    if not service:
        print("❌ Gmail 未配置")
        return
    
    deleted = delete_recent_emails(service, 10)
    print(f"\n✅ 已删除 {deleted} 封邮件")
    print("="*50)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gmail 标记已读 - 不需要删除权限
"""

import os
from datetime import datetime

CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_credentials.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_token.json")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return None
    
    return build('gmail', 'v1', credentials=creds)

def list_emails(service, count=10):
    """列出最近邮件"""
    results = service.users().messages().list(userId='me', maxResults=count).execute()
    return results.get('messages', [])

def main():
    print(f"\n📧 Gmail 管理 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    service = get_gmail_service()
    if not service:
        print("❌ Gmail 未授权")
        return
    
    messages = list_emails(service, 10)
    
    print(f"📬 最近 {len(messages)} 封邮件:")
    print()
    
    for i, msg in enumerate(messages, 1):
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        
        subject = sender = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender = header['value']
        
        if '<' in sender:
            sender = sender.split('<')[0].strip()
        
        print(f"{i}. 【{sender}】")
        print(f"   {subject[:45]}...")
        print()
    
    print("="*50)
    print("💡 如需删除邮件，请在 Gmail 网页版手动清理")
    print("   或运行: python3 ~/clawd/gmail_delete.py (需重新授权)")

if __name__ == "__main__":
    main()

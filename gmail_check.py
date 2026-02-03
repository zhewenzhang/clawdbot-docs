#!/usr/bin/env python3
"""
Gmail 邮件检查工具 - 优化版
格式: 简洁文字列表，适合 Telegram
"""

import os
from datetime import datetime

CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_credentials.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/agents/main/agent/gmail_token.json")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """获取 Gmail 服务"""
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
        else:
            print("❌ Gmail 未授权，请先运行 gmail_check.py 完成 OAuth")
            return None
    
    return build('gmail', 'v1', credentials=creds)

def check_emails(service, max_results=10):
    """检查最近邮件 - 简化格式"""
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return []
    
    emails = []
    for msg in messages[:max_results]:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        
        email_info = {
            'id': msg['id'],
            'subject': '',
            'sender': '',
            'date': '',
        }
        
        for header in headers:
            if header['name'] == 'Subject':
                email_info['subject'] = header['value']
            elif header['name'] == 'From':
                email_info['sender'] = header['value']
            elif header['name'] == 'Date':
                email_info['date'] = header['value']
        
        emails.append(email_info)
    
    return emails

def delete_emails(service, email_ids):
    """删除指定邮件"""
    deleted = []
    for email_id in email_ids:
        try:
            service.users().messages().trash(userId='me', id=email_id).execute()
            deleted.append(email_id)
        except Exception as e:
            print(f"❌ 删除失败: {email_id}")
    return deleted

def format_telegram_report(emails):
    """格式化报告 - Telegram 友好格式"""
    if not emails:
        return "📭 今天没有邮件"
    
    report = f"📧 Gmail - 今日 {len(emails)} 封邮件\n"
    report += "-" * 30 + "\n\n"
    
    for i, email in enumerate(emails, 1):
        # 简化发件人
        sender = email['sender']
        if '<' in sender:
            sender = sender.split('<')[0].strip()
        # 简化主题
        subject = email['subject'][:40] if len(email['subject']) > 40 else email['subject']
        if email['subject'] and len(email['subject']) > 40:
            subject += "..."
        
        report += f"{i}. 【{sender}】\n"
        report += f"   {subject}\n\n"
    
    report += "-" * 30
    report += f"\n💡 回复「/*删除邮件」可清理"
    
    return report

def main():
    print("📧 Gmail 检查...")
    
    service = get_gmail_service()
    if not service:
        return
    
    emails = check_emails(service, 10)
    
    # Telegram 友好格式
    print("\n" + format_telegram_report(emails))

if __name__ == "__main__":
    main()

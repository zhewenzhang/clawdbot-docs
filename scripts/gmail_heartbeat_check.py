#!/usr/bin/env python3
"""
Gmail 自动检查脚本
每日运行，检查重要邮件
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def check_gmail():
    """检查 Gmail"""
    creds = None
    
    # 加载凭据
    if os.path.exists('/Users/dave/clawd/token_gmail.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_gmail.json', SCOPES)
    
    if not creds or not creds.valid:
        return "Gmail 未授权"
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # 获取邮箱信息
        results = service.users().getProfile(userId='me').execute()
        email = results['emailAddress']
        
        # 获取最近邮件
        messages = service.users().messages().list(
            userId='me', maxResults=5, labelIds=['INBOX']).execute()
        
        unread_count = 0
        important_emails = []
        
        for msg in messages.get('messages', []):
            msg_detail = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata').execute()
            
            labels = msg_detail.get('labelIds', [])
            if 'UNREAD' in labels:
                unread_count += 1
            
            # 检查是否有重要关键词
            subject = ''
            for header in msg_detail.get('payload', {}).get('headers', []):
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            
            keywords = ['紧急', '重要', '会议', '日程', '投资', '财报', 'AI', '半导体']
            if any(k in subject for k in keywords):
                important_emails.append(subject)
        
        # 生成报告
        report = "📧 Gmail 检查报告\n"
        report += "-" * 30 + "\n"
        report += f"邮箱: {email}\n"
        report += f"未读邮件: {unread_count}\n\n"
        
        if important_emails:
            report += "📌 重要邮件：\n"
            for e in important_emails[:3]:
                report += f"  - {e}\n"
        else:
            report += "✅ 无重要邮件"
        
        return report
        
    except Exception as e:
        return f"Gmail 检查失败: {str(e)}"

if __name__ == '__main__':
    print(check_gmail())

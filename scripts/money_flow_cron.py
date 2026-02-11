#!/usr/bin/env python3
"""
资金流向定时任务配置
作者: Clawdbot
日期: 2026-02-04

功能:
- 每日收盘后自动更新数据
- 每周生成资金流向周报
- 每月生成资金流向月报
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from a_stock_money_flow_analysis import AStockMoneyFlowAnalyzer


class MoneyFlowCronManager:
    """资金流向定时任务管理器"""
    
    def __init__(self, token: str):
        self.token = token
        self.scripts_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = "data/money_flow"
        
        # 定时任务配置
        self.cron_config = {
            'daily_update': {
                'script': 'a_stock_money_flow_analysis.py',
                'schedule': '0 16 * * 1-5',  # 每周一至周五 16:00 (收盘后)
                'description': '每日资金流向分析'
            },
            'weekly_report': {
                'script': 'sector_analysis_template.py',
                'schedule': '0 17 * * 5',  # 每周五 17:00
                'description': '每周行业资金流向报告'
            },
            'monthly_report': {
                'script': 'generate_monthly_report.py',
                'schedule': '0 9 1 * *',  # 每月1日 9:00
                'description': '每月资金流向月报'
            },
            'alert_check': {
                'script': 'money_flow_alert.py',
                'schedule': '0 9,12,15,16 * * 1-5',  # 工作日 9:00, 12:00, 15:00, 16:00
                'description': '资金流向监控告警'
            }
        }
    
    def generate_crontab(self) -> str:
        """
        生成 crontab 配置
        
        Returns:
            crontab 配置文本
        """
        lines = []
        lines.append("# A 股资金流向分析系统 - 定时任务配置")
        lines.append(f"# 生成时间: {datetime.now().isoformat()}")
        lines.append("#")
        lines.append("# 使用方法:")
        lines.append("#   crontab -e  # 编辑 crontab")
        lines.append("#   crontab -l  # 查看当前 crontab")
        lines.append("#")
        lines.append("# 环境配置:")
        lines.append(f"PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin")
        lines.append(f"PYTHONPATH={self.scripts_dir}")
        lines.append("")
        
        for task_name, config in self.cron_config.items():
            script_path = os.path.join(self.scripts_dir, config['script'])
            schedule = config['schedule']
            description = config['description']
            
            # 生成 cron 行
            line = f"{schedule} cd {self.scripts_dir} && python3 {script_path} >> logs/{task_name}.log 2>&1 # {description}"
            lines.append(line)
        
        return '\n'.join(lines)
    
    def save_crontab_config(self, filepath: str = None):
        """
        保存 crontab 配置文件
        
        Args:
            filepath: 文件路径
        """
        if filepath is None:
            filepath = os.path.join(self.scripts_dir, 'cron_config.txt')
        
        crontab_content = self.generate_crontab()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(crontab_content)
        
        print(f"✅ crontab 配置已保存: {filepath}")
        print("\n使用方法:")
        print(f"  1. 查看配置: cat {filepath}")
        print(f"  2. 安装 crontab: crontab {filepath}")
        print(f"  3. 查看任务: crontab -l")
        
        return filepath
    
    def run_daily_update(self):
        """
        运行每日更新任务
        """
        print("\n" + "="*60)
        print("每日资金流向更新")
        print(f"执行时间: {datetime.now().isoformat()}")
        print("="*60)
        
        analyzer = AStockMoneyFlowAnalyzer(self.token, self.data_dir)
        
        # 更新最近5日数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
        
        # 获取市场汇总
        report = analyzer.run_analysis(days=5)
        
        # 保存数据
        report_file = f"daily_update_{end_date}.json"
        with open(f"{self.data_dir}/{report_file}", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 每日更新完成: {self.data_dir}/{report_file}")
        
        return report
    
    def run_weekly_report(self):
        """
        运行每周报告任务
        """
        print("\n" + "="*60)
        print("每周资金流向报告")
        print(f"执行时间: {datetime.now().isoformat()}")
        print("="*60)
        
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
        
        # 导入行业分析
        from sector_analysis_template import SectorMoneyFlowAnalyzer
        
        analyzer = SectorMoneyFlowAnalyzer(self.token)
        report = analyzer.run_full_analysis(days=7)
        
        # 保存报告
        report_file = f"weekly_report_{end_date}.json"
        with open(f"{self.data_dir}/{report_file}", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 周报生成完成: {self.data_dir}/{report_file}")
        
        return report
    
    def run_monthly_report(self, year: int = None, month: int = None):
        """
        运行每月报告任务
        
        Args:
            year: 年份 (默认当前)
            month: 月份 (默认当前)
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        print("\n" + "="*60)
        print(f"月度资金流向报告: {year}年{month}月")
        print(f"执行时间: {datetime.now().isoformat()}")
        print("="*60)
        
        # 计算月起始日期
        start_date = f"{year}{month:02d}01"
        
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        end_date = (datetime(next_year, next_month, 1) - timedelta(days=1)).strftime('%Y%m%d')
        
        # 初始化分析器
        analyzer = AStockMoneyFlowAnalyzer(self.token, self.data_dir)
        
        # 获取月度数据
        df = analyzer.get_hsgt_money_flow(start_date, end_date)
        
        if df.empty:
            print("⚠️ 无数据")
            return {}
        
        # 生成月度汇总
        monthly_summary = {
            'report_period': f"{start_date} - {end_date}",
            'total_trading_days': len(df),
            'north_money_total': float(df['north_money'].sum()),
            'south_money_total': float(df['south_money'].sum()),
            'avg_north_daily': float(df['north_money'].mean()),
            'avg_south_daily': float(df['south_money'].mean()),
            'max_north_day': df.loc[df['north_money'].idxmax(), 'trade_date'],
            'max_north_value': float(df['north_money'].max()),
            'min_north_day': df.loc[df['north_money'].idxmin(), 'trade_date'],
            'min_north_value': float(df['north_money'].min()),
        }
        
        # 趋势分析
        if len(df) >= 5:
            recent_avg = df.tail(5)['north_money'].mean()
            early_avg = df.head(5)['north_money'].mean()
            monthly_summary['trend'] = 'up' if recent_avg > early_avg else 'down'
            monthly_summary['trend_change'] = (recent_avg - early_avg) / early_avg if early_avg != 0 else 0
        
        # 保存报告
        report = {
            'report_date': datetime.now().isoformat(),
            'period': f"{year}年{month}月",
            'summary': monthly_summary
        }
        
        report_file = f"monthly_report_{year}{month:02d}.json"
        with open(f"{self.data_dir}/{report_file}", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n月度汇总:")
        print(f"  交易天数: {monthly_summary['total_trading_days']}")
        print(f"  北向资金总计: {monthly_summary['north_money_total']:,.2f}")
        print(f"  日均北向: {monthly_summary['avg_north_daily']:,.2f}")
        print(f"  趋势: {monthly_summary.get('trend', 'N/A')}")
        print(f"\n✅ 月报生成完成: {self.data_dir}/{report_file}")
        
        return report
    
    def install_crontab(self):
        """
        安装 crontab
        """
        config_file = self.save_crontab_config()
        
        try:
            # 备份当前 crontab
            subprocess.run(['crontab', '-l'], capture_output=True)
            
            # 安装新 crontab
            result = subprocess.run(['crontab', config_file], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ crontab 安装成功")
                subprocess.run(['crontab', '-l'])
            else:
                print(f"❌ crontab 安装失败: {result.stderr}")
        
        except Exception as e:
            print(f"❌ 安装 crontab 失败: {e}")
    
    def run_task(self, task_name: str):
        """
        运行指定任务
        
        Args:
            task_name: 任务名称 (daily_update, weekly_report, monthly_report, alert_check)
        """
        tasks = {
            'daily_update': self.run_daily_update,
            'weekly_report': self.run_weekly_report,
            'monthly_report': self.run_monthly_report,
            'alert_check': self.run_alert_check
        }
        
        if task_name not in tasks:
            print(f"❌ 未知任务: {task_name}")
            print(f"可用任务: {', '.join(tasks.keys())}")
            return
        
        print(f"\n执行任务: {task_name}")
        tasks[task_name]()
    
    def run_alert_check(self):
        """运行告警检查"""
        from money_flow_alert import run_alert_check
        run_alert_check()


def main():
    """主函数"""
    TOKEN = "18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8"
    
    manager = MoneyFlowCronManager(TOKEN)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'install':
            manager.install_crontab()
        elif command == 'daily':
            manager.run_daily_update()
        elif command == 'weekly':
            manager.run_weekly_report()
        elif command == 'monthly':
            manager.run_monthly_report()
        elif command == 'alert':
            manager.run_alert_check()
        elif command == 'show':
            print(manager.generate_crontab())
        else:
            print(f"未知命令: {command}")
            print("用法: python money_flow_cron.py [命令]")
            print("命令:")
            print("  install - 安装 crontab")
            print("  daily   - 运行每日更新")
            print("  weekly  - 运行周报")
            print("  monthly - 运行月报")
            print("  alert   - 运行告警检查")
            print("  show    - 显示 crontab 配置")
    else:
        # 默认显示 crontab 配置
        print(manager.generate_crontab())


if __name__ == '__main__':
    main()

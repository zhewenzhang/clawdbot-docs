#!/usr/bin/env python3
"""
资金流向监控告警系统
作者: Clawdbot
日期: 2026-02-04

功能:
- 监控主力资金大幅流入/流出
- 监控资金集中度突变
- 发送 Telegram 告警
"""

import json
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from a_stock_money_flow_analysis import AStockMoneyFlowAnalyzer


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MoneyFlowAlert:
    """资金流向告警器"""
    
    def __init__(self, token: str, config_file: str = None):
        """
        初始化告警器
        
        Args:
            token: TuShare API Token
            config_file: 配置文件路径
        """
        self.analyzer = AStockMoneyFlowAnalyzer(token)
        self.config = self._load_config(config_file)
        self.alerts: List[Dict] = []
        
        # 默认阈值配置
        self.thresholds = {
            'main_net_inflow_change': 0.5,      # 主力净流入变化 > 50%
            'main_net_inflow_absolute': 100000000,  # 主力净流入 > 1亿
            'concentration_change': 0.3,        # 资金集中度变化 > 30%
            'concentration_extreme': 0.8,       # 资金集中度 > 80%
            'retail_selloff': -50000000,         # 散户净流出 < -5000万
            'volume_spike': 2.0,                # 成交量放大 > 2倍
        }
        
        # 更新阈值配置
        if self.config and 'thresholds' in self.config:
            self.thresholds.update(self.config['thresholds'])
    
    def _load_config(self, config_file: str = None) -> Dict:
        """加载配置文件"""
        if config_file is None:
            config_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'money_flow_alert_config.json'
            )
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def check_main_net_inflow(self, current: float, previous: float = None) -> Optional[Dict]:
        """
        检查主力净流入
        
        Args:
            current: 当前主力净流入
            previous: 前期主力净流入
            
        Returns:
            告警信息或 None
        """
        alerts = []
        
        # 大幅净流入
        if current > self.thresholds['main_net_inflow_absolute']:
            level = AlertLevel.CRITICAL if current > self.thresholds['main_net_inflow_absolute'] * 3 else AlertLevel.WARNING
            alerts.append({
                'level': level.value,
                'type': 'main_net_inflow_positive',
                'message': f"主力资金大幅净流入: {current:,.2f}",
                'value': current,
                'threshold': self.thresholds['main_net_inflow_absolute']
            })
        
        # 大幅净流出
        if current < -self.thresholds['main_net_inflow_absolute']:
            alerts.append({
                'level': AlertLevel.CRITICAL.value,
                'type': 'main_net_inflow_negative',
                'message': f"主力资金大幅净流出: {current:,.2f}",
                'value': current,
                'threshold': -self.thresholds['main_net_inflow_absolute']
            })
        
        # 变化检测
        if previous is not None and previous != 0:
            change_rate = (current - previous) / abs(previous)
            if abs(change_rate) > self.thresholds['main_net_inflow_change']:
                alerts.append({
                    'level': AlertLevel.WARNING.value,
                    'type': 'main_net_inflow_change',
                    'message': f"主力净流入变化率: {change_rate:.1%}",
                    'value': current,
                    'previous': previous,
                    'change_rate': change_rate
                })
        
        return alerts if alerts else None
    
    def check_concentration(self, concentration: float, previous: float = None) -> Optional[Dict]:
        """
        检查资金集中度
        
        Args:
            concentration: 当前资金集中度
            previous: 前期资金集中度
            
        Returns:
            告警信息或 None
        """
        alerts = []
        
        # 极端集中
        if concentration > self.thresholds['concentration_extreme']:
            alerts.append({
                'level': AlertLevel.WARNING.value,
                'type': 'concentration_high',
                'message': f"资金集中度过高: {concentration:.1%}",
                'value': concentration,
                'threshold': self.thresholds['concentration_extreme']
            })
        
        # 集中度突变
        if previous is not None:
            change = concentration - previous
            if abs(change) > self.thresholds['concentration_change']:
                alerts.append({
                    'level': AlertLevel.INFO.value,
                    'type': 'concentration_change',
                    'message': f"资金集中度突变: {change:+.1%}",
                    'value': concentration,
                    'previous': previous,
                    'change': change
                })
        
        return alerts if alerts else None
    
    def check_retail_sentiment(self, retail_net: float) -> Optional[Dict]:
        """
        检查散户情绪
        
        Args:
            retail_net: 散户净流入
            
        Returns:
            告警信息或 None
        """
        if retail_net < self.thresholds['retail_selloff']:
            return {
                'level': AlertLevel.WARNING.value,
                'type': 'retail_selloff',
                'message': f"散户大幅抛售: {retail_net:,.2f}",
                'value': retail_net,
                'threshold': self.thresholds['retail_selloff']
            }
        return None
    
    def check_stock_alerts(self, ts_code: str, indicators: Dict) -> List[Dict]:
        """
        检查个股告警
        
        Args:
            ts_code: 股票代码
            indicators: 指标字典
            
        Returns:
            告警列表
        """
        alerts = []
        
        # 检查主力净流入
        main_net = indicators.get('main_net_inflow', 0)
        previous_main = indicators.get('previous_main_net_inflow', None)
        
        main_alerts = self.check_main_net_inflow(main_net, previous_main)
        if main_alerts:
            for alert in main_alerts:
                alert['ts_code'] = ts_code
                alerts.append(alert)
        
        # 检查资金集中度
        concentration = indicators.get('concentration', 0)
        previous_concentration = indicators.get('previous_concentration', None)
        
        conc_alerts = self.check_concentration(concentration, previous_concentration)
        if conc_alerts:
            for alert in conc_alerts:
                alert['ts_code'] = ts_code
                alerts.append(alert)
        
        # 检查散户情绪
        retail_net = indicators.get('retail_net_inflow', 0)
        retail_alert = self.check_retail_sentiment(retail_net)
        if retail_alert:
            retail_alert['ts_code'] = ts_code
            alerts.append(retail_alert)
        
        return alerts
    
    def analyze_and_alert(self, ts_code: str, start_date: str, end_date: str = None) -> List[Dict]:
        """
        分析并生成告警
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            告警列表
        """
        # 获取数据
        df = self.analyzer.get_stock_money_flow(ts_code, start_date, end_date)
        
        if df.empty:
            return []
        
        # 计算指标
        indicators = self.analyzer.calculate_stock_indicators(df)
        
        # 获取前期数据用于对比
        previous_df = self.analyzer.get_stock_money_flow(
            ts_code, 
            (datetime.strptime(start_date, '%Y%m%d') - timedelta(days=7)).strftime('%Y%m%d'),
            (datetime.strptime(start_date, '%Y%m%d') - timedelta(days=1)).strftime('%Y%m%d')
        )
        
        if not previous_df.empty:
            previous_indicators = self.analyzer.calculate_stock_indicators(previous_df)
            indicators['previous_main_net_inflow'] = previous_indicators.get('main_net_inflow')
            indicators['previous_concentration'] = previous_indicators.get('concentration')
        
        # 检查告警
        alerts = self.check_stock_alerts(ts_code, indicators)
        self.alerts.extend(alerts)
        
        return alerts
    
    def generate_alert_report(self) -> Dict:
        """
        生成告警报告
        """
        if not self.alerts:
            return {'status': 'no_alerts', 'message': '无告警', 'alerts': []}
        
        # 按级别分组
        critical_alerts = [a for a in self.alerts if a['level'] == AlertLevel.CRITICAL.value]
        warning_alerts = [a for a in self.alerts if a['level'] == AlertLevel.WARNING.value]
        info_alerts = [a for a in self.alerts if a['level'] == AlertLevel.INFO.value]
        
        return {
            'report_time': datetime.now().isoformat(),
            'total_alerts': len(self.alerts),
            'critical_count': len(critical_alerts),
            'warning_count': len(warning_alerts),
            'info_count': len(info_alerts),
            'critical_alerts': critical_alerts,
            'warning_alerts': warning_alerts,
            'info_alerts': info_alerts
        }
    
    def format_telegram_message(self, report: Dict) -> str:
        """
        格式化 Telegram 告警消息
        
        Args:
            report: 告警报告
            
        Returns:
            Telegram 消息文本
        """
        if report['status'] == 'no_alerts':
            return "✅ 资金流向监控\n\n当前无异常告警"
        
        messages = ["⚠️ 资金流向告警\n"]
        
        if report['critical_count'] > 0:
            messages.append(f"🚨 严重告警 ({report['critical_count']} 项)\n")
            for alert in report['critical_alerts'][:5]:  # 最多显示5条
                messages.append(f"• {alert['message']}\n")
        
        if report['warning_count'] > 0:
            messages.append(f"⚠️ 警告 ({report['warning_count']} 项)\n")
            for alert in report['warning_alerts'][:5]:
                messages.append(f"• {alert['message']}\n")
        
        if report['info_count'] > 0:
            messages.append(f"ℹ️ 信息 ({report['info_count']} 项)\n")
            for alert in report['info_alerts'][:3]:
                messages.append(f"• {alert['message']}\n")
        
        messages.append(f"\n报告时间: {report['report_time']}")
        
        return ''.join(messages)


class AlertNotification:
    """告警通知"""
    
    @staticmethod
    def send_telegram(bot_token: str, chat_id: str, message: str) -> bool:
        """
        发送 Telegram 消息
        
        Args:
            bot_token: Telegram Bot Token
            chat_id: Chat ID
            message: 消息内容
            
        Returns:
            是否发送成功
        """
        import requests
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram 发送失败: {e}")
            return False


def run_alert_check(ts_codes: List[str] = None, config: Dict = None):
    """
    运行告警检查
    
    Args:
        ts_codes: 股票代码列表
        config: 配置
    """
    TOKEN = "18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8"
    
    # 默认监控列表
    if ts_codes is None:
        ts_codes = [
            '000001.SZ',  # 平安银行
            '600519.SH',  # 贵州茅台
            '300750.SZ',  # 宁德时代
            '601398.SH',  # 工商银行
            '688981.SH',  # 中芯国际
        ]
    
    alert_system = MoneyFlowAlert(TOKEN)
    
    # 分析每只股票
    start_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
    
    print("\n" + "="*60)
    print("资金流向监控告警")
    print("="*60)
    
    for ts_code in ts_codes:
        print(f"\n[检查] {ts_code}")
        alerts = alert_system.analyze_and_alert(ts_code, start_date)
        
        if alerts:
            for alert in alerts:
                print(f"  ⚠️ [{alert['level']}] {alert['message']}")
        else:
            print(f"  ✅ 无异常")
    
    # 生成报告
    report = alert_system.generate_alert_report()
    
    # 格式化消息
    message = alert_system.format_telegram_message(report)
    
    print(f"\n{'='*60}")
    print("告警汇总")
    print(f"{'='*60}")
    print(message)
    
    # 保存报告
    report_file = f"alert_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(f"data/money_flow/{report_file}", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: data/money_flow/{report_file}")
    
    return report


def main():
    """主函数"""
    run_alert_check()


if __name__ == '__main__':
    main()

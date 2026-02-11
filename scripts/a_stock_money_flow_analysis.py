#!/usr/bin/env python3
"""
A 股资金流向分析系统
作者: Clawdbot
日期: 2026-02-04

功能:
- 行业资金流向分析
- 个股资金流向分析
- 融资融券数据监控
- 市场情绪分析
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional


class AStockMoneyFlowAnalyzer:
    """A 股资金流向分析器"""
    
    def __init__(self, token: str, data_dir: str = "data/money_flow"):
        """
        初始化分析器
        
        Args:
            token: TuShare API Token
            data_dir: 数据存储目录
        """
        ts.set_token(token)
        self.pro = ts.pro_api()
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(f"{data_dir}/industry", exist_ok=True)
        os.makedirs(f"{data_dir}/daily", exist_ok=True)
    
    # ==================== 数据获取模块 ====================
    
    def get_hsgt_money_flow(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取沪深港通资金流向
        
        Args:
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            
        Returns:
            沪深港通资金流向数据
        """
        try:
            df = self.pro.moneyflow_hsgt(start_date=start_date, end_date=end_date)
            print(f"[HSGT] 获取 {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"[HSGT] 获取失败: {e}")
            return pd.DataFrame()
    
    def get_stock_money_flow(self, ts_code: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """
        获取个股资金流向
        
        Args:
            ts_code: 股票代码 (如 000001.SZ)
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            个股资金流向数据
        """
        try:
            params = {'ts_code': ts_code, 'start_date': start_date}
            if end_date:
                params['end_date'] = end_date
                
            df = self.pro.moneyflow(**params)
            print(f"[Stock] {ts_code}: 获取 {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"[Stock] {ts_code} 获取失败: {e}")
            return pd.DataFrame()
    
    def get_margin_detail(self, ts_code: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """
        获取融资融券明细
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            融资融券明细数据
        """
        try:
            params = {'ts_code': ts_code, 'start_date': start_date}
            if end_date:
                params['end_date'] = end_date
                
            df = self.pro.margin_detail(**params)
            print(f"[Margin] {ts_code}: 获取 {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"[Margin] {ts_code} 获取失败: {e}")
            return pd.DataFrame()
    
    def get_market_summary(self, trade_date: str) -> Dict:
        """
        获取当日市场资金汇总
        
        Args:
            trade_date: 交易日期
            
        Returns:
            市场汇总数据
        """
        df = self.get_hsgt_money_flow(trade_date, trade_date)
        if df.empty:
            return {}
        
        summary = {
            'trade_date': trade_date,
            'north_money': float(df['north_money'].sum()) if 'north_money' in df.columns else 0,
            'south_money': float(df['south_money'].sum()) if 'south_money' in df.columns else 0,
            'ggt_ss': float(df['ggt_ss'].sum()) if 'ggt_ss' in df.columns else 0,
            'ggt_sz': float(df['ggt_sz'].sum()) if 'ggt_sz' in df.columns else 0,
            'hgt': float(df['hgt'].sum()) if 'hgt' in df.columns else 0,
            'sgt': float(df['sgt'].sum()) if 'sgt' in df.columns else 0,
        }
        
        return summary
    
    # ==================== 分析指标模块 ====================
    
    def calculate_stock_indicators(self, df: pd.DataFrame) -> Dict:
        """
        计算个股资金流向指标
        
        Args:
            df: 个股资金流向数据
            
        Returns:
            分析指标字典
        """
        if df.empty:
            return {}
        
        # 提取关键列
        buy_sm_amount = df['buy_sm_amount'].sum()  # 小单买入金额
        sell_sm_amount = df['sell_sm_amount'].sum()  # 小单卖出金额
        buy_md_amount = df['buy_md_amount'].sum()  # 中单买入金额
        sell_md_amount = df['sell_md_amount'].sum()  # 中单卖出金额
        buy_lg_amount = df['buy_lg_amount'].sum()  # 大单买入金额
        sell_lg_amount = df['sell_lg_amount'].sum()  # 大单卖出金额
        buy_elg_amount = df['buy_elg_amount'].sum()  # 特大单买入金额
        sell_elg_amount = df['sell_elg_amount'].sum()  # 特大单卖出金额
        
        # 计算净流入
        # 散户: 小单 (sm)
        retail_net = buy_sm_amount - sell_sm_amount
        
        # 主力: 中单+大单+特大单
        main_buy = buy_md_amount + buy_lg_amount + buy_elg_amount
        main_sell = sell_md_amount + sell_lg_amount + sell_elg_amount
        main_net = main_buy - main_sell
        
        # 总净流入
        total_net = retail_net + main_net
        
        # 资金集中度 (主力净流入 / 总净流入)
        concentration = main_net / total_net if total_net != 0 else 0
        
        # 计算买卖单数
        net_mf_vol = df['net_mf_vol'].sum() if 'net_mf_vol' in df.columns else 0
        
        return {
            'retail_net_inflow': retail_net,
            'main_net_inflow': main_net,
            'total_net_inflow': total_net,
            'concentration': concentration,
            'net_mf_volume': net_mf_vol,
            'buy_sm_amount': buy_sm_amount,
            'sell_sm_amount': sell_sm_amount,
            'buy_lg_amount': buy_lg_amount,
            'sell_lg_amount': sell_lg_amount,
        }
    
    def calculate_continuity(self, df: pd.DataFrame, days: int = 5) -> Dict:
        """
        计算资金连续性指标
        
        Args:
            df: 资金流向数据
            days: 统计天数
            
        Returns:
            连续性指标
        """
        if len(df) < days:
            return {'consecutive_positive_days': 0, 'positive_ratio': 0}
        
        # 取最近 N 天
        recent_df = df.tail(days)
        
        # 计算每日净流入
        daily_net = recent_df['buy_md_amount'] + recent_df['buy_lg_amount'] + recent_df['buy_elg_amount'] - \
                   (recent_df['sell_md_amount'] + recent_df['sell_lg_amount'] + recent_df['sell_elg_amount'])
        
        # 正流入天数
        positive_days = (daily_net > 0).sum()
        positive_ratio = positive_days / days
        
        return {
            'consecutive_positive_days': positive_days,
            'positive_ratio': positive_ratio,
            'days_analyzed': days
        }
    
    def calculate_flow_rate(self, df: pd.DataFrame, total_amount: float) -> float:
        """
        计算净流入率
        
        Args:
            df: 资金流向数据
            total_amount: 成交额
            
        Returns:
            净流入率
        """
        if total_amount == 0:
            return 0
        
        net_inflow = df['buy_md_amount'].sum() + df['buy_lg_amount'].sum() + df['buy_elg_amount'].sum() - \
                     (df['sell_md_amount'].sum() + df['sell_lg_amount'].sum() + df['sell_elg_amount'].sum())
        
        return net_inflow / total_amount
    
    # ==================== 行业分析模块 ====================
    
    def get_industry_list(self) -> List[str]:
        """
        获取预设行业列表
        
        Returns:
            行业代码列表
        """
        return {
            'bank': '银行',
            'securities': '券商',
            'insurance': '保险',
            'pharma': '医药',
            'semiconductor': '半导体',
            'new_energy': '新能源',
            'consumer': '消费',
            'real_estate': '房地产',
            'steel': '钢铁',
            'aviation': '航空'
        }
    
    def analyze_sector(self, sector_name: str, ts_codes: List[str], 
                       start_date: str, end_date: str = None) -> pd.DataFrame:
        """
        分析特定行业
        
        Args:
            sector_name: 行业名称
            ts_codes: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            行业分析结果 DataFrame
        """
        results = []
        
        for ts_code in ts_codes:
            df = self.get_stock_money_flow(ts_code, start_date, end_date)
            if not df.empty:
                indicators = self.calculate_stock_indicators(df)
                indicators['ts_code'] = ts_code
                indicators['sector'] = sector_name
                results.append(indicators)
        
        return pd.DataFrame(results)
    
    # ==================== 报告生成模块 ====================
    
    def generate_daily_report(self, trade_date: str) -> Dict:
        """
        生成当日资金流向报告
        
        Args:
            trade_date: 交易日期
            
        Returns:
            报告字典
        """
        # 获取市场汇总
        market_data = self.get_market_summary(trade_date)
        
        if not market_data:
            return {'error': f'无法获取 {trade_date} 的数据'}
        
        # 计算市场情绪
        north_money = market_data.get('north_money', 0)
        market_sentiment = 'bullish' if north_money > 0 else 'bearish'
        
        report = {
            'report_date': datetime.now().isoformat(),
            'trade_date': trade_date,
            'market_summary': market_data,
            'market_sentiment': market_sentiment,
            'north_money_status': '净流入' if north_money > 0 else '净流出',
            'insight': self._generate_insight(market_data)
        }
        
        return report
    
    def _generate_insight(self, market_data: Dict) -> str:
        """生成市场洞察"""
        north = market_data.get('north_money', 0)
        south = market_data.get('south_money', 0)
        
        if north > south * 2:
            return "北向资金大幅流入，市场情绪积极"
        elif south > north * 2:
            return "南向资金主导，可能存在资金外流压力"
        elif north > 0 and south > 0:
            return "双向资金均呈流入，市场活跃"
        else:
            return "资金流向偏谨慎，建议观望"
    
    def save_data(self, df: pd.DataFrame, category: str, filename: str):
        """
        保存数据到文件
        
        Args:
            df: DataFrame 数据
            category: 类别 (industry/daily)
            filename: 文件名
        """
        filepath = f"{self.data_dir}/{category}/{filename}"
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"[Save] {filepath}")
    
    # ==================== 主函数入口 ====================
    
    def run_analysis(self, days: int = 5):
        """
        运行完整分析流程
        
        Args:
            days: 分析天数
        """
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        print(f"\n{'='*60}")
        print(f"A 股资金流向分析")
        print(f"分析周期: {start_date} - {end_date}")
        print(f"{'='*60}\n")
        
        # 1. 获取市场汇总
        print("[1] 获取市场资金汇总...")
        market_report = self.generate_daily_report(end_date)
        
        # 2. 生成并保存报告
        print("\n[2] 生成分析报告...")
        report_file = f"daily_report_{end_date}.json"
        with open(f"{self.data_dir}/daily/{report_file}", 'w', encoding='utf-8') as f:
            json.dump(market_report, f, ensure_ascii=False, indent=2)
        
        # 3. 输出报告
        print(f"\n{'='*60}")
        print("市场分析报告")
        print(f"{'='*60}")
        print(f"交易日期: {market_report.get('trade_date')}")
        print(f"北向资金: {market_report['market_summary'].get('north_money', 0):,.2f}")
        print(f"南向资金: {market_report['market_summary'].get('south_money', 0):,.2f}")
        print(f"市场情绪: {market_report['market_sentiment']}")
        print(f"市场洞察: {market_report['insight']}")
        print(f"{'='*60}\n")
        
        return market_report


def main():
    """主函数"""
    # TuShare Token
    TOKEN = "18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8"
    
    # 初始化分析器
    analyzer = AStockMoneyFlowAnalyzer(
        token=TOKEN,
        data_dir="data/money_flow"
    )
    
    # 运行分析
    report = analyzer.run_analysis(days=5)
    
    return report


if __name__ == '__main__':
    main()

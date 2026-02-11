#!/usr/bin/env python3
"""
行业资金流向分析模板
作者: Clawdbot
日期: 2026-02-04

预设行业列表:
- 银行 (Bank)
- 券商 (Securities)
- 医药 (Pharma)
- 半导体 (Semiconductor)
- 新能源 (New Energy)
- 消费 (Consumer)
"""

import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from a_stock_money_flow_analysis import AStockMoneyFlowAnalyzer


class SectorMoneyFlowAnalyzer:
    """行业资金流向分析器"""
    
    def __init__(self, token: str, data_dir: str = "data/money_flow"):
        """
        初始化行业分析器
        """
        self.analyzer = AStockMoneyFlowAnalyzer(token, data_dir)
        
        # 预设行业及成分股
        self.sectors = {
            '银行': {
                'description': '银行业上市公司',
                'ts_codes': [
                    '601398.SH',  # 工商银行
                    '601939.SH',  # 建设银行
                    '601288.SH',  # 农业银行
                    '601988.SH',  # 中国银行
                    '600016.SH',  # 民生银行
                    '600015.SH',  # 华夏银行
                ]
            },
            '券商': {
                'description': '证券业上市公司',
                'ts_codes': [
                    '600030.SH',  # 中信证券
                    '600837.SH',  # 海通证券
                    '601066.SH',  # 中信建投
                    '600958.SH',  # 东方证券
                    '600999.SH',  # 招商证券
                    '000686.SZ',  # 东北证券
                ]
            },
            '医药': {
                'description': '医药生物行业',
                'ts_codes': [
                    '600276.SH',  # 恒瑞医药
                    '000538.SZ',  # 云南白药
                    '600518.SH',  # 贵州百灵
                    '300003.SZ',  # 乐普医疗
                    '000423.SZ',  # 东阿阿胶
                    '600436.SH',  # 片仔癀
                ]
            },
            '半导体': {
                'description': '半导体芯片行业',
                'ts_codes': [
                    '688981.SH',  # 中芯国际
                    '600460.SH',  # 士兰微
                    '300474.SZ',  # 景嘉微
                    '002475.SZ',  # 立讯精密
                    '000725.SZ',  # 京东方A
                    '603986.SH',  # 兆易创新
                ]
            },
            '新能源': {
                'description': '新能源行业',
                'ts_codes': [
                    '002594.SZ',  # 比亚迪
                    '300750.SZ',  # 宁德时代
                    '600438.SH',  # 通威股份
                    '601012.SH',  # 隆基绿能
                    '002129.SZ',  # 中环股份
                    '002709.SZ',  # 天赐材料
                ]
            },
            '消费': {
                'description': '消费行业',
                'ts_codes': [
                    '000858.SZ',  # 五粮液
                    '600519.SH',  # 贵州茅台
                    '603288.SH',  # 海天味业
                    '000568.SZ',  # 泸州老窖
                    '600887.SH',  # 伊利股份
                    '000651.SZ',  # 格力电器
                ]
            },
            '科技': {
                'description': '科技行业',
                'ts_codes': [
                    '002410.SZ',  # 广联达
                    '002410.SZ',  # 恒生电子
                    '300059.SZ',  # 东方财富
                    '600850.SH',  # 华东电脑
                    '000977.SZ',  # 浪潮信息
                    '002230.SZ',  # 科大讯飞
                ]
            }
        }
    
    def analyze_all_sectors(self, start_date: str, end_date: str = None) -> Dict[str, pd.DataFrame]:
        """
        分析所有预设行业
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            各行业分析结果字典
        """
        all_results = {}
        
        print(f"\n{'='*70}")
        print(f"行业资金流向分析")
        print(f"{'='*70}\n")
        
        for sector_name, sector_info in self.sectors.items():
            print(f"\n[分析行业] {sector_name} ({sector_info['description']})")
            print("-" * 50)
            
            # 分析该行业
            result = self.analyzer.analyze_sector(
                sector_name=sector_name,
                ts_codes=sector_info['ts_codes'],
                start_date=start_date,
                end_date=end_date
            )
            
            if not result.empty:
                # 保存结果
                filename = f"sector_{sector_name}_{start_date}.csv"
                self.analyzer.save_data(result, 'industry', filename)
                
                # 计算行业汇总
                sector_summary = self._summarize_sector(result, sector_name)
                all_results[sector_name] = sector_summary
                
                # 打印汇总
                self._print_sector_summary(sector_summary)
            else:
                print(f"  ⚠️ 无数据")
        
        return all_results
    
    def _summarize_sector(self, df: pd.DataFrame, sector_name: str) -> Dict:
        """
        汇总行业数据
        """
        if df.empty:
            return {}
        
        total_main = df['main_net_inflow'].sum()
        total_retail = df['retail_net_inflow'].sum()
        total_inflow = df['total_net_inflow'].sum()
        avg_concentration = df['concentration'].mean()
        
        # 找出资金流入最多的股票
        top_stock = df.loc[df['total_net_inflow'].idxmax()] if not df.empty else {}
        
        return {
            'sector': sector_name,
            'stock_count': len(df),
            'total_main_net_inflow': total_main,
            'total_retail_net_inflow': total_retail,
            'total_net_inflow': total_inflow,
            'avg_concentration': avg_concentration,
            'top_stock': {
                'ts_code': top_stock.get('ts_code', 'N/A'),
                'net_inflow': top_stock.get('total_net_inflow', 0)
            },
            'market_sentiment': 'bullish' if total_main > 0 else 'bearish'
        }
    
    def _print_sector_summary(self, summary: Dict):
        """打印行业汇总"""
        if not summary:
            return
        
        print(f"\n  股票数量: {summary['stock_count']}")
        print(f"  主力净流入: {summary['total_main_net_inflow']:,.2f}")
        print(f"  散户净流入: {summary['total_retail_net_inflow']:,.2f}")
        print(f"  总净流入: {summary['total_net_inflow']:,.2f}")
        print(f"  资金集中度: {summary['avg_concentration']:.2%}")
        print(f"  资金最多: {summary['top_stock']['ts_code']} ({summary['top_stock']['net_inflow']:,.2f})")
        print(f"  市场情绪: {summary['market_sentiment']}")
    
    def generate_sector_comparison_report(self, results: Dict[str, Dict]) -> Dict:
        """
        生成行业对比报告
        """
        if not results:
            return {}
        
        # 转换为 DataFrame 进行排序
        df = pd.DataFrame(results).T
        df = df.sort_values('total_net_inflow', ascending=False)
        
        # 生成报告
        report = {
            'report_date': datetime.now().isoformat(),
            'sector_count': len(results),
            'market_overview': self._get_market_overview(results),
            'sector_ranking': df.to_dict('records'),
            'recommendations': self._generate_recommendations(results)
        }
        
        return report
    
    def _get_market_overview(self, results: Dict) -> Dict:
        """获取市场概览"""
        df = pd.DataFrame(results).T if results else pd.DataFrame()
        
        if df.empty:
            return {}
        
        bullish_sectors = (df['market_sentiment'] == 'bullish').sum()
        total_net_inflow = df['total_net_inflow'].sum()
        
        return {
            'total_sectors': len(results),
            'bullish_sectors': bullish_sectors,
            'bearish_sectors': len(results) - bullish_sectors,
            'total_net_inflow': total_net_inflow,
            'sentiment': '偏多' if bullish_sectors > len(results) / 2 else '偏空'
        }
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """生成投资建议"""
        recommendations = []
        
        df = pd.DataFrame(results).T if results else pd.DataFrame()
        
        if df.empty:
            return ['数据不足，无法生成建议']
        
        # 资金流入最多的行业
        top_sectors = df.nlargest(3, 'total_net_inflow')
        recommendations.append(f"资金关注度最高的行业: {', '.join(top_sectors.index.tolist())}")
        
        # 资金集中度最高的行业
        high_concentration = df.nlargest(3, 'avg_concentration')
        recommendations.append(f"资金最集中的行业: {', '.join(high_concentration.index.tolist())}")
        
        # 市场情绪
        bullish_count = (df['market_sentiment'] == 'bullish').sum()
        if bullish_count > len(df) / 2:
            recommendations.append("整体市场情绪偏多，可关注资金流入板块")
        else:
            recommendations.append("整体市场情绪偏空，建议谨慎操作")
        
        return recommendations
    
    def run_full_analysis(self, days: int = 5):
        """
        运行完整行业分析
        """
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        print(f"\n{'='*70}")
        print(f"行业资金流向分析报告")
        print(f"分析周期: {start_date} - {end_date}")
        print(f"{'='*70}")
        
        # 分析所有行业
        results = self.analyze_all_sectors(start_date, end_date)
        
        # 生成对比报告
        if results:
            comparison_report = self.generate_sector_comparison_report(results)
            
            print(f"\n{'='*70}")
            print("行业对比报告")
            print(f"{'='*70}")
            print(f"\n市场概览:")
            print(f"  分析行业数: {comparison_report['market_overview']['total_sectors']}")
            print(f"  偏多行业数: {comparison_report['market_overview']['bullish_sectors']}")
            print(f"  偏空行业数: {comparison_report['market_overview']['bearish_sectors']}")
            print(f"  总净流入: {comparison_report['market_overview']['total_net_inflow']:,.2f}")
            print(f"  市场情绪: {comparison_report['market_overview']['sentiment']}")
            
            print(f"\n投资建议:")
            for rec in comparison_report['recommendations']:
                print(f"  • {rec}")
            
            # 保存报告
            report_file = f"sector_comparison_report_{end_date}.json"
            with open(f"data/money_flow/{report_file}", 'w', encoding='utf-8') as f:
                json.dump(comparison_report, f, ensure_ascii=False, indent=2)
            print(f"\n报告已保存: data/money_flow/{report_file}")
        
        return comparison_report


def main():
    """主函数"""
    TOKEN = "18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8"
    
    analyzer = SectorMoneyFlowAnalyzer(TOKEN)
    report = analyzer.run_full_analysis(days=5)
    
    return report


if __name__ == '__main__':
    main()

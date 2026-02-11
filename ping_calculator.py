#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坪↔平方米 換算計算器
使用方式：python ping_calculator.py
"""

TWD_TO_CNY = 0.219  # 匯率：1 臺幣 = 0.219 人民币
PING_TO_SQM = 3.3058  # 1 坪 = 3.3058 平方米

def calculate(ping_price):
    """計算一平方公尺多少人民幣"""
    sqm_price = (ping_price / PING_TO_SQM) * TWD_TO_CNY
    return sqm_price

def main():
    print("=" * 40)
    print("🏠 坪↔平方米 換算計算器")
    print("=" * 40)
    print(f"📊 匯率：1 臺幣 = {TWD_TO_CNY} 人民币")
    print(f"📐 換算：1 坪 = {PING_TO_SQM} 平方米")
    print("=" * 40)
    print()
    
    while True:
        try:
            user_input = input("💰 輸入一坪多少臺幣（例如：50 或 50萬）：")
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("\n👋 再見！")
                break
            
            # 處理「萬」單位
            price = float(user_input.replace('萬', '').replace(',', '').strip())
            
            if '萬' in user_input:
                price = price * 10000
            
            if price <= 0:
                print("❌ 請輸入大於 0 的金額！")
                continue
            
            result = calculate(price)
            print()
            print("-" * 40)
            print(f"📍 輸入：{price:,.0f} 臺幣 / 坪")
            print(f"📍 結果：{result:.2f} 人民币 / 平方米")
            print("-" * 40)
            print()
            
        except ValueError:
            print("❌ 請輸入有效的數字！")
            print()
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break

if __name__ == "__main__":
    main()

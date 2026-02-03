# Excel 自动化报告生成：VBA/Python xlwings
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、Excel 自动化概述

### 1.1 自动化方式

```
Excel 自动化方式

├── VBA（Visual Basic for Applications）
│   ├── 内置在 Excel 中
│   ├── 无需额外安装
│   └── 适合简单任务
│
└── Python + xlwings
    ├── 需要安装 Python 和 xlwings
    ├── 功能强大
    ├── 可与其他 Python 库集成
    └── 适合复杂任务
```

### 1.2 应用场景

| 场景 | 推荐方式 | 说明 |
|------|----------|------|
| **格式调整** | VBA | 简单快捷 |
| **数据更新** | VBA/xlwings | 均可 |
| **图表生成** | xlwings | 与 Python 集成 |
| **复杂计算** | xlwings | Python 计算能力 |
| **自动化报告** | xlwings | 批量生成 |
| **数据抓取** | xlwings | 与 akshare 集成 |

---

## 二、VBA 实战

### 2.1 VBA 基础

**打开 VBA 编辑器**
- 按 `Alt + F11`
- 或：开发工具 → Visual Basic

**基本结构**

```vba
Sub 宏名称()
    ' 代码在这里
End Sub
```

### 2.2 数据操作

**自动更新数据**

```vba
Sub 更新数据()
    ' 刷新所有数据透视表
    Dim pt As PivotTable
    For Each pt In ActiveSheet.PivotTables
        pt.RefreshTable
    Next pt
    
    ' 刷新所有链接
    ActiveWorkbook.RefreshAll
    
    MsgBox "数据更新完成！"
End Sub
```

**自动计算财务指标**

```vba
Sub 计算财务指标()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("财务数据")
    
    ' 获取数据
    Dim revenue As Double
    Dim cost As Double
    Dim expense As Double
    
    revenue = ws.Range("B2").Value
    cost = ws.Range("B3").Value
    expense = ws.Range("B4").Value
    
    ' 计算毛利率
    ws.Range("B6").Value = (revenue - cost) / revenue
    
    ' 计算净利润
    ws.Range("B7").Value = revenue - cost - expense
    
    ' 计算净利润率
    ws.Range("B8").Value = ws.Range("B7").Value / revenue
    
    MsgBox "财务指标计算完成！"
End Sub
```

### 2.3 图表自动化

**自动生成图表**

```vba
Sub 生成股价走势图()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("股价数据")
    
    ' 清除旧图表
    Dim ch As ChartObject
    For Each ch In ws.ChartObjects
        ch.Delete
    Next ch
    
    ' 创建新图表
    Set ch = ws.ChartObjects.Add(Left:=100, Width:=500, Top:=50, Height:=300)
    ch.Chart.SetSourceData Source:=ws.Range("A1:B100")
    ch.Chart.ChartType = xlLine
    ch.Chart.HasTitle = True
    ch.Chart.ChartTitle.Text = "股价走势图"
    
    MsgBox "图表生成完成！"
End Sub
```

### 2.4 报告自动生成

**自动生成月报**

```vba
Sub 生成月报()
    Dim ws As Worksheet
    Dim report_ws As Worksheet
    
    Set ws = ThisWorkbook.Sheets("原始数据")
    
    ' 创建新报告表
    Set report_ws = ThisWorkbook.Sheets.Add
    report_ws.Name = "月报_" & Format(Date, "yyyymmdd")
    
    ' 复制数据
    ws.Range("A1:E50").Copy
    report_ws.Range("A1").PasteSpecial Paste:=xlPasteValues
    
    ' 设置格式
    report_ws.Columns("A:E").AutoFit
    
    ' 添加标题
    report_ws.Range("A1").Value = "月度报告"
    report_ws.Range("A1").Font.Size = 18
    report_ws.Range("A1").Font.Bold = True
    
    ' 添加日期
    report_ws.Range("A2").Value = "生成日期: " & Format(Date, "yyyy-mm-dd")
    
    MsgBox "月报生成完成！"
End Sub
```

### 2.5 VBA 常用代码

**文件操作**

```vba
' 打开文件
Workbooks.Open "C:\data\stock.xlsx"

' 保存文件
ActiveWorkbook.SaveAs "C:\report\output.xlsx"

' 关闭文件
Workbooks("output.xlsx").Close
```

**数据处理**

```vba
' 筛选数据
ActiveSheet.Range("A1:C100").AutoFilter Field:=2, Criteria1:=">1000"

' 排序数据
ActiveSheet.Sort.SortFields.Clear
ActiveSheet.Sort.SortFields.Add Key:=Range("B1:B100"), _
    SortOn:=xlSortOnValues, Order:=xlDescending
ActiveSheet.Sort.Apply

' 去重
ActiveSheet.Range("A1:C100").RemoveDuplicates Columns:=1, Header:=xlYes
```

**格式设置**

```vba
' 设置列宽
Columns("A:A").ColumnWidth = 15

' 设置货币格式
Range("B2:B100").NumberFormat = "$#,##0.00"

' 设置百分比格式
Range("C2:C100").NumberFormat = "0.00%"

' 设置条件格式
Range("D2:D100").FormatConditions.Add Type:=xlCellValue, _
    Operator:=xlGreater, Formula1:="=0"
Range("D2:D100").FormatConditions(1).Interior.Color = RGB(0, 255, 0)
```

---

## 三、Python xlwings 实战

### 3.1 xlwings 基础

**安装 xlwings**

```bash
pip install xlwings
```

**基础用法**

```python
import xlwings as xw

# 打开 Excel
app = xw.App(visible=True)
wb = app.books.open('template.xlsx')

# 或新建 Excel
wb = xw.books.add()

# 关闭 Excel
wb.close()
app.quit()
```

### 3.2 数据操作

**读取数据**

```python
import xlwings as xw

# 打开 Excel
wb = xw.books.open('data.xlsx')
sheet = wb.sheets['Sheet1']

# 读取单个单元格
a1 = sheet.range('A1').value
print(f"A1: {a1}")

# 读取区域数据
data = sheet.range('A1:C10').value
print(data)

# 读取整列
col_a = sheet.range('A:A').value
print(col_a)

# 读取整行
row_1 = sheet.range('1:1').value
print(row_1)
```

**写入数据**

```python
import xlwings as xw

wb = xw.books.add()
sheet = wb.sheets['Sheet1']

# 写入单个单元格
sheet.range('A1').value = "财务指标"

# 写入列表（行）
sheet.range('A2').value = ['营收', '成本', '利润']

# 写入列表（列）
sheet.range('B2').value = [[100], [80], [20]]

# 写入二维列表
data = [
    ['项目', '数值'],
    ['营收', 1000],
    ['成本', 600],
    ['利润', 400]
]
sheet.range('A1').value = data

# 保存
wb.save('output.xlsx')
wb.close()
```

### 3.3 格式设置

```python
import xlwings as xw

wb = xw.books.add()
sheet = wb.sheets['Sheet1']

# 写入数据
sheet.range('A1').value = [['项目', '数值'], ['营收', 1000], ['成本', 600], ['利润', 400]]

# 设置列宽
sheet.range('A:A').column_width = 15
sheet.range('B:B').column_width = 20

# 设置字体
sheet.range('A1').font.size = 14
sheet.range('A1').font.bold = True
sheet.range('A1').font.name = '微软雅黑'

# 设置数字格式
sheet.range('B2:B4').number_format = '#,##0'

# 设置边框
sheet.range('A1:B4').api.Borders.LineStyle = 1

# 设置背景色
sheet.range('A1').api.Interior.Color = 0xFF0000  # 红色

# 自动调整列宽
sheet.range('A:B').columns.autofit()

# 保存
wb.save('formatted.xlsx')
wb.close()
```

### 3.4 图表操作

```python
import xlwings as xw

wb = xw.books.open('data.xlsx')
sheet = wb.sheets['Sheet1']

# 清除旧图表
for chart in sheet.charts:
    chart.delete()

# 创建图表
chart = sheet.charts.add()
chart.set_source_data(sheet.range('A1:B10'))
chart.chart_type = 'line'

# 设置图表标题
chart.has_title = True
chart.chart_title.text = '股价走势图'

# 设置坐标轴
chart.value_axis.has_title = True
chart.value_axis.axis_title.text = '价格'

# 保存
wb.save('chart.xlsx')
wb.close()
```

### 3.5 与 pandas 集成

```python
import xlwings as xw
import pandas as pd
import akshare as ak

# 获取股票数据
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                         start_date="20230101", end_date="20231231")

# 数据处理
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 打开 Excel
wb = xw.books.add()
sheet = wb.sheets['Sheet1']

# 写入数据（从 A1 开始）
sheet.range('A1').value = df.columns.tolist()
sheet.range('A2').value = df.values.tolist()

# 设置标题格式
sheet.range('A1').expand('right').font.bold = True
sheet.range('A1').expand('right').font.size = 12

# 自动调整列宽
sheet.columns.autofit()

# 添加计算
sheet.range('H1').value = "涨跌幅"
for i in range(len(df)):
    sheet.range(f'H{i+2}').value = df['涨跌幅'].iloc[i]

# 条件格式
sheet.range('H2:H250').api.FormatConditions.Add(
    Type=xlwings.constants.FormatConditionType.xlCellValue,
    Operator=xlwings.constants.Operator.xlGreater,
    Formula1='=0'
).Interior.Color = 0xFF0000  # 红色

# 保存
wb.save('stock_analysis.xlsx')
wb.close()

print("Excel 报告生成完成！")
```

### 3.6 自动化报告生成

```python
import xlwings as xw
import pandas as pd
import akshare as ak
from datetime import datetime

def generate_stock_report(stock_code, stock_name):
    """生成股票分析报告"""
    
    # 获取数据
    df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", 
                            start_date="20230101", end_date=datetime.now().strftime('%Y%m%d'))
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values('日期')
    
    # 计算指标
    latest_price = df['收盘'].iloc[-1]
    year_high = df['最高'].max()
    year_low = df['最低'].min()
    year_change = (latest_price - df['收盘'].iloc[0]) / df['收盘'].iloc[0] * 100
    
    # 创建 Excel
    wb = xw.books.add()
    sheet = wb.sheets['Sheet1']
    
    # 设置标题
    sheet.range('A1').value = f"{stock_name} ({stock_code}) 年度分析报告"
    sheet.range('A1').font.size = 18
    sheet.range('A1').font.bold = True
    
    sheet.range('A3').value = "报告日期:"
    sheet.range('B3').value = datetime.now().strftime('%Y-%m-%d')
    
    # 基本信息
    sheet.range('A5').value = "基本信息"
    sheet.range('A5').font.bold = True
    
    info_data = [
        ['最新收盘价', f'{latest_price:.2f}'],
        ['年度最高价', f'{year_high:.2f}'],
        ['年度最低价', f'{year_low:.2f}'],
        ['年度涨跌幅', f'{year_change:.2f}%'],
        ['成交额（万）', f'{df["成交额"].sum()/1e8:.2f}'],
        ['成交量（万）', f'{df["成交量"].sum()/1e8:.2f}']
    ]
    sheet.range('A6').value = info_data
    
    # 写入行情数据
    sheet.range('A14').value = "年度行情数据"
    sheet.range('A14').font.bold = True
    
    headers = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '涨跌幅']
    sheet.range('A15').value = headers
    
    # 写入最近 100 天数据
    recent_data = df[['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '涨跌幅']].tail(100)
    sheet.range('A16').value = recent_data.values.tolist()
    
    # 设置格式
    sheet.range('A:H').columns.autofit()
    
    # 保存
    filename = f"{stock_name}_report.xlsx"
    wb.save(filename)
    wb.close()
    
    print(f"报告已生成: {filename}")
    return filename

# 生成报告
generate_stock_report("600519", "贵州茅台")
generate_stock_report("000001", "平安银行")
```

---

## 四、自动化报告模板

### 4.1 月度投资报告模板

```python
import xlwings as xw
import pandas as pd
from datetime import datetime

def generate_monthly_report():
    """生成月度投资报告"""
    
    wb = xw.books.add()
    sheet = wb.sheets['Sheet1']
    
    # 标题
    sheet.range('A1').value = "月度投资报告"
    sheet.range('A1').font.size = 20
    sheet.range('A1').font.bold = True
    
    # 报告日期
    sheet.range('A3').value = f"报告月份: {datetime.now().strftime('%Y-%m')}"
    
    # 组合概况
    sheet.range('A5').value = "一、组合概况"
    sheet.range('A5').font.bold = True
    sheet.range('A5').font.size = 14
    
    portfolio_data = [
        ['指标', '数值', '说明'],
        ['期初价值', '100万', '假设'],
        ['期末价值', '110万', '假设'],
        ['收益率', '10%', '假设'],
        ['最大回撤', '-5%', '假设']
    ]
    sheet.range('A7').value = portfolio_data
    
    # 持仓情况
    sheet.range('A13').value = "二、持仓情况"
    sheet.range('A13').font.bold = True
    sheet.range('A13').font.size = 14
    
    holdings_data = [
        ['股票', '持仓比例', '收益率', '贡献度'],
        ['台积电', '30%', '15%', '4.5%'],
        ['NVIDIA', '25%', '20%', '5.0%'],
        ['AMD', '15%', '10%', '1.5%'],
        ['中芯国际', '10%', '-5%', '-0.5%'],
        ['欣兴电子', '10%', '12%', '1.2%'],
        ['现金', '10%', '0%', '0%']
    ]
    sheet.range('A15').value = holdings_data
    
    # 市场展望
    sheet.range('A22').value = "三、市场展望"
    sheet.range('A22').font.bold = True
    sheet.range('A22').font.size = 14
    
    outlook = [
        ['宏观环境', '美联储加息周期接近尾声，流动性改善'],
        ['行业机会', 'AI 需求持续旺盛，先进封装产能紧缺'],
        ['风险因素', '地缘政治风险，宏观经济下行'],
        ['配置建议', '增持 AI 相关，减仓周期性股票']
    ]
    sheet.range('A24').value = outlook
    
    # 设置格式
    sheet.range('A:G').columns.autofit()
    
    # 添加边框
    sheet.range('A7:D12').api.Borders.LineStyle = 1
    sheet.range('A15:D21').api.Borders.LineStyle = 1
    
    # 保存
    filename = f"月度投资报告_{datetime.now().strftime('%Y%m')}.xlsx"
    wb.save(filename)
    wb.close()
    
    return filename

# 生成报告
generate_monthly_report()
```

---

## 五、学习要点总结

### 5.1 VBA vs xlwings

| 特性 | VBA | xlwings |
|------|-----|---------|
| **安装** | 无需 | 需安装 |
| **学习曲线** | 中 | 中 |
| **灵活性** | 低 | 高 |
| **数据处理** | 弱 | 强（pandas） |
| **可视化** | 一般 | 强 |
| **部署** | Excel 内 | Python 环境 |
| **适用场景** | 简单任务 | 复杂任务 |

### 5.2 常用操作

| 操作 | VBA | xlwings |
|------|-----|---------|
| **打开文件** | Workbooks.Open | xw.books.open() |
| **读取单元格** | Range("A1").Value | sheet.range('A1').value |
| **写入单元格** | Range("A1").Value = x | sheet.range('A1').value = x |
| **循环** | For...Next | for...in |
| **条件** | If...Then | if...elif...else |
| **创建图表** | Charts.Add | sheet.charts.add() |
| **保存** | Workbook.Save | wb.save() |

### 5.3 最佳实践

1. **模板化**：建立标准报告模板
2. **参数化**：使用变量控制输出
3. **错误处理**：添加错误捕获
4. **日志记录**：记录执行过程
5. **自动化调度**：结合 Windows 任务计划程序

---

## 六、延伸学习

### 6.1 推荐研究

1. VBA 高级应用
2. xlwings 官方文档
3. Excel 插件开发
4. 自动化调度

### 6.2 待实践

1. 建立投资报告模板
2. 自动化财务数据更新
3. 生成 K 线图报告
4. 设置定时任务

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*

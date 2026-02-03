# 机器学习入门：scikit-learn 实战
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、机器学习概述

### 1.1 机器学习分类

```
机器学习

├── 监督学习（有标签数据）
│   ├── 分类（Classification）
│   │   ├── 逻辑回归
│   │   ├── 决策树
│   │   ├── 随机森林
│   │   ├── 支持向量机
│   │   └── 神经网络
│   │
│   └── 回归（Regression）
│       ├── 线性回归
│       ├── 岭回归
│       ├── 决策树回归
│       └── 随机森林回归
│
├── 无监督学习（无标签数据）
│   ├── 聚类（Clustering）
│   │   ├── K-Means
│   │   ├── DBSCAN
│   │   └── 层次聚类
│   │
│   └── 降维（Dimensionality Reduction）
│       ├── PCA
│       └── t-SNE
│
└── 强化学习（Reward 驱动）
    ├── Q-Learning
    └── Deep Q-Network
```

### 1.2 机器学习在金融中的应用

| 应用场景 | 算法 | 说明 |
|----------|------|------|
| **股价预测** | 回归/时间序列 | 预测未来价格 |
| **涨跌预测** | 分类 | 预测涨跌方向 |
| **风险评估** | 分类/回归 | 信用评分/风险等级 |
| **异常检测** | 聚类 | 欺诈检测 |
| **资产配置** | 强化学习 | 组合优化 |
| **自然语言处理** | NLP | 财报分析/情绪分析 |

---

## 二、scikit-learn 基础

### 2.1 安装与导入

```python
# 安装
pip install scikit-learn pandas numpy matplotlib

# 导入
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
```

### 2.2 数据准备

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

# 内置数据集
iris = load_iris()
X = iris.data  # 特征
y = iris.target  # 标签

# 自定义数据
df = pd.DataFrame({
    'revenue': np.random.rand(100) * 100,
    'profit': np.random.rand(100) * 20,
    'growth': np.random.rand(100) * 50 - 10,
    'label': np.random.randint(0, 2, 100)  # 0 或 1
})

print(df.head())
```

### 2.3 数据划分

```python
from sklearn.model_selection import train_test_split

# 特征和标签
X = df[['revenue', 'profit', 'growth']]
y = df['label']

# 划分训练集和测试集（80% 训练，20% 测试）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"训练集大小: {X_train.shape[0]}")
print(f"测试集大小: {X_test.shape[0]}")
```

### 2.4 数据标准化

```python
from sklearn.preprocessing import StandardScaler

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"标准化后均值: {X_train_scaled.mean(axis=0)}")
print(f"标准化后标准差: {X_train_scaled.std(axis=0)}")
```

---

## 三、监督学习实战

### 3.1 线性回归（预测股价）

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 生成模拟数据
np.random.seed(42)
n = 100
revenue = np.random.rand(n) * 100 + 50  # 营收
expense = revenue * 0.6 + np.random.randn(n) * 5  # 成本
profit = revenue - expense  # 利润

# 添加一些噪声
noise = np.random.randn(n) * 2
profit_with_noise = profit + noise

# 特征和标签
X = revenue.reshape(-1, 1)
y = profit_with_noise

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建模型
model = LinearRegression()

# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"均方误差 (MSE): {mse:.2f}")
print(f"R² 分数: {r2:.4f}")
print(f"斜率: {model.coef_[0]:.4f}")
print(f"截距: {model.intercept_:.4f}")

# 可视化
plt.scatter(X_test, y_test, color='blue', label='实际值')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='预测值')
plt.xlabel('营收')
plt.ylabel('利润')
plt.legend()
plt.title('线性回归：营收预测利润')
plt.show()
```

### 3.2 逻辑回归（预测涨跌）

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# 生成模拟数据
np.random.seed(42)
n = 1000

# 特征
pe = np.random.rand(n) * 50 + 10  # P/E: 10-60
pb = np.random.rand(n) * 5 + 1  # P/B: 1-6
roe = np.random.rand(n) * 30 + 5  # ROE: 5-35
growth = np.random.rand(n) * 40 - 10  # 增长率: -10-30

# 标签：PE 低 + ROE 高 = 上涨
prob = (1 / (1 + np.exp(-(0.1 * (30 - pe) + 0.2 * roe + 0.05 * growth))))
label = (np.random.rand(n) < prob).astype(int)

# 创建 DataFrame
df = pd.DataFrame({
    'PE': pe,
    'PB': pb,
    'ROE': roe,
    'growth': growth,
    'label': label
})

# 特征和标签
X = df[['PE', 'PB', 'ROE', 'growth']]
y = df['label']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建模型
model = LogisticRegression(random_state=42)

# 训练模型
model.fit(X_train_scaled, y_train)

# 预测
y_pred = model.predict(X_test_scaled)

# 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率: {accuracy:.4f}")
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=['下跌', '上涨']))

# 特征重要性
print("\n特征系数:")
for feature, coef in zip(X.columns, model.coef_[0]):
    print(f"  {feature}: {coef:.4f}")
```

### 3.3 随机森林（分类任务）

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification

# 生成模拟数据
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林模型
model = RandomForestClassifier(
    n_estimators=100,  # 树的数量
    max_depth=10,      # 最大深度
    random_state=42
)

# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率: {accuracy:.4f}")

# 特征重要性
feature_importance = pd.DataFrame({
    'feature': range(20),
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 重要特征:")
print(feature_importance.head(10))
```

### 3.4 随机森林回归（股价预测）

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import akshare as ak

# 获取真实股票数据
stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                                start_date="20230101", end_date="20231231")
stock_data['日期'] = pd.to_datetime(stock_data['日期'])
stock_data = stock_data.sort_values('日期')

# 创建特征
stock_data['MA5'] = stock_data['收盘'].rolling(5).mean()
stock_data['MA20'] = stock_data['收盘'].rolling(20).mean()
stock_data['RSI'] = stock_data['涨跌幅'].rolling(14).mean()
stock_data['Volume_MA5'] = stock_data['成交量'].rolling(5).mean()

# 创建标签：下一天涨跌
stock_data['target'] = stock_data['收盘'].shift(-1)
stock_data = stock_data.dropna()

# 特征和标签
features = ['收盘', 'MA5', 'MA20', 'RSI', 'Volume_MA5', '涨跌幅']
X = stock_data[features]
y = stock_data['target']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建模型
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"均方误差 (MSE): {mse:.2f}")
print(f"R² 分数: {r2:.4f}")

# 特征重要性
print("\n特征重要性:")
for feature, importance in zip(features, model.feature_importances_):
    print(f"  {feature}: {importance:.4f}")
```

---

## 四、模型评估与优化

### 4.1 交叉验证

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# 生成数据
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

# 创建模型
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 5 折交叉验证
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"交叉验证分数: {scores}")
print(f"平均准确率: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
```

### 4.2 网格搜索

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# 定义参数网格
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

# 创建模型
model = RandomForestClassifier(random_state=42)

# 网格搜索
grid_search = GridSearchCV(
    model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
)

# 拟合
grid_search.fit(X, y)

print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳分数: {grid_search.best_score_:.4f}")
```

### 4.3 模型评估指标

```python
from sklearn.metrics import (
    accuracy_score,      # 准确率
    precision_score,     # 精确率
    recall_score,        # 召回率
    f1_score,            # F1 分数
    confusion_matrix,    # 混淆矩阵
    roc_auc_score,       # AUC 分数
    mean_squared_error,  # 均方误差
    r2_score             # R² 分数
)
```

---

## 五、实战案例：股票涨跌预测

### 5.1 完整流程

```python
import pandas as pd
import numpy as np
import akshare as ak
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# 1. 获取数据
stock_data = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                                start_date="20230101", end_date="20231231")
stock_data['日期'] = pd.to_datetime(stock_data['日期'])
stock_data = stock_data.sort_values('日期')

# 2. 特征工程
stock_data['MA5'] = stock_data['收盘'].rolling(5).mean()
stock_data['MA20'] = stock_data['收盘'].rolling(20).mean()
stock_data['MA5_MA20_ratio'] = stock_data['MA5'] / stock_data['MA20']
stock_data['volatility'] = stock_data['最高'] - stock_data['最低']
stock_data['volume_ratio'] = stock_data['成交量'] / stock_data['成交量'].rolling(5).mean()

# RSI 计算
delta = stock_data['收盘'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
stock_data['RSI'] = 100 - (100 / (1 + rs))

# MACD 计算
ema12 = stock_data['收盘'].ewm(span=12, adjust=False).mean()
ema26 = stock_data['收盘'].ewm(span=26, adjust=False).mean()
stock_data['MACD'] = ema12 - ema26
stock_data['Signal'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()

# 创建标签：下一天涨跌
stock_data['target'] = (stock_data['收盘'].shift(-1) > stock_data['收盘']).astype(int)

# 3. 数据清洗
features = ['收盘', 'MA5', 'MA20', 'MA5_MA20_ratio', 'volatility', 
            'volume_ratio', 'RSI', 'MACD', 'Signal']
stock_data = stock_data.dropna()
X = stock_data[features]
y = stock_data['target']

# 4. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. 训练模型
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train_scaled, y_train)

# 7. 预测
y_pred = model.predict(X_test_scaled)

# 8. 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率: {accuracy:.4f}")
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=['下跌', '上涨']))

# 9. 特征重要性
print("\n特征重要性:")
for feature, importance in sorted(zip(features, model.feature_importances_), 
                                   key=lambda x: x[1], reverse=True):
    print(f"  {feature}: {importance:.4f}")

# 10. 可视化
plt.figure(figsize=(12, 4))
plt.bar(features, model.feature_importances_)
plt.xticks(rotation=45)
plt.title('特征重要性')
plt.tight_layout()
plt.show()
```

---

## 六、学习要点总结

### 6.1 常用算法

| 算法 | 类型 | 适用场景 | 优点 | 缺点 |
|------|------|----------|------|------|
| **线性回归** | 回归 | 连续值预测 | 简单、可解释 | 假设线性 |
| **逻辑回归** | 分类 | 二分类 | 可解释、快 | 假设线性 |
| **随机森林** | 分类/回归 | 通用 | 准确、抗过拟合 | 慢、难解释 |
| **SVM** | 分类 | 高维数据 | 准确、泛化强 | 慢、调参难 |
| **神经网络** | 分类/回归 | 复杂模式 | 强大、灵活 | 需要大数据 |

### 6.2 机器学习流程

```
1. 数据收集 → 2. 数据清洗 → 3. 特征工程
       ↓              ↓              ↓
4. 数据划分 → 5. 模型训练 → 6. 模型评估
       ↓              ↓              ↓
7. 参数调优 → 8. 模型部署 → 9. 持续监控
```

### 6.3 注意事项

| 注意事项 | 说明 |
|----------|------|
| **数据质量** | 垃圾进，垃圾出 |
| **特征工程** | 特征比模型更重要 |
| **过拟合** | 使用交叉验证、正则化 |
| **数据泄露** | 测试集不能参与训练 |
| **可解释性** | 金融领域需要可解释 |

---

## 七、延伸学习

### 7.1 推荐研究

1. 深度学习（PyTorch/TensorFlow）
2. 时间序列预测（LSTM/GRU）
3. 自然语言处理（BERT/GPT）
4. 强化学习（交易策略）

### 7.2 待实践

1. 用真实股票数据预测股价
2. 使用 LSTM 进行时间序列预测
3. 构建完整的量化交易系统
4. 开发基于 NLP 的舆情分析系统

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*

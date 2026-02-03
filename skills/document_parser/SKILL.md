# 文档解析技能

> 读取并解析 Word (docx)、PDF 等文档

## 技能说明

本技能用于解析用户发送的文档文件，自动提取文字内容并保存。

## 使用场景

- 用户发送 docx 文件时自动解析
- 用户发送 PDF 文件时自动提取内容
- 批量处理多个文档

## 依赖安装

```bash
pip install python-docx PyPDF2 pdfplumber
```

## 核心能力

### 1. 读取 docx 文档

```python
import zipfile
import re

def read_docx(file_path):
    # 解压 docx (本质是 zip 压缩包)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('/tmp/docx_extract')
    
    # 读取主内容 document.xml
    xml_path = '/tmp/docx_extract/word/document.xml'
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 清理 XML 标签，只保留文字
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

### 2. 读取 PDF 文档

```python
import pdfplumber

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
```

### 3. 自动识别文件类型

```python
import os

def read_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.docx':
        return read_docx(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "不支持的文件格式"
```

## 自动化处理流程

### 当收到 docx 文件时

1. **接收文件路径**
   ```
   /Users/dave/.openclaw/media/inbound/{uuid}.docx
   ```

2. **解析内容**
   ```
   - 解压 docx (zip 格式)
   - 读取 word/document.xml
   - 清理 XML 标签
   - 提取纯文字
   ```

3. **保存到公司档案**
   ```
   /Users/dave/clawd/companies/{公司名}.md
   ```

4. **更新长期记忆**
   ```
   - 添加到 MEMORY.md
   - 更新 INDEX.md
   ```

## 文件命名规范

| 文件类型 | 命名模板 |
|---------|---------|
| 公司档案 | `/Users/dave/clawd/companies/{公司名}.md` |
| 产品介绍 | `/Users/dave/clawd/companies/{公司名}_产品介绍.md` |
| 会议记录 | `/Users/dave/clawd/companies/{公司名}_会议_{日期}.md` |

## 注意事项

1. **docx 是压缩文件** - 本质是 zip 格式，包含 XML 文件
2. **编码问题** - 优先使用 UTF-8
3. **图片提取** - 需要额外处理 image 标签
4. **表格处理** - 需要解析 table 相关 XML

## 当前实现状态

| 能力 | 状态 | 说明 |
|-----|------|------|
| 读取 docx | ✅ 已实现 | Python zipfile 解析 |
| 读取 PDF | ⚠️ 需安装 | 需要 pdfplumber 库 |
| 自动保存 | ✅ 已实现 | 保存到 companies/ 目录 |
| 更新记忆 | ✅ 已实现 | 更新 MEMORY.md |

## 示例：解析礼鼎半导体介绍

```python
# 输入文件
file_path = "/Users/dave/.openclaw/media/inbound/7e88521f-398c-4341-bd8a-9f2b13cb7d1a.docx"

# 解析结果
text = read_docx(file_path)
# 输出: "礼鼎半导体高端 IC 芯片 ABF 先进封装载板介绍..."
# 长度: 2038 字

# 保存
save_company_profile("礼鼎半导体", text)
# 文件: /Users/dave/clawd/companies/礼鼎半导体.md
```

---

**创建时间**: 2026-02-02
**版本**: V1.0
**维护者**: Clawdbot

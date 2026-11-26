# arXiv 每日论文推送

🤖 每天自动从 arXiv 获取你指定领域的最新论文，使用 DeepSeek AI 生成中文/英文/双语摘要，并推送到你的邮箱。

中文文档 | [English](./README_EN.md)

## ✨ 功能特点

- 📚 **智能论文选择**：从配置的 4 个 arXiv 分类获取最新论文
- 🎯 **领域平衡**：确保每个研究领域都有代表性论文
- 🏆 **质量筛选**：基于多个质量指标对论文评分
- 🔄 **智能去重**：自动检测并移除相似论文
- 🤖 **AI 智能摘要**：使用 DeepSeek V3.2 生成高质量中文摘要
- 📧 **邮件推送**：精美的 HTML 邮件格式，包含日期提醒和质量徽章
- ⏰ **自动定时**：通过 GitHub Actions 自动运行
- 🆓 **完全免费**：所有服务都在免费额度内

## 🚀 快速开始

### 1. Fork 或克隆此仓库

```bash
git clone https://github.com/RunRiotComeOn/arXiv-Daily-Summarizer.git
cd arxiv-daily-summarizer
```

### 2. 配置 GitHub Secrets

在你的 GitHub 仓库中，进入 **Settings → Secrets and variables → Actions → New repository secret**，添加以下密钥：

| 密钥名称 | 说明 | 示例 |
|---------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `SENDER_EMAIL` | 发件人邮箱地址 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | 邮箱应用专用密码 | `abcd efgh ijkl mnop` |
| `RECEIVER_EMAIL` | 单个邮箱或多个邮箱组成的 JSON 数组 | `["alice@example.com","bob@example.com"]` |
| `SMTP_SERVER` | SMTP 服务器地址（GitHub Actions 必填） | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口（GitHub Actions 必填） | `587` |

#### Api 配置说明
使用 DeepSeek 官方 API 和 `deepseek-flash` 模型，通过 `DEEPSEEK_API_KEY` 设置密钥。

#### 📮 邮箱配置说明

**Gmail 用户：**
1. 前往 [Google 账号安全设置](https://myaccount.google.com/security)
2. 开启"两步验证"
3. 生成"应用专用密码"
4. 选择"邮件"和"其他设备"
5. 使用生成的 16 位密码作为 `SENDER_PASSWORD`

**QQ 邮箱用户：**
1. 登录 QQ 邮箱，进入"设置 → 账户"
2. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
3. 开启"IMAP/SMTP服务"
4. 获取授权码作为 `SENDER_PASSWORD`
5. `SMTP_SERVER` 设置为 `smtp.qq.com`

**163 邮箱用户：**
1. 登录 163 邮箱，进入"设置 → POP3/SMTP/IMAP"
2. 开启"IMAP/SMTP服务"
3. 获取授权码
4. `SMTP_SERVER` 设置为 `smtp.163.com`

### 3. 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 点击 "I understand my workflows, go ahead and enable them"
3. 首次运行可以点击 "Run workflow" 手动触发测试

### 4. 等待每日推送

系统会在每天北京时间早上 7:00 自动运行（可在 `.github/workflows/daily_arxiv.yml` 中修改时间）。

## 🛠️ 自定义配置

### 修改关注领域

直接编辑 `fetch_papers.py` 中的 `CATEGORIES`。默认配置如下，可从下表选择其他分类。

```python
CATEGORIES = ['cs.CV', 'cs.CL', 'cs.MA', 'cs.LG']
```

| 分类代码 | 研究方向 |
| --- | --- |
| `cs.AI` | 人工智能 |
| `cs.CV` | 计算机视觉与模式识别 |
| `cs.CL` | 计算与语言（自然语言处理） |
| `cs.LG` | 机器学习 |
| `cs.NE` | 神经与进化计算 |
| `cs.MA` | 多智能体系统 |
| `cs.RO` | 机器人学 |
| `cs.SE` | 软件工程 |
| `cs.PL` | 编程语言 |
| `cs.DB` | 数据库 |
| `cs.IR` | 信息检索 |
| `cs.DC` | 分布式、并行与集群计算 |
| `cs.OS` | 操作系统 |
| `cs.DS` | 数据结构与算法 |
| `cs.HC` | 人机交互 |
| `cs.CR` | 密码学与安全 |
| `cs.NI` | 网络与互联网架构 |

仅收录原文 PDF 提供本工作 GitHub 仓库的论文。垂直领域筛选规则在 [筛选提示词](screening_prompt.txt) 中维护。

### 修改论文数量

编辑 `fetch_papers.py` 中的 `MAX_RESULTS` 变量：

```python
MAX_RESULTS = 20  # 每天推送的论文数量
```

### 修改领域平衡策略

编辑 `MIN_PAPERS_PER_CATEGORY` 变量：

```python
MIN_PAPERS_PER_CATEGORY = 1  # 每个领域至少保证的论文数
```

### 修改推送时间

编辑 `.github/workflows/daily_arxiv.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 23 * * *'  # UTC 时间，北京时间需要加 8 小时
```

常用时间参考：
- `'0 23 * * *'` - 北京时间 07:00
- `'0 1 * * *'` - 北京时间 09:00
- `'0 12 * * *'` - 北京时间 20:00

### 调整质量筛选

修改 `fetch_papers.py` 中的阈值：

```python
MIN_ABSTRACT_LENGTH = 100  # 最小摘要长度
SIMILARITY_THRESHOLD = 0.85  # 去重相似度阈值（0-1）
```

## 📁 项目结构

```
arxiv-daily-summarizer/
├── .github/
│   └── workflows/
│       └── daily_arxiv.yml    # GitHub Actions 工作流配置
├── fetch_papers.py            # 主程序脚本（包含质量筛选）
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量示例
├── README.md                 # 英文文档
└── README_CN.md              # 中文文档
```

## 🔧 本地测试

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量（Windows PowerShell）
$env:DEEPSEEK_API_KEY="your-api-key"
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="your-password"
$env:RECEIVER_EMAIL="receiver@example.com"

# 或使用 .env 文件（Unix/Linux/Mac）
cp .env.example .env
# 编辑 .env 填入你的配置
export $(cat .env | xargs)

# 3. 运行脚本
python fetch_papers.py

# 4. 如果你需要测试 arXiv 可达性
python test_arxiv.py
```

## 📊 质量评分系统

论文根据以下因素评分：

1. **摘要长度**：更长的摘要通常表示更详细的工作（+0-2 分）
2. **作者数量**：合作研究获得加分（+0-1 分）
3. **标题关键词**：包含 "novel"、"efficient"、"transformer" 等重要术语（每个 +0.5 分）
4. **时效性**：越新的论文分数越高（+0.5-3 分）
5. **标题质量**：适当的长度和结构

高质量论文（评分 ≥ 5.0）会在邮件中显示 ⭐ 徽章。

## 🔍 智能去重机制

系统通过以下方式检测相似论文：
- 使用序列匹配算法计算标题相似度
- 移除相似度 >85% 的重复论文
- 发现重复时保留质量分数更高的版本

## ⚖️ 领域平衡算法

1. **保证最小值**：每个领域至少获得 1 篇论文
2. **质量填充**：剩余名额由所有领域中评分最高的论文填充
3. **最终排序**：按发布日期排序（最新的在前）

## 📊 使用限制

- **GitHub Actions**：每月 2000 分钟免费额度（本项目每天约消耗 2-3 分钟）
- **DeepSeek API**：按 DeepSeek 官方账户计费
- **邮件发送**：取决于你的邮箱服务商限制

## ❓ 常见问题

**Q: 为什么没有收到邮件？**
- 检查 GitHub Actions 运行日志，查看是否有错误
- 确认所有 Secrets 配置正确
- 检查垃圾邮件文件夹
- 确认邮箱服务的 SMTP 设置正确

**Q: 如何修改邮件样式？**
- 编辑 `fetch_papers.py` 中的 `generate_email_content()` 函数
- 修改 HTML 和 CSS 代码即可

**Q: 可以推送到微信或 Telegram 吗？**
- 可以！修改 `send_email()` 函数，替换为对应平台的 API 即可

**Q: 为什么有些论文是好几天前的？**
- arXiv 按时间表发布论文，不是连续的
- 系统会在论文较旧时显示日期提醒
- 如果想要更严格的时效性，可以调整 `MIN_PAPERS_PER_CATEGORY`

**Q: 如何提高论文质量？**
- 增加 `MIN_ABSTRACT_LENGTH` 阈值
- 在 `calculate_paper_quality_score()` 中添加更多质量关键词
- 提高质量分数筛选阈值

## 📝 许可证

MIT License

## 🙏 致谢

- [arXiv](https://arxiv.org/) - 提供开放的学术论文库
- [DeepSeek](https://www.deepseek.com/) - 提供强大的 AI 模型
- [GitHub Actions](https://github.com/features/actions) - 提供免费的自动化服务

---

⭐ 如果这个项目对你有帮助，欢迎 Star！

## 🔄 更新日志

### v2.0 - 增强质量与智能
- ✅ 添加质量评分系统
- ✅ 实现智能去重功能
- ✅ 确保领域平衡
- ✅ 添加高质量论文徽章
- ✅ 改进日期提醒
- ✅ 完整英文文档

### v1.0 - 初始版本
- 基础论文获取和摘要生成
- 邮件推送功能
- GitHub Actions 自动化

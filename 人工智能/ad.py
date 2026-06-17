import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from jieba import analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 确保标准输出编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 加载环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class ArticleSummarizer:
    """文章摘要生成器 - 仅支持 URL 输入"""
    
    def __init__(self):
        # 初始化大模型客户端（使用环境变量中的任意一个可用API）
        self.client = self._init_client()
        
    def _init_client(self):
        """初始化大模型客户端"""
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("DEEPSEEK_API_KEY") or os.getenv("GLM_API_KEY")
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 默认使用阿里云千问
        
        if not api_key:
            raise ValueError("请在 .env 文件中配置至少一个 API Key")
        
        return OpenAI(api_key=api_key, base_url=base_url)
    
    def _fetch_url(self, url):
        """获取网页内容"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取主要内容
            for script in soup(['script', 'style', 'nav', 'footer', 'aside']):
                script.decompose()
            
            # 优先提取 article 或 main 标签
            content = soup.find('article') or soup.find('main') or soup.find('div', class_='article')
            
            if content:
                text = content.get_text(separator='\n', strip=True)
            else:
                # 如果没有找到特定标签，提取所有文本
                text = soup.get_text(separator='\n', strip=True)
            
            return text
        except Exception as e:
            raise ValueError(f"获取网页内容失败: {str(e)}")
    
    def _clean_text(self, text):
        """清理文本：去HTML标签、分段、清理空行"""
        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 去除多余空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 分段处理
        paragraphs = text.split('。')
        paragraphs = [p.strip() + '。' for p in paragraphs if p.strip()]
        
        return '\n\n'.join(paragraphs)
    
    def _extract_keywords(self, text, top_n=10):
        """使用jieba提取关键词"""
        try:
            # 尝试使用停用词文件
            stopwords_path = os.path.join(os.path.dirname(__file__), 'stopwords.txt')
            if os.path.exists(stopwords_path):
                analyse.set_stop_words(stopwords_path)
        except:
            pass
        
        keywords = analyse.extract_tags(text, topK=top_n, withWeight=True)
        return [(word, weight) for word, weight in keywords]
    
    def _generate_summary(self, text, summary_type):
        """调用大模型生成摘要"""
        prompts = {
            'short': f"""请用一句话概括以下文章的核心观点：\n\n{text[:3000]}""",
            'standard': f"""请用3-5句话概括以下文章，保留关键论据：\n\n{text[:3000]}""",
            'detailed': f"""请对以下文章进行Q&A分析，提炼3个核心问题并给出详细答案：\n\n{text[:3000]}"""
        }
        
        prompt = prompts.get(summary_type, prompts['standard'])
        
        try:
            response = self.client.chat.completions.create(
                model="qwen-plus",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"生成摘要失败: {str(e)}"
    
    def _generate_wordcloud(self, text, output_path='wordcloud.png'):
        """生成词云"""
        keywords = self._extract_keywords(text, top_n=50)
        word_freq = {word: weight * 1000 for word, weight in keywords}
        
        # 尝试使用系统字体
        font_paths = [
            'msyh.ttc',  # 微软雅黑
            'SimHei.ttf',  # 黑体
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
        ]
        
        font_path = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_path = fp
                break
        
        if not font_path:
            print(" 未找到中文字体，词云可能无法正确显示中文")
        
        wc = WordCloud(
            font_path=font_path,
            width=800,
            height=600,
            background_color='white',
            max_words=50,
            scale=2
        )
        
        wc.generate_from_frequencies(word_freq)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def summarize(self, url):
        """主函数：处理 URL 并生成摘要"""
        print(" 正在获取网页内容...")
        
        # 1. 获取网页内容
        print(f" URL: {url}")
        raw_text = self._fetch_url(url)
        
        # 2. 预处理文本
        print(" 正在清理文本...")
        clean_text = self._clean_text(raw_text)
        
        # 3. 提取关键词
        print(" 正在提取关键词...")
        keywords = self._extract_keywords(clean_text)
        
        # 4. 生成三种摘要
        print("正在生成摘要...")
        short_summary = self._generate_summary(clean_text, 'short')
        standard_summary = self._generate_summary(clean_text, 'standard')
        detailed_summary = self._generate_summary(clean_text, 'detailed')
        
        # 5. 生成词云
        print(" 正在生成词云...")
        timestamp = url.replace('https://', '').replace('http://', '').replace('/', '_')[:20]
        wordcloud_path = f"wordcloud_{timestamp}.png"
        self._generate_wordcloud(clean_text, wordcloud_path)
        
        # 6. 输出到文件
        print(" 正在保存结果...")
        output_path = self._save_output(
            url,
            clean_text,
            keywords,
            short_summary,
            standard_summary,
            detailed_summary,
            wordcloud_path
        )
        
        print(f" 完成！结果已保存到 {output_path}")
        
        return {
            'keywords': keywords,
            'short_summary': short_summary,
            'standard_summary': standard_summary,
            'detailed_summary': detailed_summary,
            'wordcloud_path': wordcloud_path,
            'output_path': output_path
        }
    
    def _save_output(self, source, text, keywords, short, standard, detailed, wordcloud_path):
        """保存输出到 Markdown 文件"""
        timestamp = source.replace('https://', '').replace('http://', '').replace('/', '_')[:20]
        output_path = f"summary_{timestamp}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"""# 文章摘要报告

##  来源
[{source}]({source})

## 基本信息
- 原文字数：{len(text)} 字
- 关键词数量：{len(keywords)} 个

##  Top 10 关键词
| 关键词 | 权重 |
|--------|------|
""")
            for word, weight in keywords[:10]:
                f.write(f"| {word} | {weight:.4f} |\n")
            
            f.write(f"""
##  摘要

### 简短版（一句话概括）
{short}

### 标准版（3-5句话）
{standard}

### 详细版（Q&A格式）
{detailed}

##  词云图
![词云]({wordcloud_path})

---
*生成时间：{timestamp}*
""")
        
        return output_path

def main():
    """交互式主函数"""
    print("="*50)
    print("     文章摘要生成器 v1.0")
    print("="*50)
    print("支持输入：网页 URL")
    print("="*50)
    
    url = input("请输入网页 URL：").strip()
    
    if not url:
        print("❌ URL 不能为空！")
        return
    
    # 验证 URL 格式
    if not (url.startswith('http://') or url.startswith('https://')):
        print("❌ 请输入有效的 URL（以 http:// 或 https:// 开头）")
        return
    
    try:
        summarizer = ArticleSummarizer()
        result = summarizer.summarize(url)
        
        print("\n" + "="*50)
        print(" 摘要预览")
        print("="*50)
        print("\n【简短版】")
        print(result['short_summary'])
        print("\n【关键词】")
        print(", ".join([word for word, _ in result['keywords'][:10]]))
        
    except Exception as e:
        print(f"\n 处理失败: {str(e)}")

if __name__ == "__main__":
    main()
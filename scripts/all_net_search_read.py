#!/usr/bin/env python3
"""
全网搜读 - 主入口
整合 Agent Reach 能力，提供全网搜索+内容提取功能
"""

import sys
import os
import json
import subprocess
import re
from typing import List, Dict, Optional

# 配置目录
CONFIG_DIR = os.path.expanduser("~/.all-net-search-read")
DATA_DIR = os.path.join(CONFIG_DIR, "data")

class AllNetSearchRead:
    """全网搜读主类"""
    
    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        self.history_file = os.path.join(DATA_DIR, "history.json")
        self.favorites_file = os.path.join(DATA_DIR, "favorites.json")
        self.monitors_file = os.path.join(DATA_DIR, "monitors.json")
        
        # 加载数据
        self.history = self._load_json(self.history_file, [])
        self.favorites = self._load_json(self.favorites_file, [])
        self.monitors = self._load_json(self.monitors_file, [])
    
    def _load_json(self, path: str, default):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return default
    
    def _save_json(self, path: str, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def check_agent_reach_update(self) -> Dict:
        """检查 Agent Reach 更新"""
        try:
            result = subprocess.run(
                ["agent-reach", "check-update"],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            
            if "已是最新版本" in output:
                return {
                    "status": "up_to_date",
                    "message": output.strip(),
                    "need_update": False
                }
            else:
                return {
                    "status": "update_available",
                    "message": output.strip(),
                    "need_update": True
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "need_update": None
            }
    
    def search(self, query: str, platform: str = None) -> str:
        """全网搜索"""
        if platform:
            # 特定平台搜索
            cmd = self._get_platform_cmd(platform, query)
        else:
            # 默认使用 Agent Reach 搜索
            cmd = ["xreach", "search", query, "--json"]
        
        return self._run_command(cmd)
    
    def _get_platform_cmd(self, platform: str, query: str) -> List[str]:
        """获取平台特定命令"""
        platform_map = {
            "twitter": ["xreach", "search", f"@{query}"],
            "推特": ["xreach", "search", f"@{query}"],
            "x": ["xreach", "search", f"@{query}"],
            "小红书": ["xreach", "search", f"site:xiaohongshu.com {query}"],
            "b站": ["xreach", "site", "bilibili.com", query],
            "bilibili": ["xreach", "site", "bilibili.com", query],
            "youtube": ["xreach", "site", "youtube.com", query],
            "reddit": ["xreach", "search", f"site:reddit.com {query}"],
            "公众号": ["xreach", "search", f"site:weixin.qq.com {query}"],
            "微信": ["xreach", "search", f"site:weixin.qq.com {query}"],
        }
        return platform_map.get(platform.lower(), ["xreach", "search", query])
    
    def read_url(self, url: str) -> str:
        """读取网页内容"""
        # 优先使用 r.jina.ai 提取
        jina_url = f"https://r.jina.ai/{url}"
        
        cmd = ["curl", "-s", jina_url]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.stdout and len(result.stdout) > 100:
                return result.stdout
        except:
            pass
        
        # 备用：使用 xread
        cmd = ["xread", url]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout or result.stderr
        except Exception as e:
            return f"读取失败: {str(e)}"
    
    def summarize(self, content: str = None, url: str = None) -> str:
        """内容摘要"""
        if url:
            content = self.read_url(url)
        
        if not content:
            return "请提供内容或链接"
        
        # 简单摘要：取前500字 + 关键句
        lines = content.split('\n')
        key_lines = [l for l in lines if l.strip() and len(l) > 20][:5]
        
        summary = f"📝 内容摘要：\n\n"
        summary += content[:500] + "..." if len(content) > 500 else content
        summary += "\n\n🔑 关键要点：\n"
        for i, line in enumerate(key_lines, 1):
            summary += f"{i}. {line[:100]}\n"
        
        return summary
    
    def extract_keywords(self, content: str = None, url: str = None) -> str:
        """关键词提取"""
        if url:
            content = self.read_url(url)
        
        if not content:
            return "请提供内容或链接"
        
        # 简单关键词提取：提取英文单词和中文术语
        import re
        
        # 提取英文术语（连续大写字母）
        english_terms = re.findall(r'\b[A-Z]{2,}\b', content)
        # 提取中文术语（可能的关键概念）
        chinese_terms = re.findall(r'[\u4e00-\u9fa5]{2,6}(?:算法|模型|系统|技术|框架|工具|平台|应用|研究|学习|网络|模型)', content)
        
        # 去重
        english_terms = list(set(english_terms))[:10]
        chinese_terms = list(set(chinese_terms))[:10]
        
        result = "🏷️ 关键词提取：\n\n"
        if english_terms:
            result += "**英文术语**: " + ", ".join(english_terms) + "\n"
        if chinese_terms:
            result += "**中文术语**: " + ", ".join(chinese_terms) + "\n"
        
        if not english_terms and not chinese_terms:
            result += "未能提取到关键词"
        
        return result
    
    def add_to_history(self, query: str, results: List[Dict]):
        """添加到历史记录"""
        from datetime import datetime
        record = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "result_count": len(results)
        }
        self.history.insert(0, record)
        self.history = self.history[:100]  # 保留最近100条
        self._save_json(self.history_file, self.history)
    
    def get_history(self) -> str:
        """获取历史记录"""
        if not self.history:
            return "暂无搜索历史"
        
        lines = ["🕐 搜索历史：\n"]
        for i, record in enumerate(self.history[:20], 1):
            lines.append(f"{i}. {record['query']} ({record['result_count']}结果) - {record['timestamp'][:10]}")
        
        return "\n".join(lines)
    
    def add_to_favorites(self, item: Dict) -> str:
        """添加到收藏"""
        from datetime import datetime
        item['saved_at'] = datetime.now().isoformat()
        self.favorites.insert(0, item)
        self._save_json(self.favorites_file, self.favorites)
        return "✅ 已收藏"
    
    def get_favorites(self) -> str:
        """获取收藏"""
        if not self.favorites:
            return "暂无收藏"
        
        lines = ["📚 我的收藏：\n"]
        for i, item in enumerate(self.favorites[:20], 1):
            title = item.get('title', item.get('query', '未知'))
            lines.append(f"{i}. {title}")
        
        return "\n".join(lines)
    
    def add_monitor(self, keyword: str, freq: str = "daily") -> str:
        """添加监控"""
        from datetime import datetime
        monitor = {
            "keyword": keyword,
            "frequency": freq,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        self.monitors.append(monitor)
        self._save_json(self.monitors_file, self.monitors)
        return f"✅ 已添加监控: {keyword} ({freq})"
    
    def get_monitors(self) -> str:
        """获取监控列表"""
        if not self.monitors:
            return "暂无监控"
        
        lines = ["🔔 定时监控：\n"]
        for i, m in enumerate(self.monitors, 1):
            status = "✅" if m.get('enabled') else "⏸️"
            lines.append(f"{i}. {status} {m['keyword']} - {m['frequency']}")
        
        return "\n".join(lines)
    
    def _run_command(self, cmd: List[str]) -> str:
        """运行命令"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.stdout or result.stderr
        except subprocess.TimeoutExpired:
            return "⏱️ 命令超时"
        except Exception as e:
            return f"❌ 执行失败: {str(e)}"
    
    def help(self) -> str:
        """帮助信息"""
        return """🕵️ 全网搜读 - 使用指南

🔍 搜索:
  搜 {关键词} - 全网搜索
  小红书 {关键词} - 小红书搜索
  推特 {关键词} - Twitter搜索

📖 内容:
  {网址} - 网页脱水/读取
  总结 {网址/内容} - 内容摘要
  提取关键词 {网址/内容} - 关键词提取

📚 管理:
  我的收藏 - 查看收藏
  收藏这个 - 收藏当前内容
  搜索历史 - 查看历史
  监控 {关键词} - 添加监控

🔄 工具:
  检测更新 - 检查 Agent Reach 更新
"""
    
    def process(self, query: str) -> str:
        """处理用户请求"""
        query = query.strip()
        
        # 帮助
        if query in ['帮助', 'help', '?']:
            return self.help()
        
        # 检测更新
        if '检测更新' in query or '检查更新' in query:
            result = self.check_agent_reach_update()
            if result['need_update'] == False:
                return f"✅ Agent Reach 已是最新版本\n\n{result['message']}"
            elif result['need_update'] == True:
                return f"⚠️ 有新版本可用！\n\n{result['message']}\n\n是否需要我帮你更新？"
            else:
                return f"❌ 检查失败: {result['message']}"
        
        # 历史记录
        if '搜索历史' in query or '我的记录' in query:
            return self.get_history()
        
        # 收藏
        if '我的收藏' in query:
            return self.get_favorites()
        
        # 监控
        if query.startswith('监控'):
            keyword = query[2:].strip()
            if keyword:
                return self.add_monitor(keyword)
            return self.get_monitors()
        
        # 搜索
        if query.startswith('搜') or query.startswith('找'):
            # 提取平台前缀
            platforms = ['小红书', '推特', 'twitter', 'B站', 'bilibili', 'youtube', 'reddit', '公众号', '微信']
            platform = None
            
            for p in platforms:
                if query.startswith(p):
                    platform = p
                    query = query[len(p):].strip()
                    break
            
            return self.search(query, platform)
        
        # 总结
        if query.startswith('总结'):
            content = query[2:].strip()
            if content.startswith('http'):
                return self.summarize(url=content)
            return self.summarize(content=content)
        
        # 关键词提取
        if '提取关键词' in query:
            content = query.replace('提取关键词', '').strip()
            if content.startswith('http'):
                return self.extract_keywords(url=content)
            return self.extract_keywords(content=content)
        
        # 默认：尝试作为URL读取或搜索
        if query.startswith('http'):
            return self.read_url(query)
        else:
            return self.search(query)


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = sys.stdin.read().strip()
    
    if not query:
        print(AllNetSearchRead().help())
        return
    
    app = AllNetSearchRead()
    result = app.process(query)
    print(result)


if __name__ == "__main__":
    main()

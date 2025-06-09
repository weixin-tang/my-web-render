import requests
import json
import time
from typing import Optional, Dict, Any

class WebPageToolTester:
    """网页显示工具测试类"""
    
    def __init__(self, base_url: str = "http://localhost:8008/web-render"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def health_check(self) -> bool:
        """健康检查"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ 服务健康检查通过")
                print(f"响应: {response.json()}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def upload_webpage(self, html_content: str, title: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """上传网页"""
        try:
            data = {
                "html_content": html_content
            }
            if title:
                data["title"] = title
                
            response = self.session.post(
                f"{self.base_url}/api/pages",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ 网页上传成功")
                print(f"页面ID: {result['page_id']}")
                print(f"访问URL: {self.base_url}{result['url']}")
                print(f"消息: {result['message']}")
                return result
            else:
                print(f"❌ 上传失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 上传异常: {e}")
            return None
    
    def get_page_info(self, page_id: str) -> Optional[Dict[str, Any]]:
        """获取页面信息"""
        try:
            response = self.session.get(f"{self.base_url}/api/pages/{page_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 获取页面信息成功")
                print(f"ID: {result['id']}")
                print(f"页面ID: {result['page_id']}")
                print(f"标题: {result['title']}")
                print(f"创建时间: {result['created_at']}")
                print(f"HTML内容长度: {len(result['html_content'])} 字符")
                return result
            else:
                print(f"❌ 获取页面信息失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 获取页面信息异常: {e}")
            return None
    
    def list_all_pages(self, skip: int = 0, limit: int = 100) -> Optional[list]:
        """获取所有页面列表"""
        try:
            params = {"skip": skip, "limit": limit}
            response = self.session.get(f"{self.base_url}/api/pages", params=params)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 获取页面列表成功，共 {len(result)} 个页面")
                for i, page in enumerate(result, 1):
                    print(f"  {i}. ID: {page['page_id']}, 标题: {page['title']}, 创建时间: {page['created_at']}")
                return result
            else:
                print(f"❌ 获取页面列表失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 获取页面列表异常: {e}")
            return None
    
    def view_page(self, page_id: str) -> bool:
        """访问页面（获取HTML内容）"""
        try:
            response = self.session.get(f"{self.base_url}/view/{page_id}")
            
            if response.status_code == 200:
                print(f"✅ 页面访问成功")
                print(f"页面URL: {self.base_url}/view/{page_id}")
                print(f"HTML内容长度: {len(response.text)} 字符")
                print(f"内容预览: {response.text[:200]}...")
                return True
            else:
                print(f"❌ 页面访问失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 页面访问异常: {e}")
            return False
    
    def preview_page(self, page_id: str) -> bool:
        """预览页面（在模板中显示）"""
        try:
            response = self.session.get(f"{self.base_url}/preview/{page_id}")
            
            if response.status_code == 200:
                print(f"✅ 页面预览成功")
                print(f"预览URL: {self.base_url}/preview/{page_id}")
                print(f"预览页面长度: {len(response.text)} 字符")
                return True
            else:
                print(f"❌ 页面预览失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 页面预览异常: {e}")
            return False
    
    def delete_page(self, page_id: str) -> bool:
        """删除页面"""
        try:
            response = self.session.delete(f"{self.base_url}/api/pages/{page_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 页面删除成功")
                print(f"消息: {result['message']}")
                return True
            else:
                print(f"❌ 页面删除失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 页面删除异常: {e}")
            return False
    
    def access_home_page(self) -> bool:
        """访问首页"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                print(f"✅ 首页访问成功")
                print(f"首页URL: {self.base_url}/")
                print(f"页面长度: {len(response.text)} 字符")
                return True
            else:
                print(f"❌ 首页访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 首页访问异常: {e}")
            return False
    
    def access_list_page(self) -> bool:
        """访问列表页面"""
        try:
            response = self.session.get(f"{self.base_url}/list")
            
            if response.status_code == 200:
                print(f"✅ 列表页面访问成功")
                print(f"列表页面URL: {self.base_url}/list")
                print(f"页面长度: {len(response.text)} 字符")
                return True
            else:
                print(f"❌ 列表页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 列表页面访问异常: {e}")
            return False

def run_comprehensive_test():
    """运行综合测试"""
    print("🚀 开始网页显示工具综合测试")
    print("=" * 50)
    
    # 初始化测试器
    tester = WebPageToolTester()
    
    # 1. 健康检查
    print("\n📋 1. 健康检查")
    if not tester.health_check():
        print("❌ 服务未启动，请先启动服务")
        return
    
    # 2. 访问首页
    print("\n📋 2. 访问首页")
    tester.access_home_page()
    
    # 3. 访问列表页面
    print("\n📋 3. 访问列表页面")
    tester.access_list_page()
    
    # 4. 上传测试网页
    print("\n📋 4. 上传测试网页")
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试页面</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { color: #333; text-align: center; }
            .content { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1 class="header">这是一个测试页面</h1>
        <div class="content">
            <p>这是通过API上传的测试网页内容。</p>
            <p>当前时间: <span id="time"></span></p>
            <script>
                document.getElementById('time').textContent = new Date().toLocaleString();
            </script>
        </div>
    </body>
    </html>
    """
    
    upload_result = tester.upload_webpage(test_html, "API测试页面")
    if not upload_result:
        print("❌ 上传失败，终止测试")
        return
    
    page_id = upload_result['page_id']
    
    # 5. 获取页面信息
    print("\n📋 5. 获取页面信息")
    tester.get_page_info(page_id)
    
    # 6. 访问页面
    print("\n📋 6. 访问页面")
    tester.view_page(page_id)
    
    # 7. 预览页面
    print("\n📋 7. 预览页面")
    tester.preview_page(page_id)
    
    # 8. 获取所有页面列表
    print("\n📋 8. 获取所有页面列表")
    tester.list_all_pages()
    
    # 9. 上传第二个测试页面
    print("\n📋 9. 上传第二个测试页面")
    test_html2 = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>第二个测试页面</title>
    </head>
    <body>
        <h1>第二个测试页面</h1>
        <p>这是第二个通过API上传的页面</p>
    </body>
    </html>
    """
    
    upload_result2 = tester.upload_webpage(test_html2, "第二个测试页面")
    if upload_result2:
        page_id2 = upload_result2['page_id']
        
        # 10. 再次获取列表，验证新页面
        print("\n📋 10. 验证新页面已添加")
        tester.list_all_pages()
        
        # 11. 删除第二个页面
        print("\n📋 11. 删除第二个页面")
        tester.delete_page(page_id2)
        
        # 12. 验证删除结果
        print("\n📋 12. 验证删除结果")
        tester.list_all_pages()
    
    print("\n🎉 综合测试完成！")
    print(f"\n📝 测试总结:")
    print(f"   - 第一个测试页面ID: {page_id}")
    print(f"   - 访问链接: {tester.base_url}/view/{page_id}")
    print(f"   - 预览链接: {tester.base_url}/preview/{page_id}")
    print(f"   - 首页: {tester.base_url}/")
    print(f"   - 列表页: {tester.base_url}/list")

if __name__ == "__main__":
    run_comprehensive_test()
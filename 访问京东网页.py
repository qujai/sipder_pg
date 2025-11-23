"""
使用 DrissionPage 模块访问京东网页
"""
from DrissionPage import ChromiumPage
import time

# 创建页面对象
page = ChromiumPage()

# 目标网页URL
url = 'https://pro.jd.com/mall/active/2cqCAHDDWm2f5u5irY4TsPPWHQNj/index.html?babelChannel=ttt14&cu=true&utm_source=baidu-pinzhuan&utm_medium=cpc&utm_campaign=t_288551095_baidupinzhuan&utm_term=0f3d30c8dba7459bb52f2eb5eba8ac7d_0_455802cdbb0543e4832e319e90bf9d9e'

try:
    print("正在访问网页...")
    # 访问网页
    page.get(url)
    print(f"成功访问网页: {url}")
    print(f"当前页面标题: {page.title}")
    
    # 等待页面加载完成
    page.wait.load_start()
    
    print("页面加载完成！")
    
    # 等待页面元素加载
    time.sleep(2)
    
    # 查找并点击"京东首页"链接
    print("正在查找京东首页链接...")
    try:
        # 方法1: 通过文本内容查找
        home_link = page.ele('text:京东首页', timeout=5)
        if home_link:
            print("找到京东首页链接，准备点击...")
            home_link.click()
            print("已点击京东首页链接！")
        else:
            # 方法2: 通过aria-label属性查找
            home_link = page.ele('@aria-label:京东首页', timeout=5)
            if home_link:
                print("通过aria-label找到京东首页链接，准备点击...")
                home_link.click()
                print("已点击京东首页链接！")
            else:
                # 方法3: 通过href属性查找
                home_link = page.ele('@href://www.jd.com', timeout=5)
                if home_link:
                    print("通过href找到京东首页链接，准备点击...")
                    home_link.click()
                    print("已点击京东首页链接！")
                else:
                    print("未找到京东首页链接")
    except Exception as e:
        print(f"查找或点击京东首页链接时出错: {e}")
        # 尝试其他定位方式
        try:
            # 尝试通过XPath查找
            home_link = page.ele('xpath://a[@aria-label="京东首页"]', timeout=3)
            if home_link:
                home_link.click()
                print("已通过XPath定位并点击京东首页链接！")
            else:
                # 尝试通过包含jd.com的href查找
                home_link = page.ele('xpath://a[contains(@href, "jd.com")]', timeout=3)
                if home_link:
                    home_link.click()
                    print("已通过href包含jd.com定位并点击链接！")
        except Exception as e2:
            print(f"无法定位京东首页链接: {e2}")
    
    # 等待页面跳转
    time.sleep(2)
    print("等待页面跳转完成...")
    
    # 检查当前窗口数量和URL
    print(f"当前窗口数量: {len(page.tab_ids)}")
    print(f"当前窗口URL: {page.url}")
    
    # 等待新窗口出现并切换到新窗口
    try:
        print("等待新窗口出现...")
        new_tab = page.wait.new_tab(timeout=5)
        if new_tab:
            print(f"✓ 检测到新窗口")
            print(f"新窗口URL: {new_tab.url}")
            
            # 激活新窗口
            print("切换到新窗口...")
            new_tab.set.activate()
            time.sleep(2)
            
            # 更新page对象指向新窗口
            page = new_tab
            print(f"✓ 已切换到新窗口")
            print(f"当前窗口URL: {page.url}")
        else:
            print("未检测到新窗口，可能在同一窗口跳转")
    except Exception as e:
        print(f"等待新窗口失败: {e}")
        # 如果等待新窗口失败，检查是否有多个窗口
        if len(page.tab_ids) > 1:
            print(f"检测到多个窗口，尝试其他方法切换...")
            try:
                # 尝试使用latest_tab
                latest_tab = page.latest_tab
                if latest_tab:
                    print(f"获取到最新标签页，URL: {latest_tab.url}")
                    latest_tab.set.activate()
                    page = latest_tab
                    time.sleep(2)
                    print(f"✓ 已切换到最新窗口")
                    print(f"当前窗口URL: {page.url}")
            except Exception as e2:
                print(f"切换窗口失败: {e2}")
                # 如果无法切换，直接访问京东首页
                print("无法切换窗口，直接访问京东首页...")
                page.get('https://www.jd.com')
                time.sleep(3)
                print(f"直接访问后的URL: {page.url}")
        else:
            print("只有一个窗口，等待页面跳转...")
            time.sleep(2)
            print(f"当前窗口URL: {page.url}")
    
    # 确认是否在京东首页
    current_url = page.url
    print(f"\n当前页面URL: {current_url}")
    
    # 如果还在活动页面，直接访问首页
    if 'active' in current_url:
        print("⚠️ 检测到仍在活动页面，直接访问京东首页...")
        page.get('https://www.jd.com')
        time.sleep(3)
        final_url = page.url
        print(f"访问后的URL: {final_url}")
    elif 'jd.com' in current_url and 'active' not in current_url:
        print("✓ 确认已在京东首页")
    else:
        print(f"⚠️ 当前URL可能不是京东首页: {current_url}")
    
    # 等待页面完全加载
    print("\n等待页面完全加载...")
    try:
        page.wait.load_complete(timeout=10)
    except:
        pass
    time.sleep(2)
    print(f"页面加载完成，当前URL: {page.url}")
    
    # 尝试滚动到顶部，确保搜索框可见
    try:
        page.scroll.to_top()
        time.sleep(1)
    except:
        pass
    
    # 等待页面元素完全加载，特别是等待input元素出现
    print("\n等待页面元素完全加载...")
    try:
        # 等待input#key元素出现
        page.wait.ele_displayed('xpath://input[@id="key"]', timeout=15)
        print("✓ 确认input#key元素已出现在页面上")
        print(f"当前页面URL: {page.url}")
    except Exception as e:
        print(f"⚠️ 等待input#key元素超时: {e}")
        print(f"当前页面URL: {page.url}")
        # 列出所有input元素供调试
        try:
            all_inputs = page.eles('tag:input', timeout=5)
            print(f"页面上共有 {len(all_inputs)} 个input元素")
            for i, inp in enumerate(all_inputs[:10]):
                inp_id = inp.attr('id') or '无id'
                inp_type = inp.attr('type') or '无type'
                print(f"  Input {i+1}: id='{inp_id}', type='{inp_type}'")
        except Exception as e2:
            print(f"无法列出input元素: {e2}")
    
    time.sleep(1)  # 再等待1秒确保元素完全渲染
    print(f"准备查找输入框，当前URL: {page.url}\n")
    
    # 查找搜索输入框并输入内容
    print("正在查找搜索输入框...")
    search_input = None
    try:
        # 方法1: 通过XPath查找input[@id='key']（最准确，确保是input元素）
        print("尝试方法1: 通过XPath查找input[@id='key']...")
        search_input = page.ele('xpath://input[@id="key"]', timeout=10)
        if search_input:
            print(f"  找到元素，标签: {search_input.tag}")
            if search_input.tag.lower() == 'input':
                print("✓ 通过XPath找到正确的input元素")
            else:
                print(f"✗ 找到的元素不是input，而是{search_input.tag}，继续查找...")
                search_input = None
        else:
            print("✗ 未找到元素")
            search_input = None
        
        if not search_input:
            # 方法2: 通过id查找，但验证是input
            print("尝试方法2: 通过id='key'查找（可能找到非input元素）...")
            temp_element = page.ele('#key', timeout=10)
            if temp_element:
                print(f"  找到元素，标签: {temp_element.tag}")
                if temp_element.tag.lower() == 'input':
                    search_input = temp_element
                    print("✓ 通过id找到input元素")
                else:
                    print(f"✗ 通过id找到的是{temp_element.tag}元素，不是input，继续查找...")
                    search_input = None
            else:
                print("✗ 未找到元素")
                search_input = None
        
        if not search_input:
            # 方法3: 通过XPath查找input[@type='text' and @aria-label='搜索']
            print("尝试方法3: 通过XPath查找input[@type='text' and @aria-label='搜索']...")
            search_input = page.ele('xpath://input[@type="text" and @aria-label="搜索"]', timeout=10)
            if search_input and search_input.tag.lower() == 'input':
                print("✓ 通过XPath组合找到input元素")
            else:
                search_input = None
        
        if not search_input:
            # 方法4: 通过aria-label查找，但验证是input
            print("尝试方法4: 通过aria-label='搜索'查找input元素...")
            inputs_with_aria = page.eles('xpath://input[@aria-label="搜索"]', timeout=10)
            if inputs_with_aria:
                for inp in inputs_with_aria:
                    if inp.tag.lower() == 'input':
                        search_input = inp
                        print(f"✓ 通过aria-label找到input元素 (id={inp.attr('id')})")
                        break
                if not search_input:
                    print("✗ 找到的元素都不是input类型")
            else:
                print("✗ 未找到匹配的input元素")
                search_input = None
        
        # 如果还是没找到，列出页面上所有input元素供调试
        if not search_input:
            print("\n" + "=" * 50)
            print("未找到input#key元素，列出页面上所有input元素供参考：")
            print("=" * 50)
            try:
                all_inputs = page.eles('tag:input', timeout=5)
                print(f"页面上共有 {len(all_inputs)} 个input元素：")
                for i, inp in enumerate(all_inputs[:15]):  # 只显示前15个
                    inp_id = inp.attr('id') or '无id'
                    inp_type = inp.attr('type') or '无type'
                    inp_class = inp.attr('class') or '无class'
                    inp_aria = inp.attr('aria-label') or '无aria-label'
                    print(f"  Input {i+1}: id='{inp_id}', type='{inp_type}', class='{inp_class}', aria-label='{inp_aria}'")
            except Exception as e:
                print(f"无法列出input元素: {e}")
            print("=" * 50 + "\n")
        
        if search_input:
            print("=" * 50)
            print("找到元素！")
            print("=" * 50)
            print(f"元素对象: {search_input}")
            print(f"元素类型: {type(search_input)}")
            print(f"元素标签: {search_input.tag}")
            
            # 安全地获取元素属性
            try:
                element_id = search_input.attr('id') or search_input.attrs.get('id', '无')
            except:
                element_id = '无法获取'
            
            try:
                element_classes = search_input.classes if hasattr(search_input, 'classes') else search_input.attrs.get('class', '无')
            except:
                element_classes = '无法获取'
            
            try:
                element_attrs = search_input.attrs
            except:
                element_attrs = '无法获取'
            
            try:
                element_text = search_input.text
            except:
                element_text = '无法获取'
            
            try:
                element_value = search_input.value if hasattr(search_input, 'value') else '无value属性'
            except:
                element_value = '无法获取'
            
            print(f"元素ID: {element_id}")
            print(f"元素class: {element_classes}")
            print(f"元素属性: {element_attrs}")
            print(f"元素文本: {element_text}")
            print(f"元素值: {element_value}")
            print("=" * 50)
            
            # 检查是否是input元素
            if search_input.tag.lower() != 'input':
                print(f"⚠️ 警告：找到的元素不是input标签，而是{search_input.tag}标签！")
                print("继续查找真正的input元素...")
                search_input = None
                
                # 重新查找，只查找input元素
                print("重新查找：只查找input[@id='key']...")
                search_input = page.ele('xpath://input[@id="key"]', timeout=5)
                if search_input and search_input.tag.lower() == 'input':
                    print("✓ 找到正确的input元素！")
                else:
                    # 查找所有input元素
                    print("查找页面上所有input元素...")
                    all_inputs = page.eles('tag:input', timeout=5)
                    print(f"找到 {len(all_inputs)} 个input元素")
                    for inp in all_inputs:
                        inp_id = inp.attr('id') or inp.attrs.get('id', '')
                        inp_type = inp.attr('type') or inp.attrs.get('type', '')
                        inp_aria = inp.attr('aria-label') or inp.attrs.get('aria-label', '')
                        print(f"  - input: id='{inp_id}', type='{inp_type}', aria-label='{inp_aria}'")
                        if inp_id == 'key' or inp_aria == '搜索':
                            search_input = inp
                            print(f"  ✓ 找到匹配的input元素！")
                            break
            
            if search_input and search_input.tag.lower() == 'input':
                print("=" * 50)
                print("找到正确的搜索输入框（input元素）！")
                print("=" * 50)
                print("准备输入内容...")
                
                try:
                    # 等待输入框可见
                    print("等待输入框准备就绪...")
                    time.sleep(0.5)
                    
                    # 滚动到输入框位置，确保可见
                    try:
                        print("滚动到输入框位置...")
                        search_input.scroll.to_see()
                        time.sleep(0.5)
                    except:
                        print("滚动失败，继续尝试...")
                    
                    # 检查输入框当前值
                    try:
                        current_value = search_input.value
                        print(f"输入框当前值: '{current_value}'")
                    except:
                        print("无法获取输入框当前值")
                    
                    # 方法1: 先点击输入框获取焦点，然后输入
                    print("\n尝试方法1: 点击输入框获取焦点，然后使用input()方法...")
                    try:
                        # 点击输入框获取焦点
                        search_input.click()
                        time.sleep(0.5)
                        print("✓ 已点击输入框获取焦点")
                        
                        # 清空输入框
                        search_input.clear()
                        time.sleep(0.3)
                        print("✓ 已清空输入框")
                        
                        # 使用input方法输入
                        search_input.input('RTX5090 / D')
                        time.sleep(0.8)
                        
                        # 验证输入是否成功
                        input_value = search_input.value
                        print(f"输入后，输入框的值: '{input_value}'")
                        if input_value and 'RTX5090' in input_value:
                            print(f"✓ 已通过input方法输入搜索内容：{input_value}")
                            
                            # 使用JavaScript确保值被设置并触发所有事件
                            print("\n使用JavaScript确保页面显示输入内容...")
                            try:
                                # 方法A: 直接设置值并触发所有事件
                                result = page.run_js('''
                                    var input = document.getElementById('key');
                                    if (input) {
                                        // 先聚焦
                                        input.focus();
                                        
                                        // 设置值
                                        input.value = 'RTX5090 / D';
                                        
                                        // 触发所有可能的事件
                                        var events = ['input', 'change', 'keyup', 'keydown', 'focus', 'blur'];
                                        events.forEach(function(eventType) {
                                            var event;
                                            if (eventType === 'keyup' || eventType === 'keydown') {
                                                event = new KeyboardEvent(eventType, { 
                                                    bubbles: true, 
                                                    cancelable: true,
                                                    key: 'a',
                                                    code: 'KeyA'
                                                });
                                            } else {
                                                event = new Event(eventType, { 
                                                    bubbles: true, 
                                                    cancelable: true 
                                                });
                                            }
                                            input.dispatchEvent(event);
                                        });
                                        
                                        // 再次聚焦确保可见
                                        input.focus();
                                        
                                        return {
                                            success: true,
                                            value: input.value,
                                            isFocused: document.activeElement === input
                                        };
                                    }
                                    return { success: false };
                                ''')
                                
                                time.sleep(0.8)
                                
                                if result:
                                    if isinstance(result, dict):
                                        if result.get('success'):
                                            print(f"✓ JavaScript设置成功")
                                            print(f"  值: {result.get('value')}")
                                            print(f"  是否聚焦: {result.get('isFocused')}")
                                        else:
                                            print("⚠️ JavaScript设置返回success=false")
                                    else:
                                        print(f"✓ JavaScript执行完成，返回: {result}")
                                else:
                                    print("⚠️ JavaScript设置可能失败")
                                
                                # 再次验证值
                                final_value = search_input.value
                                print(f"最终验证，输入框的值: '{final_value}'")
                                
                                # 等待一下让页面更新
                                time.sleep(0.5)
                                
                                # 使用JavaScript检查页面上实际显示的内容
                                try:
                                    displayed_value = page.run_js('''
                                        var input = document.getElementById('key');
                                        if (input) {
                                            return {
                                                value: input.value,
                                                displayValue: input.value || '',
                                                placeholder: input.placeholder || '',
                                                isVisible: input.offsetWidth > 0 && input.offsetHeight > 0,
                                                style: window.getComputedStyle(input).display
                                            };
                                        }
                                        return null;
                                    ''')
                                    if displayed_value:
                                        print(f"页面上input元素的实际状态:")
                                        if isinstance(displayed_value, dict):
                                            print(f"  value: '{displayed_value.get('value', '')}'")
                                            print(f"  displayValue: '{displayed_value.get('displayValue', '')}'")
                                            print(f"  placeholder: '{displayed_value.get('placeholder', '')}'")
                                            print(f"  isVisible: {displayed_value.get('isVisible', False)}")
                                            print(f"  display style: '{displayed_value.get('style', '')}'")
                                        else:
                                            print(f"  {displayed_value}")
                                except Exception as check_error:
                                    print(f"检查页面显示失败: {check_error}")
                                    
                            except Exception as js_error:
                                print(f"JavaScript触发事件失败: {js_error}")
                                import traceback
                                traceback.print_exc()
                        else:
                            print(f"✗ input方法失败，输入框值仍为: '{input_value}'")
                            raise Exception("input方法未成功")
                    except Exception as method1_error:
                        print(f"方法1失败: {method1_error}")
                        
                        # 方法2: 使用set.value方法
                        print("\n尝试方法2: 使用set.value()方法...")
                        try:
                            search_input.set.value('RTX5090 / D')
                            time.sleep(0.8)
                            
                            # 验证输入是否成功
                            input_value = search_input.value
                            print(f"输入后，输入框的值: '{input_value}'")
                            if input_value and 'RTX5090' in input_value:
                                print(f"✓ 已通过set.value输入搜索内容：{input_value}")
                            else:
                                print(f"✗ set.value方法失败，输入框值仍为: '{input_value}'")
                                raise Exception("set.value方法未成功")
                        except Exception as method2_error:
                            print(f"方法2失败: {method2_error}")
                            
                            # 方法3: 先点击，再清空，再逐个字符输入
                            print("\n尝试方法3: 逐个字符输入...")
                            try:
                                # 点击获取焦点
                                search_input.click()
                                time.sleep(0.3)
                                
                                # 清空
                                search_input.clear()
                                time.sleep(0.3)
                                
                                # 逐个字符输入
                                text_to_input = 'RTX5090 / D'
                                for char in text_to_input:
                                    search_input.input(char)
                                    time.sleep(0.1)
                                
                                time.sleep(0.5)
                                
                                # 验证输入是否成功
                                input_value = search_input.value
                                print(f"输入后，输入框的值: '{input_value}'")
                                if input_value and 'RTX5090' in input_value:
                                    print(f"✓ 已通过逐个字符输入搜索内容：{input_value}")
                                else:
                                    print(f"✗ 逐个字符输入也失败，输入框值仍为: '{input_value}'")
                            except Exception as method3_error:
                                print(f"方法3失败: {method3_error}")
                                import traceback
                                traceback.print_exc()
                    
                    # 查找并点击搜索按钮
                    print("正在查找搜索按钮...")
                    time.sleep(0.5)
                
                    search_button = None
                    # 方法1: 通过aria-label查找搜索按钮（确保是button标签）
                    buttons = page.eles('@aria-label:搜索', timeout=5)
                    for btn in buttons:
                        if btn.tag == 'button':
                            search_button = btn
                            break
                    
                    if not search_button:
                        # 方法2: 通过XPath查找button标签
                        search_button = page.ele('xpath://button[@aria-label="搜索"]', timeout=5)
                    
                    if not search_button:
                        # 方法3: 通过class和文本内容查找
                        search_button = page.ele('xpath://button[@class="button" and text()="搜索"]', timeout=5)
                    
                    if not search_button:
                        # 方法4: 通过文本内容查找（可能是第一个button）
                        buttons = page.eles('text:搜索', timeout=5)
                        for btn in buttons:
                            if btn.tag == 'button':
                                search_button = btn
                                break
                    
                    if search_button:
                        # 点击搜索按钮
                        try:
                            search_button.click()
                            print("已点击搜索按钮，开始搜索！")
                        except Exception as click_error:
                            print(f"点击按钮失败: {click_error}")
                            print("请检查按钮是否可见和可点击")
                    else:
                        print("未找到搜索按钮")
                        
                except Exception as e:
                    print(f"操作搜索输入框或按钮时出错: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("✗ 未找到正确的input输入框元素，无法继续输入")
                search_input = None
        else:
            print("=" * 50)
            print("未找到搜索输入框！")
            print("=" * 50)
            print("已尝试以下所有方法：")
            print("1. 通过id='key'查找")
            print("2. 通过aria-label='搜索'查找")
            print("3. 通过class='text'查找")
            print("4. 通过XPath查找input[@id='key']")
            print("5. 通过XPath查找input[@type='text' and @aria-label='搜索']")
            print("=" * 50)
            # 尝试查找所有input元素，看看页面上有哪些input
            print("尝试查找页面上所有的input元素...")
            all_inputs = page.eles('tag:input', timeout=3)
            print(f"页面上共有 {len(all_inputs)} 个input元素")
            for i, inp in enumerate(all_inputs[:10]):  # 只显示前10个
                print(f"  Input {i+1}: id={inp.id}, type={inp.attrs.get('type', '')}, class={inp.classes}, aria-label={inp.attrs.get('aria-label', '')}")
            print("=" * 50)
    except Exception as e:
        print(f"查找或操作搜索输入框时出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 等待搜索结果加载
    time.sleep(3)
    
    print("操作完成！")
    
    # 保持浏览器打开，方便查看
    input("按 Enter 键关闭浏览器...")
    
except Exception as e:
    print(f"访问网页时出错: {e}")
    
finally:
    # 关闭页面
    page.close()
    print("浏览器已关闭")


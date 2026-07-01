# 鸿远门户开发教训 0527（竞品详情页白屏修复全过程）

> 本文档记录 2026-05-27 修复「竞品对手雷达点击无反应/白屏/专利加载不出」全过程踩过的坑。

---

## 教训16：竞品详情跳转白屏 = showPage里page名映射错误

```
症状：点击竞品card → 白屏
根本原因：旧版 showPage()（行759）里 'competitor':-1，-1 表示没有对应tab
         'comp-detail' 根本不在映射表里
新版 showPage()（行1170）里 competitor:4 是正确的
但文件里同时存在两个 showPage 定义，后定义覆盖前定义
而 goCompDetail 调用时恰好走了旧版
✅ 修复：删除旧版 showPage，只保留新版；补充 'comp-detail':4 映射
```

## 教训17：两个同名函数并存 = 后者覆盖前者，前者调用参数失效

```
症状：专利列表一直显示「加载中」，不渲染
根本原因：文件里有两个 loadCompDetail 定义
  - 第1268行：async function loadCompDetail(name, patentsEl, newsEl, statsEl) ← 旧版，4参数
  - 第1882行：async function loadCompDetail(name, keywords) ← 新版，2参数
goCompDetail 传的是4个参数（第2个是DOM元素），但新版函数只接受2个参数
=> name 收到了 DOM元素，搜索关键词变成 "[object HTMLDivElement]"
✅ 修复：删除旧版（第1268~1331行），只保留新版
✅ 同时修复调用：loadCompDetail(name, name) 只传名字
```

## 教训18：同名 id 在隐藏页面里 = getElementById 找到的是隐藏元素，渲染了也看不见

```
症状：数据接口返回正常（终端有✅），但页面永远显示「加载中」
根本原因：`cd-patents` div 在第741行 page-competitor 里（默认隐藏）
         page-comp-detail 里根本没有这个 id
         loadCompDetail 里 getElementById('cd-patents') 找到的是隐藏页面里的元素
         渲染了也看不见
✅ 修复：在 page-comp-detail 里新增 id="cd-patents-detail" div
✅ loadCompDetail 改为优先找 cd-patents-detail，fallback cd-patents
```

## 教训19：page div 的 inline style="display:none" 会覆盖 CSS .page.active

```
症状：showPage('comp-detail') 调用成功，但页面仍然白屏
根本原因：page-comp-detail 的 HTML 是 <div id="page-comp-detail" class="page" style="display:none">
         CSS .page.active{display:block} 优先级低于 inline style，被覆盖
✅ 修复：去掉 inline display:none，统一由 CSS .page / .page.active 控制
```

## 教训20：@folder 挂载路径与真实磁盘路径可能一致，但 grep 有时返回0匹配

```
本次实测：@folder:hongyuan_portal/public/index.html cat 可以读到1934行
但有时 files grep 返回0匹配，原因未知
✅ 安全做法：grep不到时，改用 files head 指定行范围读取
            关键修改用 node -e 脚本在Mac Terminal执行，不依赖 Eureka grep
```

## 教训21：多次patch脚本叠加 = 函数残骸、残留参数、多版本并存

```
危险：多个 fix_xxx.js 脚本先后执行，每次patch一部分
=> 最终文件里出现：
   - 2个 loadCompDetail 定义（行1268 + 行1882）
   - goCompDetail 里的调用参数不匹配（传DOM元素 vs 接收name字符串）
   - page-comp-detail 有 cd-total/cd-active 但没有 cd-patents
✅ 安全做法：每次patch后立刻验证所有关键函数只有一个定义
   node -e "['loadCompDetail','goCompDetail','showPage'].forEach(fn=>{
     const hits=[];lines.forEach((l,i)=>{if(l.includes('function '+fn))hits.push(i+1);});
     console.log(fn+' 定义行:', hits);
   })"
```

## 教训22：终端有数据但页面不渲染，优先检查「渲染目标元素是否在当前可见页面里」

```
诊断顺序（节省时间）：
1. 终端有✅ → 接口OK，问题在前端渲染
2. 检查 getElementById('目标id') 是否在当前显示的页面里
3. 检查同名id是否在其他隐藏页面里
4. 检查函数是否有多个定义（后者覆盖前者）
5. 最后才检查函数逻辑
```

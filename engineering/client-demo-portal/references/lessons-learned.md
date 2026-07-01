# 调试教训汇总（持续更新）

## 【教训16】按钮要放在它所属容器的内部，不要放外部靠display控制
```
❌ 错误：
<button class="back-btn" onclick="hideDetail()">← 返回</button>  ← 在panel外面
<div id="detail-panel" style="display:none">...</div>
→ panel隐藏时按钮可见，panel显示时按钮被showDetail误隐藏

✅ 正确：
<div id="detail-panel" style="display:none">
  <button class="back-btn" onclick="hideDetail()">← 返回</button>  ← 在panel里面
  ...
</div>
→ 按钮随panel一起显隐，永远不会丢失
```

## 【教训17】querySelectorAll批量显隐时选择器要精确，避免误伤
```
❌ 危险：querySelectorAll('.grid, .title, .header, .back-btn')
→ .back-btn被一起隐藏了，再也找不回来

✅ 正确：querySelectorAll('.grid, .section-title, .header')
→ 只隐藏内容区，不动按钮
→ 按钮随panel容器显隐，不需要单独控制
```

## 【教训18】</html>后面有残留<script>块是历史遗留，需清理
```
症状：文件结构变成：
  </body>
  </html>
  <script>...残骸...</script>  ← 不规范

原因：之前patch脚本追加位置找错，追加到</html>后面了

清理方法：
1. 找到</html>位置
2. 把</html>后面的所有<script>块移到</body>前面
3. 删除</html>后面的残骸

✅ 临时可用：语法检查通过就不影响运行，但要在稳定版备份后清理
```

## 【教训19】脚本文件必须先确认存在再让用户运行
```
症状：用户运行 node /path/to/script.js 报 MODULE_NOT_FOUND
原因：Eureka写脚本工具调用失败或路径不对，文件没有生成

✅ 正确做法：
1. 每次写脚本后，立刻用 files.exists 或 files.stat 确认文件存在
2. 文件不存在就重写，不要让用户先跑再报错
3. 或者改用 node -e "..." 内联方式，完全不依赖外部文件
```

## 【教训20】showDetail/hideDetail函数分工铁律
```
showDetail(key)：
  1. 把所有内容区(.grid/.section-title/.header)设为 display:none
  2. 把detail-panel设为 display:block
  ❌ 绝对不要隐藏 .back-btn

hideDetail()：
  1. 把所有内容区设为 display:''
  2. 把detail-panel设为 display:none
  ❌ 绝对不要单独操作 .back-btn（它在panel里，随panel一起隐藏）
```

## 历史教训（前15条见SKILL.md）
见 SKILL.md 中的【教训1】~【教训15】

# 金属材料及热处理：教材与习题实验 Skill

基于史文主编《金属材料及热处理》第二版和配套《金属材料及热处理习题集与实验指导书》第二版，由book-to-skill流程生成并人工式按页核对关键图表的中文知识工具。

用途是按原书的思考路径学习、解释、计算与选材：**成分 → 工艺 → 组织 → 性能 → 检验**。成果采用重新组织的短解释与方法，没有上传原书PDF、OCR全文或原书图片。

## 从这里开始

- [技能入口](skills/shi-metal-materials-heat-treatment/SKILL.md)：按主题路由，适合支持SKILL.md格式的代理读取。
- [学习路线](skills/shi-metal-materials-heat-treatment/study-plan.md)：六阶段学习和复习任务。
- [逐题索引](skills/shi-metal-materials-heat-treatment/exercises/index.json)：184道顶层题，保留准确的题目页范围。
- [计算详解](skills/shi-metal-materials-heat-treatment/exercises/worked-calculations.md)：12组公式、演算和近似检查。
- [金相实验基础](skills/shi-metal-materials-heat-treatment/labs/metallography-basics.md)：连接6个实验指南。
- [来源与页码](skills/shi-metal-materials-heat-treatment/sources.md)、[覆盖与已知限制](skills/shi-metal-materials-heat-treatment/quality.md)：先确认依据再使用。

## 内容规模

| 内容 | 范围 |
|---|---|
| 章节知识文件 | 9章 |
| 习题导航与解题要点 | 绪论6题+九章178题=184道顶层题 |
| 计算详解 | 12组 |
| 实验 | 金相基础+6个实验 |
| 辅助知识 | 术语、方法、决策速查、学习计划 |
| 本地工具 | 习题检索、杠杆/FCC/再结晶温度计算 |

**184题均有索引和要点，不等于184题全部子问已精解认证。**17道题明确列出需进一步补核的图表或完整子问；并非出版社标准答案。没有进行真实实验或生成实测数据。具体列表和OCR限制见quality.md。

## 使用

将 `skills/shi-metal-materials-heat-treatment/` 整个目录放入所用代理的个人技能目录，或由代理直接读取本仓库SKILL.md。保留目录层次，入口链接按需加载其他文件。

本项目在Codex环境中的安装目标是用户已有的 `.codex/skills` 下的同名目录。对于其他工具，应使用其实际配置的技能目录；不要把本仓库根目录误当成单个技能。

示例请求：

> 使用 shi-metal-materials-heat-treatment，解释淬硬性、淬透性和淬硬层深度，给出原书页码。
>
> 辅导习题3-12，先提示，再列式，最后做质量守恒检查。
>
> 分析45钢主轴的调质与轴颈表面淬火路线，指出还缺哪些条件。
>
> 设计实验5的记录表，不填造实验数值。

从仓库根目录复算（Python标准库即可）：

```sh
python skills/shi-metal-materials-heat-treatment/scripts/find_exercise.py 5-40
python skills/shi-metal-materials-heat-treatment/scripts/calculate.py lever --c0 50 --left 15 --right 95
python skills/shi-metal-materials-heat-treatment/scripts/calculate.py fcc --diameter-nm 0.256
python -m unittest discover -s tests -v
python tools/validate_repository.py
```

## 来源与处理

教材扫描302页、配套扫描72页，共374页均经本地中文OCR，随后将保留页边界的文本传入book-to-skill提取流程，按章重组。由于原文件是扫描页，未使用会跳过OCR的Docling默认流程；技术性公式、图表和关键题目另看原图核验。完整指纹在技能内source-manifest.json。

原书成书年份早于本项目，引用牌号与标准处于原书语境。本项目没有认证所有历史参数等同现行工程要求。对于真实工件，仍需明确截面、工况、产品数据、验收和实际试验。

## 权利与范围

原书版权归各原权利人。本项目为独立整理的学习笔记、解题推导和脚本，不代表作者、出版社或官方解答，也未获得原书再分发授权。公开仓库不授予任何原书复制传播权利。

生成日期：2026-10-20。发布前执行技能结构校验、提示注入模式扫描、内部链接与题号核对，以及数值测试；见[验证记录](validation/RESULTS.md)。

根据当前 Session 的 `propose.md`、`skills/route-a-evaluator.md`、`skills/route-b-evaluator.md` 和 `docs/prior_work/`，继续自主研究。

本轮采用 **Batch Research Mode**：

> 不再每完成一篇论文等待用户确认。  
> 以 **连续完成 5 个论文项目** 为一个研究批次。  
> 只有整个批次完成后，再暂停并统一向用户汇报，等待下一轮确认。

## 1. 批次执行规则

从当前已有论文编号继续。

连续完成最多 5 个新的论文项目：

```text
Paper N
→ Paper N+1
→ Paper N+2
→ Paper N+3
→ Paper N+4
```

每完成一个论文项目后：

1. 完成该论文当前阶段能够支持的数学、代码、实验和验证；
2. 生成完整论文 PDF；
3. 更新该论文项目的 `README.md`；
4. 按 Session 规范在根目录 `README.md` 追加一行：
   ```text
   论文子目录名称 - 当前阶段 - 主要进展
   ```
5. 使用 Route A / Route B evaluator 对当前结果进行适当评估；
6. 提取：
   - strongest positive result；
   - strongest obstruction；
   - open theorem；
   - reusable structure；
   - ROUND2_CLUE；
7. **根据刚完成论文的真实结论，自主决定下一篇论文最值得研究的问题；**
8. 立即开始下一篇，不等待用户确认。

下一篇论文必须是上一阶段的自然延续、必要验证、反例攻击、结构推广或失败后的最小合理替代。

不要为了凑满 5 篇而制造无意义论文。

---

## 2. 自主决策原则

每篇论文完成后，自动判断下一步。

优先级：

```text
强异常信号
→ 独立复现 / adversarial validation

明确正结果
→ 最小结构推广 / 更严格 theorem

明确 obstruction
→ 定位缺失结构并测试最自然替代

候选失败
→ 提取 obstruction 后切换到本 Session 内下一个合理候选

跨系统族新想法
→ 只记录 ROUND2_CLUE，不展开
```

始终遵守：

```text
one session = one dynamical-system family
```

不要像自由探索模式一样扩张到其他系统族。

---

## 3. 研究风格

本批次允许：

```text
大胆假设
+
快速实验
+
自动迭代
+
后续严格求证
```

可以先提出高风险猜想并快速验证。

但必须严格区分：

```text
PROVED
CONDITIONAL_THEOREM
NUMERICALLY_CERTIFIED
NUMERICAL_OBSERVATION
HEURISTIC
CONJECTURE
MODELING_CHOICE
OPEN
REFUTED
STOP_SCOPED
```

正式宣称 Route A / Route B 通过时，必须严格使用 evaluator。

---

## 4. 不允许中途暂停询问用户的情况

以下情况自行判断并继续：

- 下一篇论文选哪个候选；
- 是否增加数值精度；
- 是否增加合理对照；
- 一个猜想失败后测试哪个自然替代；
- 是否检索新论文；
- 是否写证明、代码或补实验；
- 是否将负结果写成 obstruction paper；
- 论文标题、缩写和项目目录名称；
- 合理的局部研究路线调整。

这些属于研究自主权。

**不要因为这些问题等待用户确认。**

---

## 5. 可以提前停止批次的情况

只有出现以下情况才允许在 5 篇之前停止：

### HARD BLOCKER

继续推进需要当前不存在的关键数学定理、数据类型或外部输入，并且在当前 Session 范围内没有合理替代路线。

### SCOPE EXHAUSTED

本 Session 的系统族已经形成明确的结构性封口，继续研究只会重复已有结果。

### MAJOR BREAKTHROUGH

出现异常强的结果，例如同一个自然对象严格达到：

```text
A0 + A1 + A2
```

或更高，并通过 adversarial controls。

此时不要继续批量制造后续论文。

转入：

```text
independent reproduction
→ hostile review
→ stronger certification
```

然后提前结束批次并汇报。

### TECHNICAL BLOCKER

基础设施、编译、Git 或计算资源出现无法自行恢复的问题。

如果只是 Git push 暂时失败，不要停止科学研究：

```text
继续保存本地结果
→ 记录同步失败
→ 批次结束统一汇报
```

---

## 6. 每篇论文的质量要求

每篇论文必须是一个真实研究阶段，而不是为了满足数量要求拆分文章。

论文项目必须包含 Session `propose.md` 规定的：

```text
README.md
paper/
code/
experiments/
results/
notes/
```

并最终产生：

```text
paper/paper.pdf
```

作者统一使用 Session 中规定的 Liang Wang / HUST 信息。

每篇论文至少应贡献以下之一：

- 新候选；
- 新定理；
- 新 obstruction；
- 新 analytic structure；
- 新 numerical certificate；
- 新反例；
- 新结构推广；
- 新 arithmetic connection；
- 新 classical/quantum bridge；
- 对已有候选的严格否定。

---

## 7. Git 与持续同步

按照当前 Session `propose.md` 的 GitHub 规则执行。

每完成一个论文项目：

```text
update local README
→ commit
→ sync to the Session GitHub subdirectory
```

同步前遵守项目规定的 `git pull` / conflict check。

不要覆盖其他 Session 的内容。

---

## 8. 第 5 篇完成后

完成本批次第 5 个论文项目后：

**停止创建第 6 个项目。**

进行一次 Batch Review。

生成简洁汇报：

```text
BATCH SUMMARY

完成论文：
1.
2.
3.
4.
5.

每篇一句话：
1.
2.
3.
4.
5.

当前最强 Route-A 状态：
(A0, A1, A2, A3, A4)

本轮最重要正结果：

本轮最重要负结果 / obstruction：

最值得保留的结构：

最重要 ROUND2_CLUE：

当前最大 blocker：

下一批最值得研究的 3 个方向：
1.
2.
3.

推荐：
CONTINUE / PIVOT / FREEZE / MAJOR_REVIEW
```

然后暂停，等待用户统一确认下一批研究方向。

---

## 9. 核心要求

不要把“5 篇”理解为 KPI。

真正的执行逻辑是：

```text
上一论文的真实结论
        ↓
自动选择下一最小且最有价值的问题
        ↓
完成论文项目
        ↓
再次评价
        ↓
继续
```

用户只在 **每 5 篇一个批次** 后进行一次管理层审查。

现在开始本批次研究，不需要逐篇询问确认。
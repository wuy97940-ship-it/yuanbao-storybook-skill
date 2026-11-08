---
name: yuanbao-storybook
description: Turn prepared illustrations and optional pose keyframes into a low-frame-rate storybook video with captions. Use when making narrated or silent picture-book pages; it does not generate illustrations or publish content.
---

# 圆宝动态绘本

将用户提供或授权生成的插画整理为逐页故事：每页写清起始状态、一个动作、末态和文字；保持角色身份、构图与道具连续。复杂动作先做代表页检查，再扩展整片。

工具接受每页一至多张同构图姿态图及文案，默认 6fps 输出竖屏 MP4。关键帧用淡化过渡，适用于轻微姿态变化；不是物理动画或真实逐笔手写。用户要求真实笔顺、翻页、精确遮挡或专业口播时应另外制作并检验，不得虚称已实现。

复制项目示例 `examples/demo/story.json`，换成本次有权使用的图片和文案，调用本技能目录下的 `scripts/render.py`，例如在仓库根目录运行 `python skills/yuanbao-storybook/scripts/render.py examples/demo/story.json --output output/story.mp4`。可用 `--font` 指定支持中文的字体、`--audio` 添加用户有权使用的音乐。脚本不会自行生成图像、音乐或上传作品。

检查实际视频的每页起始、过渡和末态，确认文字可读、角色稳定、音频可用；机器参数检查与人工播放分别记录。无用户明确授权不发布，不把用户私密原图放进公开仓库。

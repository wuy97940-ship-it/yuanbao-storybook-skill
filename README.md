# 圆宝动态绘本 · Yuanbao Storybook Skill

把准备好的插画、文字和姿态图，组合成一段低帧率动态绘本。这个项目包含一份可供 Codex 等支持技能的工具读取的 Skill，以及一个可独立运行的 Python 渲染器。

![项目内置示例：种子发芽](examples/demo/preview.gif)

## 现在能做什么

- 读取简单的 JSON 故事清单，逐页合成竖屏 MP4；默认每页 3 秒、6 帧/秒。
- 每页支持一张插画或多张相同构图的姿态图，使用淡化过渡；字幕逐字显现。
- 可选择添加你有权使用的音乐；音频按视频时长截取，末尾淡出。
- 内置原创示例，使用 Pillow 和 FFmpeg 即可本地跑通；无需 API Key。

**边界：**当前脚本不生成插画、音乐或配音，也不自动发布。姿态过渡是淡化而非真实动画补帧；逐字显示不是逐笔手写，也没有独立的翻页动画或书写音效。复杂动作和素材一致性仍需人工制作和检查。

## 快速开始

需要 Python 3.10+，以及 Pillow、imageio-ffmpeg：

```bash
python -m pip install -r requirements.txt
python skills/yuanbao-storybook/scripts/render.py examples/demo/story.json --output output/demo.mp4
```

渲染你自己的故事时，复制 `examples/demo/story.json` 并将 `images` 改成相对于 JSON 文件的图片路径，修改每页 `lines`。中文请通过 `--font` 指定有权使用的中文字体：

```bash
python skills/yuanbao-storybook/scripts/render.py my-story/story.json --font /path/to/chinese-font.ttf --audio /path/to/music.mp3 --output output/my-story.mp4
```

`--audio` 可省略；脚本不会覆盖已有输出。音乐、字体与图片的使用权由使用者分别确认。请先看示例、再检查自己作品的每页起始、过渡、末态及实际听感。

## 作为 Skill 使用

将 `skills/yuanbao-storybook/` 复制到支持 `SKILL.md` 的工具的技能目录，保留其中的 `scripts/`；按工具的技能发现方式启用。准备故事清单和素材后，让助手按该 Skill 制作绘本。各平台的安装和生图能力取决于实际环境。

## 来源与许可

本项目从 [WoYun520/gif-factory 的紧凑动态绘本](https://github.com/WoYun520/gif-factory/tree/main/skills/compact-storybook) 获得创作流程启发；本仓库的脚本和示例为独立实现，功能范围以上文为准。代码与本项目原创示例使用 [MIT License](LICENSE)。第三方素材、字体和音乐须遵循各自的许可。

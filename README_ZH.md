# pixmo-docs

本仓库用于生成 [PixMo-Docs](https://huggingface.co/datasets/allenai/pixmo-docs)、[CoSyn-400K](https://huggingface.co/datasets/allenai/CoSyn-400K) 和 [CoSyn-point](https://huggingface.co/datasets/allenai/CoSyn-point) 数据集。PixMo-Docs 用于训练 [Molmo](https://arxiv.org/abs/2409.17146) 模型，CoSyn 数据集是扩展版本，采用了改进的生成流程并涵盖更多文档类型。更多细节请参见我们的 [论文](https://arxiv.org/pdf/2502.14846)。

## 快速开始
[main.py](main.py) 是数据集生成的入口脚本。可用如下参数控制生成流程：
> 更多参数及用法请参考 [main.py](main.py) 脚本。

### 先把`OPENAI`或 `Claude` key 设置到 [.env](.env) 中


### 样例
* `-p "MermaidDiagramPipeline" -l "gpt-4o" -c "gpt-4o" -n 1 -m "mermaid_diagrams" -t "sequence" -b 1 -q "False" -lang Chinese --force` 
    * -p: 使用 MermaidDiagramPipeline 管道
    * -l: 使用 gpt-4o 作为主语言模型
    * -c: 使用 gpt-4o 作为校对语言模型
    * -n: 生成 1 个样本
    * -m: 数据集名称为 "mermaid_diagrams"
    * -t: 生成时序图
    * -b: 每次生成 1 个样本
    * -q: 不生成问答对
    * -lang: 使用中文
    * --force: 强制覆盖已存在的数据集
* `-p "HTMLChartPipeline" -l "gpt-4o" -c "gpt-4o" -n 1 -m "html_charts" -t "bar" -b 1 -q "False" --force`
    * -p: 使用 HTMLChartPipeline 管道
    * -l: 使用 gpt-4o 作为主语言模型
    * -c: 使用 gpt-4o 作为校对语言模型
    * -n: 生成 1 个样本
    * -m: 数据集名称为 "html_charts"
    * -t: 生成条形图
    * -b: 每次生成 1 个样本
    * -q: 不生成问答对
    * --force: 强制覆盖已存在的数据集

### 可能会遇到的异常
Q: ValueError: Expected {'llm', 'code_llm', 'batch_size', 'code_batch_size', 'n', 'seed', 'figure_types', 'qa'} as args, with {'llm', 'code_llm', 'batch_size', 'code_batch_size', 'n', 'seed', 'figure_types', 'qa'} required, got {'llm', 'code_llm', 'batch_size', 'code_batch_size', 'n', 'seed', 'figure_types', 'qa', 'language'}. See `HTMLChartPipeline.help`:

A: 该异常是由于所使用的管道不支持 `language` 参数。本工程只针对 `MermaidDiagramPipeline` 进行了多语言支持，其他管道均不支持。**解决方式（使用一种方式即可）：** 1、请移除`all_pipelines`中`132行`的 `language` 参数。2、参考 `MermaidDiagramPipeline` 的实现自行添加多语言支持。


### 如何查看`*.arrow` 文件
可以使用 [Decompression.py](tools/Decompression.py) 代码来完成解压，指定`arrow_file`和`output_dir`即可。



## 管道说明
我们发布了 25 个管道，可生成八大类富文本图像：图表、表格、文档、图示、电路、专业图形、网页界面和指点类。每个管道使用一种渲染器或编程语言生成图像。

* **图表**：
    * *MatplotlibChartPipeline*：使用 [Matplotlib](https://matplotlib.org/) 生成条形图、折线图等。可参考 [Matplotlib gallery](https://matplotlib.org/stable/gallery/index.html)。
    * *PlotlyChartPipeline*：使用 [Plotly](https://plotly.com/python/) 生成图表。可参考 [Plotly gallery](https://plotly.com/python/)。
    * *VegaLiteChartPipeline*：使用 [Vega-Lite](https://vega.github.io/vega-lite/) 生成图表。可参考 [Vega-Lite gallery](https://vega.github.io/vega-lite/examples/)。
    * *LaTeXChartPipeline*：使用 TikZ 生成简单图表，如条形图、折线图等。
    * *HTMLChartPipeline*：使用 HTML 和 CSS 生成简单图表。

* **表格**：
    * *LaTeXTablePipeline*：适合复杂结构表格。
    * *MatplotlibTablePipeline*：用 Matplotlib 在图中渲染表格。
    * *PlotlyTablePipeline*：仅支持简单表格，如单表头表格。
    * *HTMLTablePipeline*：仅支持简单表格。

* **文档**：
    * *LaTeXDocumentPipeline*：支持多种文档类型，如报告、文章等。
    * *HTMLDocumentPipeline*：可生成复杂样式和结构的文档。
    * *DOCXDocumentPipeline*：生成 Microsoft Word 兼容的 `.docx` 文档。

* **图示**：
    * *GraphvizDiagramPipeline*：使用 [Graphviz](https://graphviz.org/) 生成有向图、树等。
    * *MermaidDiagramPipeline*：使用 [Mermaid](https://mermaid-js.github.io/mermaid/#/) 生成流程图、时序图等。
    * *LaTeXDiagramPipeline*：使用 TikZ 生成图示。可参考 [此处](https://texample.net/tikz/examples/tag/diagrams/)。

* **电路**：
    * *SchemDrawCircuitPipeline*：使用 [SchemDraw](https://schemdraw.readthedocs.io/) 生成电路图。
    * *LaTeXCircuitPipeline*：使用 TikZ 电路库生成电路图。

* **专业图形**：
    * *DALLEImagePipeline*：使用 DALL·E 模型生成图像。
    * *RdkitChemicalPipeline*：用 [RDKit](https://www.rdkit.org/) 渲染化学结构图。
    * *LaTeXMathPipeline*：用 LaTeX 生成数学表达式。
    * *LilyPondMusicPipeline*：用 [LilyPond](http://lilypond.org/) 生成乐谱。
    * *SVGGraphicPipeline*：生成 SVG 矢量图。
    * *AsymptoteGraphicPipeline*：用 [Asymptote](https://asymptote.sourceforge.io/) 生成数学和技术图形。

* **网页界面**：
    * *HTMLScreenPipeline*：用 [Playwright](https://playwright.dev/) 和 Chrome/Chromium 渲染 HTML 屏幕布局。

* **指点类**：
    * *HTMLDocumentPointPipeline*：生成带结构化指点的 HTML 文档。

## 引用
如在您的工作中使用本代码库或数据集，请引用以下论文：

```bibtex
@article{yang2025scaling,
      title={Scaling Text-Rich Image Understanding via Code-Guided Synthetic Multimodal Data Generation},
      author={Yang, Yue and Patel, Ajay and Deitke, Matt and Gupta, Tanmay and Weihs, Luca and Head, Andrew and Yatskar, Mark and Callison-Burch, Chris and Krishna, Ranjay and Kembhavi, Aniruddha and others},
      journal={arXiv preprint arXiv:2502.14846},
      year={2025}
}
```

```bibtex
@article{deitke2024molmo,
  title={Molmo and pixmo: Open weights and open data for state-of-the-art multimodal models},
  author={Deitke, Matt and Clark, Christopher and Lee, Sangho and Tripathi, Rohun and Yang, Yue and Park, Jae Sung and Salehi, Mohammadreza and Muennighoff, Niklas and Lo, Kyle and Soldaini, Luca and others},
  journal={arXiv preprint arXiv:2409.17146},
  year={2024}
}
```


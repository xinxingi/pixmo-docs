# pixmo-docs

本仓库用于生成 [PixMo-Docs](https://huggingface.co/datasets/allenai/pixmo-docs)、[CoSyn-400K](https://huggingface.co/datasets/allenai/CoSyn-400K) 和 [CoSyn-point](https://huggingface.co/datasets/allenai/CoSyn-point) 数据集。PixMo-Docs 用于训练 [Molmo](https://arxiv.org/abs/2409.17146) 模型，CoSyn 数据集是扩展版本，采用了改进的生成流程并涵盖更多文档类型。更多细节请参见我们的 [论文](https://arxiv.org/pdf/2502.14846)。

## 安装
克隆仓库后，可使用以下命令安装所需依赖：

```bash
conda create --name pixmo-doc python=3.10
conda activate pixmo-doc
pip install -r requirements.txt
```

然后将你的 API key 以环境变量形式导出：

```bash
export OPENAI_API_KEY=your-api-key
export ANTHROPIC_API_KEY=your-api-key
export HF_TOKEN=your-api-key # 仅当你需要上传数据集到 Hugging Face Hub 时
```

部分管道需要安装以下软件包：
1. LaTeX：安装方式依操作系统而异，可参考 [LaTeX 官网](https://www.latex-project.org/get/)。
2. Mermaid：可参考 [此处](https://github.com/mermaid-js/mermaid-cli) 使用 npm 安装 Mermaid CLI：
    ```bash
    npm install -g @mermaid-js/mermaid-cli
    ```
3. HTML：安装 playwright：
    ```bash
    pip install playwright
    playwright install
    ```
4. mplfinance：
   ```
   pip install mpl_finance<=0.10.1 mplfinance<=0.12.10b0
   ```
5. cairosvg：
   ```
   pip install cairosvg<=2.7.1
   ```

## 快速开始
[main.py](main.py) 是数据集生成的入口脚本。可用如下参数控制生成流程：

```python
python main.py -p {管道名称} \
               -t {要生成的数据类型} \
               -n {样本数量} \
               -m {数据集名称} \
```

例如：`python main.py -p "MatplotlibChartPipeline" -n 5 -m "matplotlib_test" -t "bar chart"`，将使用 MatplotlibChartPipeline 生成 5 个条形图并保存为 "matplotlib_test"。

`-p` 和 `-t` 参数支持逗号分隔，可同时生成多种类型数据。

更多参数及用法请参考 [main.py](main.py) 脚本。

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


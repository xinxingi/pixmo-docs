NUM_TOPICS = 5


GENERATE_DIAGRAM_TOPICS_PROMPT = {
"English":"""You are an expert in diagram design and have a broad knowledge of different topics.
My persona is: "{persona}"
I want you to generate {num_topics} topics for {figure_type} that I will be interested in or I may see during my daily life given my persona.

Here are the requirements:
1. Each topic is a high-level summary of the contents in {figure_type} with some design details, e.g., "the utility bill for the month of January 2022 with a detailed breakdown of charges".
2. The topics should be diverse to help me generate varied diagrams. Each topic should be unique and not overlap with others.
3. The topics are conditioned on the diagram type. Please ensure the topics you provided can be best visualized in "{figure_type}".
4. All topics must be in English, even if the persona is non-English.
5. List {num_topics} topics for "{persona}" and separate them with a | character, e.g., topic1 | topic2 | ...... | topic{num_topics}.
Do not include any additional text at the beginning or end of your response.""",

"Chinese":"""您是图表设计专家，并且对不同主题拥有广泛的了解。
我的角色是：“{persona}”
我希望您为 {figure_type} 生成 {num_topics} 个我感兴趣或可能在日常生活中看到的主题，这些主题与我的角色相关。

要求如下：
1. 每个主题都是 {figure_type} 内容的高级摘要，并包含一些设计细节，例如“2022 年 1 月的水电费账单，其中包含详细的费用明细”。
2. 主题应多样化，以便我生成各种图表。每个主题都应独一无二，且不能与其他主题重叠。
3. 主题取决于图表类型。请确保您提供的主题在“{figure_type}”中能够最佳地可视化。
4. 所有主题都必须使用中文，即使角色不是中文的。
5. 列出“{persona}”的 {num_topics} 个主题，并用 | 分隔。字符，例如，topic1 | topic2 | ...... | topic{num_topics}。
请勿在回复的开头或结尾添加任何其他文本。"""
}




GENERATE_DIAGRAM_DATA_JSON_PROMPT = {
"English":""""You are an expert in diagram design and have broad knowledge about various topics.
My persona is: "{persona}"
I need some elements about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The elements should be related to the topic and customized according to my persona. Its structure must be suitable for the {figure_type}.
2. The elements should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
3. Do not provide too many elements. Just provide key pieces of information that are essential for the diagram. 
4. The text for each node/edge should be concise and not too long, which can be easily understood by the viewers.
5. All elements must be in English, even if the persona is non-English.
Please provide the elements in JSON format without additional text at the beginning or end.""",

"Chinese":""""
您是图表设计专家，并且对各种主题都有广泛的了解。
我的角色是："{persona}"
我需要一些关于"{topic}"的元素，用于生成一个{figure_type}。

要求如下：
1. 元素应与主题相关，并根据我的角色进行定制，结构必须适合{figure_type}。
2. 元素应切合实际，内容应使用真实世界的实体命名，请勿使用占位符。
3. **节点数量控制**：生成4-8个节点为最佳，确保有足够节点支撑多起点多终点结构。
4. 每个节点的文本应简洁明了（4-8个字为宜），便于理解和显示。
5. 所有元素都必须使用中文。

6. **多起点多终点结构设计（核心要求）**：
   - **必须设计至少2个起始节点**（入度为0的节点）
   - **必须设计至少2个结束节点**（出度为0的节点）
   - 中间节点形成汇聚、分流或交叉连接
   - 避免单一线性链条结构（A→B→C→D这种）
   - 推荐结构模式：
     * 并行汇聚型：A→C，B→C，C→D，C→E
     * 交叉网络型：A→C，A→D，B→C，B→E
     * 分层扇形：A→C，B→C，C→D，C→E，C→F
     * 菱形结构：A→C，B→C，C→D，D→E，D→F

7. **连接关系验证**：
   - 统计每个节点的入度和出度
   - 确保至少2个节点入度=0（起点）
   - 确保至少2个节点出度=0（终点）
   - 避免孤立节点（既无输入也无输出）

8. **布局友好性**：设计时考虑最终图表应接近正方形或3:2的长宽比，多起点应水平分布，多终点应水平对齐。

严格按照以下JSON格式输出，不得有任何偏差：
{{
  "nodes": [
    {{
      "id": "node1",
      "label": "节点标题",
      "description": "节点描述",
      "node_type": "start|middle|end"
    }}
  ],
  "edges": [
    {{
      "from": "node1",
      "to": "node2",
      "label": "连接描述"
    }}
  ],
  "node_count": 6,
  "structure_type": "multi_start_end",
  "start_nodes": ["node1", "node2"],
  "end_nodes": ["node5", "node6"],
  "structure_validation": {{
    "start_count": 2,
    "end_count": 2,
    "is_multi_path": true
  }}
}}

注意：
- node_type字段标识节点类型：start（起点）、middle（中间）、end（终点）
- start_nodes和end_nodes数组明确标识起点和终点节点ID
- structure_validation用于验证结构是否符合多起点多终点要求
- 强制要求：start_count ≥ 2, end_count ≥ 2

请严格按照此格式输出JSON，开头和结尾不得包含任何额外文本。
"""
}




GENERATE_DIAGRAM_QA_PROMPT = {"English":""""You are an expert in data analysis and good at asking questions about diagrams.
My persona is: "{persona}"
I want you to generate some question-answer pairs of a {figure_type} about {topic}, which I would ask.
Instead of showing the figure, I provide the data and the code that generates the figure.

Here is the data:
<data>
{data}
</data>

Here is the code that generates the figure:
<code>
{code}
</code>

Please come up with a list of *reasonable questions* that people will ask when they see the rendered figure. Here are the requirements:
1. **Question Style**: The questions must be natural and related to the figure, which can help interpret the data and understand the insights.
    (1) The questions vary in complexity. Some are easy to answer by just referring to the figure, and some are challenging and require multiple-step reasoning.
    (2) The questions should be answerable based on the *visual information* in the figure. Don't include any coding details in the questions since this type of information is not visible in the figure.

2. **Question Types**: Most questions are short-answer, but some can be multiple-choice, yes/no, or summary questions. You can use the following types:
    (1) Short-answer: At least 5 short-answer questions.
    (2) Multiple-choice: There should be at least two multiple-choice questions. The number of options can be 3, 4, 5, or more. The option labels can be different types: alphabet, Arabic numerals, or Roman numerals. The correct option should be different in each question.
    (3) Yes/No (True/False): At least 1 binary question.
    (4) Summary: At least 1 summary question that asks for describing the *entire figure* or writing a caption for the figure.
    (5) Unanswerable: At least 1 question cannot be answered based on the visual information in the figure. The answer to this question can be "Cannot be determined", "Not enough information", "I don't know", etc.

3. **Provide Explanations**: In addition to a *concise answer* for each question, provide an explanation that details the reasoning steps to reach the answer. For the summary question, the explanation is a more detailed description of the figure.

4. **Response Format**: separate the question, answer, and explanation with a | character: question | answer | explanation. The question-answer pairs should be separated by double newlines (\n\n).
For example:
what's the difference between A and B? | 15 | A is 10 and B is 25, so the difference is 25-10=15

Which group has the highest value? A. Group-1 B. Group-2 C. Group-3 | B | Group-1 is 20, Group-2 is 25, and Group-3 is 15, so Group-2 has the highest value.

... ...

Do not include any additional text at the beginning or end of your response.""",

"Chinese":""""
您是数据分析专家，并且擅长就图表提问。
我的角色是：“{persona}”
我希望您生成一些关于{topic}的{figure_type}问答对，我会问这个问题。
我不会展示图表，而是提供数据和生成图表的代码。

数据如下：
<data>
{data}
</data>

生成图表的代码如下：
<code>
{code}
</code>

请列出一系列*合理的问题*，以便人们在看到渲染后的图表时会提出这些问题。要求如下：
1. **提问风格**：问题必须自然流畅，并与图表相关，有助于解读数据并理解其中的见解。
(1) 问题的复杂程度各不相同。有些问题只需参考图即可轻松回答，而有些问题则颇具挑战性，需要多步推理。
(2) 问题应该能够基于图表中的*视觉信息*进行回答。请勿在问题中包含任何编码细节，因为此类信息在图中不可见。

2. **问题类型**：大多数问题为简答题，但有些问题可以是多项选择题、是非题或总结题。您可以使用以下类型：
(1) 简答题：至少 5 道简答题。
(2) 多项选择题：至少应有两道多项选择题。选项数量可以是 3、4、5 或更多。选项标签可以是不同的类型：字母、阿拉伯数字或罗马数字。每个问题的正确选项应该不同。
(3) 是/否（真/假）：至少 1 道二元题。
(4) 总结题：至少 1 道总结题，要求描述*整个图形*或为图形撰写标题。
(5) 无法回答：至少 1 道题无法根据图中的视觉信息进行回答。这个问题的答案可以是“无法确定”、“信息不足”、“我不知道”等等。

3. **提供解释**：除了每个问题的*简洁答案*外，还要提供详细说明得出答案的推理步骤的解释。对于总结性问题，解释是对图表的更详细描述。

4. **答案格式**：用 | 字符分隔问题、答案和解释：问题 | 答案 | 解释。问答对之间应使用双换行符 (\n\n) 分隔。
例如：
A 和 B 之间的差是多少？| 15 | A 是 10，B 是 25，所以差值为 25-10=15

哪一组的值最高？A. 组 1 B. 组 2 C. 组 3 | B | 组 1 是 20，组 2 是 25，组 3 是 15，所以组 2 的值最高。

……

请勿在回复的开头或结尾添加任何附加文字。
"""
}




GENERATE_DIAGRAM_QA_SHORT_ANSWER_PROMPT = """You are an expert in data analysis and good at asking questions about diagrams.
My persona is: "{persona}"
I want you to generate some question-answer pairs of a "{figure_type}" about "{topic}", which I would ask.
Instead of showing the diagram, I provide the data and the code that generates the diagram.

<data>
{data}
</data>

<code>
{code}
</code>

Please come up with a list of *reasonable questions* that people will ask when they see the rendered diagram. Here are the requirements:
1. **Question Types**: All questions should be short-answer questions that are answerable based on the visual information in the diagram. All questions can be answered with a single word, phrase, or number. (as short as possible)
    (1) **Descriptive questions** ask for the basic information in the diagram, such as the value of a specific node, the relationship between two nodes, the number of nodes/edges, etc. Try to cover different aspects/locations in the diagram.
    (2) **Reasoning questions** require reasoning over multiple information in the diagram. These questions should be more challenging and require a deeper understanding of the diagram. Usually, you need to iterate through the flow of the diagram and combine multiple pieces of information to answer these questions.
    (3) **Diagram Type-specific questions** are questions that are specific and unique to this diagram type {figure_type}. These questions should be tailored to the content and structure of the diagram.

2. **Provide Explanations**: 
    (1) In addition to a *concise answer* (as short as possible) for each question, provide a *step-by-step explanation* that details the reasoning steps to reach the answer.
    (2) For complex reasoning questions, the explanation should be more detailed and include all the necessary steps.

3. **Response Format**: Use | to separate the question, explanation, and concise answer for each example.
    (1) Follow this format: question | explanation | concise answer, e.g., what's the output of this diagram if the input X=5? | After receiving input X=5, the next node computes X*2=10, then subtracts 3, which results in 10-3=7 | 7
    (2) Separate the question-answer pairs by double newlines (\n\n). question1 | explanation1 | answer1\n\nquestion2 | explanation2 | answer2\n\n...
    (3) Do not provide too many questions, 5-10 questions are enough. Focus on the diversity and quality of the questions with a very detailed explanation for challenging questions.
    (4) The concise answer should be as short as possible and directly answer the question. The answer should be faithful and exactly the same as what you would expect to see in the diagram, don't rephrase it. All words in the answer should be processed in natural language, no coding terms/characters.

Please follow the format strictly and do not include any additional text at the beginning or end of your response."""





GENERATE_DIAGRAM_CODE_GRAPHVIZ_PROMPT = """You are an expert in graph design and good at writing code (Python `graphviz`) to generate diagrams.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (JSON format, already loaded as a dictionary):
<data>
{data}
</data>

Please define a Python function (using `graphviz`) called `generate_diagram` that generates a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the arguments (e.g., font, color, marker, etc) to make the diagram more visually appealing and informative.
    (2) Consider the **scale of data** to select the appropriate design scale (canvas size, node/edge, font/marker size, etc) to ensure all information in the diagram is clear and easy to understand, with no text overlapping etc.

2. **Code Requirements**: create a function called `generate_diagram` that generates the diagram using `graphviz` and returns the diagram as a PIL Image object.
    (1) The data, which is loaded as a dictionary is provided as the first argument for the function. The function has no other arguments. You may need to adjust the data format or hardcode some data to fit the `graphviz` API.
    (2) Remember to import necessary libraries (e.g., `import numpy as np`, `import graphviz`, etc) at the beginning of the script.
    (3) The `generate_diagram` function should save the diagram to a BytesIO and then return the diagram as a PIL Image object. **Do not close the BytesIO object.**
    (4) Only define the function and do not call it. Do not show the diagram. Save the diagram with appropriate resolution. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script, your whole response should be the Python code which can be directly executed."""




GENERATE_DIAGRAM_CODE_LATEX_PROMPT = """You are an expert in data analysis and good at writing LaTeX code to generate diagrams and graphs.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (JSON format):
<data>
{data}
</data>

Please write a LaTeX script to generate a {figure_type} using the data provided. Here are the requirements:
Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, marker, etc) to make the graph style unique. You can use common LaTeX packages such as ones that help with tables (booktabs, etc.), figures (pgfplots, etc.), and drawings (tikz, etc.).
    (2) Consider the **scale of data** to select the appropriate design scale (diagram size, node/edge size, etc) to ensure the information in the diagram is clear and easy to understand, with no text overlapping, etc.

2. **Code Requirements**: You can use any LaTeX package to generate the diagram.
    (1) You need to hardcode the provided data into the LaTeX script to generate the diagram. Be careful with the syntax and formatting of the LaTeX script.
    (2) Use `standalone` LaTeX document class to generate the table and add some border margin (`[border=xxpt]`). **Do not add the page number.**
    (3) Carefully organize the layout to ensure no overlapping text or elements in the diagram.

3. **Output Requirements**:
    Put ```latex at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the LaTeX code, which can be directly executed."""




GENERATE_DIAGRAM_CODE_MERMAID_PROMPT = {"English":""""You are an expert in data analysis and good at writing Mermaid code to generate diagrams and graphs.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data:
<data>
{data}
</data>

Please write a Mermaid code to generate a {figure_type} using the data provided. Here are the requirements:
Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, marker, etc) to make the graph style unique.
    (2) Consider the **scale of data** to select the appropriate design scale (diagram size, node/edge size, etc) to ensure the information in the diagram is clear and easy to understand, with no text overlapping, etc.

2. **Code Requirements**:
    (1) You need to hardcode the provided data into the Mermaid script to generate the diagram. Be careful with the syntax and formatting of the Mermaid script. You can reformat or select a subset of the data to fit the Mermaid syntax.
    (2) Choose appropriate Mermaid types based on the diagram type and data. Available types include: flowchart, sequenceDiagram, classDiagram, stateDiagram, erDiagram, gantt, journey, quadrantChart, mindmap, timeline, etc.
    (3) Do not try to add icons or images to the diagram. Only use the built-in Mermaid features. Don't use any style syntax in the Mermaid code.

3. **Output Requirements**:
    Put ```mermaid at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the Mermaid code, which can be directly executed.""",

"Chinese":""""
角色定位：您是一位数据分析与可视化专家，精通Mermaid语法，能够根据数据特征智能选择最适合的Mermaid图表类型。基于提供的 {data} 数据，以 {persona} 的视角，针对 {topic} 主题，生成一个 {figure_type} 类型的Mermaid图表。

核心任务参数：
- 用户角色: {persona}
- 分析主题: {topic}  
- 目标图表: {figure_type}
- 数据源: {data}

1. **多起点多终点结构强化要求**：
- 严格遵循数据中的多起点多终点设计
- 起始节点应在图表顶部或左侧水平分布
- 结束节点应在图表底部或右侧水平对齐
- 中间节点形成有机的汇聚、分流或交叉连接
- 避免将多起点强制合并为单一入口
- 避免将多终点强制汇聚为单一出口

2. 数据关系类型映射（针对多路径结构优化）：
- 多流程数据 → flowchart TD/LR (垂直/水平流程图，最适合多起点多终点)
- 并行处理数据 → flowchart TB (自上而下流程图)
- 网络关系数据 → graph TD/LR (有向图)
- 决策分支数据 → flowchart (决策流程图)
- 状态转换数据 → stateDiagram (状态图，支持多起点多终点)

3. **多路径布局优化策略**：
垂直布局 (推荐用于多起点多终点)：
flowchart TD
    A[起点1] --> C[汇聚点]
    B[起点2] --> C
    C --> D[分流点]
    D --> E[终点1]
    D --> F[终点2]

水平布局：
flowchart LR
    A[起点1] --> C[中转]
    B[起点2] --> D[中转]
    C --> E[终点1]
    D --> F[终点2]

网络型布局：
graph TD
    A[起点1] --> C[节点C]
    A --> D[节点D]
    B[起点2] --> C
    B --> E[节点E]
    C --> F[终点1]
    D --> F
    E --> G[终点2]

4. **路径完整性验证**：
- 确保每个起点都有至少一条通往某个终点的路径
- 确保每个终点都能从至少一个起点到达
- 避免创建孤立的子图或断链
- 保持网络的连通性和逻辑性

5. 样式设计原则：
创意与美观：
- 起点节点使用醒目样式（如圆角矩形）
- 终点节点使用特殊形状标识（如椭圆或六边形）
- 中间节点保持统一但区别于起终点
- 根据数据主题选择合适的配色方案

规模适配：
- 小数据集(≤6项): 突出每个节点，清晰展示多路径
- 中数据集(7-12项): 合理分组，避免路径交叉混乱
- 大数据集(>12项): 采用分层策略，必要时合并相似节点

6. 技术实现要求：
代码规范：
- 硬编码所有数据到Mermaid脚本中
- 禁止使用样式语法(style, classDef等)
- 禁止添加图标或外部图像
- 只使用Mermaid内置功能
- 节点内容禁止使用\n，使用Mermaid多行语法

多路径语法：
- 正确处理多个起点的连接语法
- 确保终点节点不再有出边
- 验证所有连接的语法正确性

7. 输出格式：
仅输出可直接执行的纯净Mermaid代码
在脚本开头加上```mermaid，在脚本结尾加上```
输出内容应该是完整的Mermaid代码块，展现清晰的多起点多终点结构
代码必须语法正确，可直接执行，并完美体现多路径并行处理的业务逻辑
"""
}



DIAGRAM_QUESTION_TYPES = [
    "Basic: Ask for basic visual elements in the figure such as title, axis, ticks, colors, number of data points, etc.",
    "Visual: Ask about the visual attributes such as color, height, and length of graphical marks (e.g., bars) in the chart.",
    "Compositional: contains two mathematical/logical operations like sum, diference, average, median, etc.",
    "Compositional: contains three mathematical/logical operations like sum, diference, average, median, etc.",
    "Compositional: contains four mathematical/logical operations like sum, diference, average, median, etc.",
    "Compositional: contains five or more mathematical/logical operations like sum, diference, average, median, etc.",
    "Comparison: Ask about the relationship between two or more data points.",
    "Comparison: Ask about the relationship between three or more groups.",
    "Comparison: Ask about the relationship between four or more groups.",
    "Comparison: Ask about the relationship among all groups.",
    "Comparison: compare the data points under specific conditions.",
    "Data Retrieval: Ask for specific data points or values in the figure.",
    "Data Retrieval: Ask for some extreme (highest/lowest) data points or values in the figure.",
    "Data Retrieval: Ask for some non-extreme (somewhere in the middle) data points or values in the figure.",
    "Data Retrieval: Ask for the data points or values that meet specific conditions.",
    "Data Retrieval: Ask for the critical points (e.g., turning points, intersection, changing trend, etc) in the figure.",
    "Reasoning: Ask for a question requiring multi steps of reasoning to answer.",
    "Reasoning: Ask for a question requiring two steps of reasoning to answer.",
    "Reasoning: Ask for a question requiring three steps of reasoning to answer.",
    "Reasoning: Ask for a question requiring four steps of reasoning to answer.",
    "Reasoning: Ask for a question requiring five steps of reasoning to answer.",
    "Structure: Ask about the structure of the data or the figure.",
    "Counting: count the number of data points or groups or elements in the figure.",
    "Counting: count the number of data points under specific conditions.",
    "Trend: Ask about the trend or pattern in the figure.",
    "Layout: Ask about the layout or arrangement of the elements (e.g., subplots) in the figure.",
    "Visual Reasoning: parsing the visual information in the figure, such as line intersection, comparison of areas/hights, etc.",
    "Fact Checking: given a statement, ask if it is true or false based on the figure.",
    "Yes/No: Ask a binary question that can be answered with yes or no.",
    "Yes/No: Ask a binary question that can be answered with yes or no with multi-step reasoning.",
    "Multiple Choice: Ask a multiple-choice question with hard negative options.",
    "Multiple Choice: Ask a multiple-choice question with 3-8 options.",
    "Multiple Choice: Ask a multiple-choice question with 4 options.",
    "Multiple Choice: Ask a multiple-choice question with more than 4 options.",
    "Long question: the question is long with detailed context and requires reasoning to answer.",
    "Short question: the question is short and can be answered directly by taking a glance at the figure.",
    "Annotations: Ask about annotations in the figure, such as text notes, highlights, or arrows pointing to specific parts.",
    "Interaction: Ask about interactions between different variables in the chart.",
]
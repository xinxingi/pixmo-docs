NUM_TOPICS = 5




GENERATE_TABLE_TOPICS_PROMPT = """You are an expert in data analysis and have a broad knowledge of different topics.
My persona is: "{persona}"
I want you to generate {num_topics} topics for {figure_type} that I will be interested in or I may see during my daily life given my persona.

Here are the requirements:
1. Each topic is a high-level summary of tabular data, e.g., "Sales data of a grocery store in 2021 Q1".
2. The topics should be diverse to help me generate varied tables. Each topic should be unique and not overlap with others.
3. The topics are conditioned on the table type. Please ensure the topics you provided can be best visualized in "{figure_type}".
4. All topics must be in English, even if the persona is non-English.
5. List {num_topics} topics for "{persona}" and separate them with a | character, e.g., topic1 | topic2 | ...... | topic{num_topics}.
Do not include any additional text at the beginning or end of your response."""




GENERATE_TABLE_DATA_PROMPT = """You are an expert in data analysis and have broad knowledge about various topics.
My persona is: "{persona}"
I need some data about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The data structure must be suitable for the {figure_type}.
2. The contents are related to the topic and customized according to my persona.
3. The data should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
4. The data should be diverse and contain multiple data points to ensure the table is informative.
5. Do not provide too much data. Just necessary data points to satisfy the topic and figure type.
6. All data must be in English, even if the persona is non-English.
Please provide the data in CSV format without additional text at the beginning or end."""




GENERATE_TABLE_DATA_JSON_PROMPT = """You are an expert in data analysis and have broad knowledge about various topics.
My persona is: "{persona}"
I need some data about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The data structure must be suitable for the {figure_type}.
2. The contents are related to the topic and customized according to my persona.
3. The data should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
4. The data should be diverse and contain multiple data points to ensure the table is informative.
5. Do not provide too much data. Just necessary data points to satisfy the topic and figure type.
6. All data must be in English, even if the persona is non-English.
Please provide the data in JSON format without additional text at the beginning or end."""




GENERATE_TABLE_QA_PROMPT = """You are an expert in data analysis and good at asking questions about tables.
My persona is: "{persona}"
I want you to generate some question-answer pairs of a "{figure_type}" about "{topic}", which I would ask.
Instead of showing the table, I provide the data and the code that generates the table.

<data>
{data}
</data>

<code>
{code}
</code>

Please come up with a list of *reasonable questions* that people will ask when they see the rendered table. Here are the requirements:
1. **Question Style**: The questions must be natural and related to the table, which can help interpret the data and understand the insights.
    (1) The questions vary in complexity. Some are easy to answer by just referring to the table, and some are challenging and require multiple-step reasoning.
    (2) The questions should be answerable based on the *visual information* in the table. Don't include any coding details in the questions since this type of information is not visible in the figure.

2. **Question Types**: All questions should be short-answer questions that are answerable based on the visual information in the table.
    (1) **Retrieval questions** ask for specific values or facts in the table (keep the exact same format in the table). Some easy questions can be answered directly from the table. Some more challenging questions may require combining and filtering information from multiple rows or columns.
    (2) **Compositional questions** contain multiple mathematical/logical operations like sum, difference, and average, median, etc.
    (3) **Fact-based questions** ask for whether a specific fact is yes or no (true of false) based on the data. Make sure to have balanced numbers of yes/no questions.
    (4) **Complex reasoning questions** require multiple steps reasoning over multiple data points in the table. These questions should be more challenging and require a deeper understanding of the data.

3. **Provide Explanations**: 
    (1) In addition to a *concise answer* (as short as possible) for each question, provide a *step-by-step explanation* that details the reasoning steps to reach the answer.
    (2) For complex reasoning questions, the explanation should be more detailed and include all the necessary steps.

4. **Response Format**: Use | to separate the question, explanation, and concise answer for each example. 
    (1) Follow this format: question | explanation | concise answer, e.g., what's the average value of group A? | There are 5 data points in group A, sum them up is (34 + 45 + 23 + 56 + 12) = 170, so the average is 170/5 = 34 | 34
    (2) Separate the question-answer pairs by double newlines (\n\n). question1 | explanation1 | answer1\n\nquestion2 | explanation2 | answer2\n\n...
    (3) Do not provide too many questions, 5-10 questions are enough. Focus on the diversity and quality of the questions with a very detailed explanation for challenging questions.
    (4) The concise answer should be as short as possible and directly answer the question. All words in the response should be processed in natural language, no coding terms and remove any unnecessary characters.

Please follow the format strictly and do not include any additional text at the beginning or end of your response."""




GENERATE_TABLE_CODE_LATEX_PROMPT = """You are an expert in data analysis and good at writing LaTeX code to generate tables.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (JSON format):
<data>
{data}
</data>

Please write a LaTeX script to generate a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, border, shade, etc) to make the table style unique.
    (2) Select appropriate design, layout and margin, ensuring the table is saved with all the elements visible, clear and easy to understand, with no text overlapping, etc.
    (3) Do not use white text color or other light colors on a white background, e.g., when row color is white, use a dark text color.

2. **Code Requirements**:
    (1) You need to hardcode the provided data into the LaTeX script to generate the table. Be careful with the syntax and formatting of the LaTeX script.
    (2) Use `standalone` LaTex document class to generate the table and add some border margin (`[border=xxpt]`). **Do not add the page number.**

3. **Output Requirements**:
    Put ```latex at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the LaTex code, which can be directly executed."""




GENERATE_TABLE_CODE_MATPLOTLIB_PROMPT = """You are an expert in data analysis and good at writing code (Python `pandas`) to generate tables.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (CSV format, already loaded as a pd.DataFrame):
<data>
{data}
</data>

Please define a Python function (using `pandas`) called `generate_table` that generates a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, border, shade, etc) to make the table style unique. Set the style by using `plt.style.use('{style_name}')`.
    (2) Select the appropriate design scale (e.g., column width) to ensure the information in each cell is clear and easy to understand, with no text overlapping, etc.

2. **Code Requirements**: create a function called `generate_table` that generates the table using `pandas`.
    (1) The data, which is loaded as a pd.DataFrame is provided as the first argument for the function. The function has no other arguments. You may need to adjust the data format based on the requirements and your design.
    (2) Remember to import necessary libraries (e.g., `import numpy as np`, `import pandas as pd`, `import matplotlib.pyplot as plt`, etc) at the beginning of the script.
    (3) The `generate_table` function should save the table to a BytesIO and then return the table as a PIL Image object. **Do not close the BytesIO object.**
    (4) Select appropriate margins, resolution, and tight layout, ensuring the table is saved with all the elements visible.
    (5) Only define the function and do not call it. Do not show the table. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the Python code, which can be directly executed."""




GENERATE_TABLE_CODE_PLOTLY_PROMPT = """You are an expert in data analysis and good at writing code (Python `plotly`) to generate tables.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (CSV format, already loaded as a pd.DataFrame):
<data>
{data}
</data>

Please define a Python function (using `plotly`) called `generate_table` that generates a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, border, shade, etc) to make the table style unique.
    (2) Select the appropriate design scale (e.g., column width) to ensure the information in each cell is clear and easy to understand, with no text overlapping, etc.

2. **Code Requirements**: create a function called `generate_table` that generates the table using `plotly`. Do not use matplotlib or other libraries.
    (1) The data, which is loaded as a pd.DataFrame is provided as the first argument for the function. The function has no other arguments. You may need to adjust the data format to fit the `plotly` specification.
    (2) Remember to import necessary libraries (e.g., `import numpy as np`, `import plotly.express as px`) at the beginning of the script.
    (3) The `generate_table` function should save the table to a BytesIO and then return the table as a PIL Image object. **Do not close the BytesIO object.**
    (4) Select appropriate margins and tight layout, ensuring the table is saved with all the elements visible.
    (5) Only define the function and do not call it. Do not show the table. Save the table with enough resolution to be clearly visible. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the Python code, which can be directly executed."""




GENERATE_TABLE_CODE_HTML_PROMPT = """You are an expert web designer and are good at writing HTML to create tables.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here are the materials (JSON format):
<data>
{data}
</data>

Please use HTML and CSS to generate a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**: Feel free to use any CSS framework, libraries, JavaScript plugins, or other tools to create the table.
    (1) Try to be creative and make the web page style, fonts, colors, borders and visual layout unique with CSS. Taking persona, topic, and table type into consideration when designing the table.
    (2) Select the appropriate design scale (e.g., collumn width, cell size, margins, etc) to ensure the information in the table is clear and easy to understand, with no text overlapping etc.

2. **Code Requirements**: 
    (1) You need to hardcode the provided data into the HTML script to generate the document. Be careful with the syntax and formatting of the HTML script.
    (2) Put everything in one HTML file. Do not use external CSS or JavaScript files.

3. **Output Requirements**:
    Put ```html at the beginning and ``` at the end of the script to separate the code from the text.

Please don't answer with any additional text in the script, your whole response should be the HTML code which can be directly executed."""
NUM_TOPICS = 5




GENERATE_CHART_TOPICS_PROMPT = """You are an expert in data analysis and have a broad knowledge of different topics.
My persona is: "{persona}"
I want you to generate {num_topics} topics for {figure_type} that I will be interested in or I may see during my daily life given my persona.

Here are the requirements:
1. Each topic is a high-level summary of statistical distribution with some details, e.g., "population growth in the US with a breakdown of the age groups."
2. The topics should be diverse to help me generate varied figures. Each topic should be unique and not overlap with others.
3. The topics are conditioned on the figure type. Please ensure the topics you provided can be best visualized in "{figure_type}".
4. All topics must be in English, even if the persona is non-English.
5. List {num_topics} topics for "{persona}" and separate them with a | character, e.g., topic1 | topic2 | ...... | topic{num_topics}.
Do not include any additional text at the beginning or end of your response."""




GENERATE_CHART_DATA_PROMPT = """You are an expert in data analysis and have broad knowledge about various topics.
My persona is: "{persona}"
I need some data about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The data structure must be suitable for the {figure_type}.
2. The contents are related to the topic and customized according to my persona.
3. The data should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
4. The data should be diverse and contain multiple data points to ensure the chart is informative.
5. Do not provide too much data. Just necessary data points to satisfy the topic and figure type.
6. All data must be in English, even if the persona is non-English.
Please provide the data in CSV format without additional text at the beginning or end."""




GENERATE_CHART_DATA_JSON_PROMPT = """You are an expert in data analysis and have broad knowledge about various topics.
My persona is: "{persona}"
I need some data about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The data structure must be suitable for the {figure_type}.
2. The contents are related to the topic and customized according to my persona.
3. The data should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
4. The data should be diverse and contain multiple data points to ensure the chart is informative.
5. Do not provide too much data. Just necessary data points to satisfy the topic and figure type.
6. All data must be in English, even if the persona is non-English.
Please provide the data in JSON format without additional text at the beginning or end."""




GENERATE_CHART_QA_PROMPT = """You are an expert in data analysis and good at asking questions about plots.
My persona is: "{persona}"
I want you to generate some question-answer pairs of a {figure_type} about {topic}, which I would ask.
Instead of showing the figure, I provide the data and the code that generates the figure.

<data>
{data}
</data>

<code>
{code}
</code>

Please come up with a list of *reasonable questions* that people will ask when they see the rendered figure. Here are the requirements:
1. **Question Style**: The questions must be natural and related to the figure, which can help interpret the data and understand the insights.
    (1) The questions vary in complexity. Some are easy to answer by just referring to the figure, and some are challenging and require multiple-step reasoning.
    (2) The questions should be answerable based on the *visual information* in the figure. Don't include any coding details in the questions since this type of information is not visible in the figure.

2. **Question Types**: All questions should be short-answer questions that are answerable based on the visual information in the figure.
    (1) **Basic questions** ask for basic elements in the figure such as visual appearance, title, axis, ticks, colors, number of data points, etc. Remeber to use **natural language** when referring to these elements, do not use coding terms (RGB, HEX, etc.).
    (2) **Compositional questions** contain at least two mathematical/logical operations like sum, difference, and average, e.g., "What's the median value of group A?". Generate questions using different numbers and types of operations.
    (3) **Comparison questions** ask about the relationship between two or more data points, e.g., "Which group has the highest value?". Generate questions using different comparison operators (greater than, less than, equal to, etc.) and data points.
    (4) **Chart-Type Specific questions** are unique to the figure type of {figure_type}.

3. **Provide Explanations**: 
    (1) In addition to a *concise answer* (as short as possible) for each question, provide a *step-by-step explanation* that details the reasoning steps to reach the answer.
    (2) For complicated questions, provide a **more detailed explanation** to break down the problem-solving process.

4. **Response Format**: Use | to separate the question, explanation, and concise answer for each example. 
    (1) Follow this format: question | explanation | concise answer, e.g., what's the average value of group A? | There are 5 data points in group A, sum them up is (34 + 45 + 23 + 56 + 12) = 170, so the average is 170/5 = 34 | 34
    (2) Separate the question-answer pairs by double newlines (\n\n). question1 | explanation1 | answer1\n\nquestion2 | explanation2 | answer2\n\n...
    (3) Do not provide too many questions, 5-10 questions are enough. Focus on the diversity and quality of the questions with a very detailed explanation for challenging questions.
    (4) The concise answer should be as short as possible and directly answer the question. All words in the response should be processed in natural language, no coding terms and remove any unnecessary characters.
    
Please follow the format strictly and do not include any additional text at the beginning or end of your response."""




GENERATE_CHART_CODE_MATPLOTLIB_PROMPT = """You are an expert in data analysis and good at writing code (Python `matplotlib`) to generate plots.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (CSV format, already loaded as a pd.DataFrame):
<data>
{data}
</data>

Please define a Python function (using `matplotlib`) called `generate_plot` that generates a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the arguments (e.g., font, color, marker, etc) to make the plot look unique. Set the style by using `plt.style.use('{style_name}')`.
    (2) Consider the **scale of data** to select the appropriate design scale (axis range, figure size, font/marker size, etc) to ensure the information in the plot is clear and easy to understand, with no text overlapping etc.

2. **Code Requirements**: create a function called `generate_plot` that generates the chart using `matplotlib`.
    (1) The data, which is loaded as a pd.DataFrame is provided as the first argument for the function. The function has no other arguments. You may need to adjust the data format or hard code some data to fit the `matplotlib` specification.
    (2) Remember to import necessary libraries (e.g., `import numpy as np`, `import matplotlib.pyplot as plt`) at the beginning of the script.
    (3) The `generate_plot` function should save the plot to a BytesIO and then return the plot as a PIL Image object. **Do not close the BytesIO object.**
    (4) Use `bbox_inches='tight'` argument in `savefig` or `plt.tight_layout()`, ensuring the plot is saved with all the elements (title, labels, etc) visible.
    (5) Only define the function and do not call it. Do not show the plot. Save the plot with appropriate resolution. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script, your whole response should be the Python code which can be directly executed."""




GENERATE_CHART_CODE_PLOTLY_PROMPT = """You are an expert in data analysis and good at writing code (Python `plotly`) to generate plots.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (CSV format, already loaded as a pd.DataFrame):
<data>
{data}
</data>

Please define a Python function (using `plotly`) called `generate_plot` that generates a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, marker, etc) to make the plot style unique.
    (2) Consider the **scale of data** to select the appropriate design scale (axis range, figure size, font/marker size, etc) to ensure the information in the plot is clear and easy to understand, with no text overlapping etc.

2. **Code Requirements**: create a function called `generate_plot` that generates the chart using `plotly`. Do not use matplotlib or other libraries.
    (1) The data, which is loaded as a pd.DataFrame is provided as the first argument for the function. The function has no other arguments. You may need to adjust the data format to fit the `plotly` specification.
    (2) Remember to import necessary libraries (e.g., `import numpy as np`, `import plotly.express as px`) at the beginning of the script.
    (3) The `generate_plot` function should save the plot to a BytesIO and then return the plot as a PIL Image object. **Do not close the BytesIO object.**
    (4) Select appropriate margins and tight layout, ensuring the plot is saved with all the elements (title, labels, etc) visible. Rotate text if necessary to make sure no text overlapping.
    (5) Only define the function and do not call it. Do not show the plot. Save the plot with enough resolution to be clearly visible. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script, your whole response should be the Python code which can be directly executed."""




GENERATE_CHART_CODE_VEGALITE_PROMPT = """You are an expert in data analysis and good at writing Vega-Lite JSON to generate plots.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (JSON format):
<data>
{data}
</data>

Please use Vega-Lite to define a {figure_type} in JSON format using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, marker, etc) to make the plot style unique.
    (2) Consider the **scale of data** to select the appropriate design scale (axis range, figure size, font/marker size, etc) to ensure the information in the plot is clear and easy to understand, with no text overlapping etc.
    (3) Don't use rare fonts or colors that may not be supported by all viewers.

2. **Code Requirements**: define the chart using Vega-Lite (JSON format).
    (1) You need to hardcode the provided data into the JSON to generate the document. Be careful with the syntax and formatting of the Vega-Lite JSON.
    (2) Select appropriate margins and tight layout, ensuring the plot is saved with all the elements (title, labels, etc) visible.
    (3) Don't add actual data numbers in the plot. This is very important. Because you cannot align the data with figure elements.
    (4) If the data contains the year information, format the year correctly in the x-axis.

3. **Output Requirements**:
    Put ```vegalite at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the JSON.

Please don't answer with any additional text in the script, your whole response should be the Vega-Lite JSON which can be directly executed."""




GENERATE_CHART_CODE_LATEX_PROMPT = """You are an expert in data analysis and good at writing LaTex code to generate plots.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (CSV format):
<data>
{data}
</data>

Please write a LaTeX script to generate a {figure_type} using the data provided. Here are the requirements:
Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, marker, etc) to make the plot style unique. You can use common LaTeX packages such as ones that help with tables (booktabs, etc.), figures (pgfplots, etc.), and drawings (tikz, etc.).
    (2) Consider the **scale of data** to select the appropriate design scale (axis range, figure size, font/marker size, etc) to ensure the information in the plot is clear and easy to understand, with no text overlapping, etc.
    (3) Select appropriate margins and tight layout, ensuring the plot is saved with all the elements (title, labels, etc) visible.

2. **Code Requirements**:
    (1) You need to hardcode the provided data into the LaTeX script to generate the plot. Be careful with the syntax and formatting of the LaTeX script.
    (2) Use `standalone` LaTeX document class to generate the chart and add some border margin (`[border=xxpt]`). **Do not add the page number.**

3. **Output Requirements**:
    Put ```latex at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the LaTeX code, which can be directly executed."""




GENERATE_CHART_CODE_HTML_PROMPT = """You are an expert web designer and are good at writing HTML to create charts.
My persona is: "{persona}"
I have some data about {topic} which can be used to generate a {figure_type}.

Here is the data (JSON format):
<data>
{data}
</data>

Please use HTML and CSS to generate a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**: Feel free to use any CSS framework, libraries, JavaScript plugins, or other tools to create the chart.
    (1) Try to be creative and make the web page style, fonts, colors, and visual layout unique with CSS. Taking persona, topic, and figure type into consideration when designing the plot.
    (2) Consider the **scale of data** to select the appropriate design scale (axis range, figure size, font/marker size, etc) to ensure the information in the plot is clear and easy to understand, with no text overlapping etc.
    (3) **Important:** Choose appropriate range of axis depends on the scale of data to ensure the information in the plot is easy to parse.

2. **Code Requirements**: 
    (1) You need to hardcode the provided data into the HTML script to generate the document. Be careful with the syntax and formatting of the HTML script.
    (2) Put everything in one HTML file. Do not use external CSS or JavaScript files. Set higher width of the plot to ensure the plot is clearly visible.

3. **Output Requirements**:
    Put ```html at the beginning and ``` at the end of the script to separate the code from the text.

Please don't answer with any additional text in the script, your whole response should be the HTML code which can be directly executed."""
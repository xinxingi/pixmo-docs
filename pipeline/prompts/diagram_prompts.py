NUM_TOPICS = 5




GENERATE_DIAGRAM_TOPICS_PROMPT = """You are an expert in diagram design and have a broad knowledge of different topics.
My persona is: "{persona}"
I want you to generate {num_topics} topics for {figure_type} that I will be interested in or I may see during my daily life given my persona.

Here are the requirements:
1. Each topic is a high-level summary of the contents in {figure_type} with some design details, e.g., "the utility bill for the month of January 2022 with a detailed breakdown of charges".
2. The topics should be diverse to help me generate varied diagrams. Each topic should be unique and not overlap with others.
3. The topics are conditioned on the diagram type. Please ensure the topics you provided can be best visualized in "{figure_type}".
4. All topics must be in English, even if the persona is non-English.
5. List {num_topics} topics for "{persona}" and separate them with a | character, e.g., topic1 | topic2 | ...... | topic{num_topics}.
Do not include any additional text at the beginning or end of your response."""



GENERATE_DIAGRAM_DATA_JSON_PROMPT = """You are an expert in diagram design and have broad knowledge about various topics.
My persona is: "{persona}"
I need some elements about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The elements should be related to the topic and customized according to my persona. Its structure must be suitable for the {figure_type}.
2. The elements should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc.
3. Do not provide too many elements. Just provide key pieces of information that are essential for the diagram. 
4. The text for each node/edge should be concise and not too long, which can be easily understood by the viewers.
5. All elements must be in English, even if the persona is non-English.
Please provide the elements in JSON format without additional text at the beginning or end."""




GENERATE_DIAGRAM_QA_PROMPT = """You are an expert in data analysis and good at asking questions about diagrams.
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




GENERATE_DIAGRAM_CODE_MERMAID_PROMPT = """You are an expert in data analysis and good at writing Mermaid code to generate diagrams and graphs.
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

Please don't answer with any additional text in the script. Your whole response should be the Mermaid code, which can be directly executed."""
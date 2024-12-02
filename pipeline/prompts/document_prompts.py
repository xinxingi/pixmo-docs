NUM_TOPICS = 5




GENERATE_DOCUMENT_TOPICS_PROMPT = """You are an expert in document generation and have a broad knowledge of different topics.
My persona is: "{persona}"
I want you to generate {num_topics} topics for {figure_type} that I will be interested in or I may see during my daily life given my persona.

Here are the requirements:
1. Each topic is a high-level summary of the contents in {figure_type} with some design details, e.g., "the utility bill for the month of January 2022 with a detailed breakdown of charges".
2. The topics should be diverse to help me generate varied documents. Each topic should be unique and not overlap with others.
3. The topics are conditioned on the document type. Please ensure the topics you provided can be best visualized in "{figure_type}".
4. All topics must be in English, even if the persona is non-English.
5. List {num_topics} topics for "{persona}" and separate them with a | character, e.g., topic1 | topic2 | ...... | topic{num_topics}.
Do not include any additional text at the beginning or end of your response."""




GENERATE_DOCUMENT_DATA_JSON_PROMPT = """You are an expert in content creation and have broad knowledge about various topics.
My persona is: "{persona}"
I need some materials about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The materials should be related to the topic and customized according to my persona. Its structure must be suitable for the {figure_type}.
2. The materials should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc. Do not use template data like [Name], [Date], etc.
3. The materials should be diverse and contain information from different aspects of the topic to ensure the document is informative.
4. Do not provide too many materials. Just provide key pieces of information that are essential for a **one-page document.**
5. All materials must be in English, even if the persona is non-English.
Please provide the materials in JSON format without additional text at the beginning or end."""




GENERATE_DOCUMENT_DATA_JSON_FEW_PROMPT = """You are an expert in content creation and have broad knowledge about various topics.
My persona is: "{persona}"
I need some materials about "{topic}", which can be used to generate a {figure_type}. 
Here are the requirements:
1. The materials should be related to the topic and customized according to my persona. Its structure must be suitable for the {figure_type}.
2. The materials should be realistic, and the contents should be named using real-world entities. Do not use placeholder names like xxA, xxB, etc. Do not use template data like [Name], [Date], etc.
3. The materials should be diverse and contain information from different aspects of the topic to ensure the document is informative.
4. Do not provide too many materials. Just provide key pieces of information that are essential for a **one-page document.**
5. All materials must be in English, even if the persona is non-English.
Please provide the materials in JSON format without additional text at the beginning or end."""




GENERATE_DOCUMENT_QA_PROMPT = """You are an expert in data analysis and good at asking questions about documents.
My persona is: "{persona}"
I want you to generate some question-answer pairs of a {figure_type} about {topic}, which I would ask.
Instead of showing the document, I provide the data and the code that generates the document.

<data>
{data}
</data>

<code>
{code}
</code>

Please come up with a list of *reasonable questions* that people will ask when they see the rendered document. Here are the requirements:

1. **Question Types**: All questions should be short-answer questions that are answerable based on the visual information in the document. All questions can be answered with a single word, phrase, or number. (as short as possible)
    (1) **Information Retrieval questions** ask for specific information in the document, such as numbers, names, dates, titles, etc. The questions should cover different aspects (areas) of the document. This is the most common type of question.
    (2) **Reasoning questions** require reasoning over multiple information in the document. These questions should be more challenging and require a deeper understanding of the document.
    (3) **Document Type-specific questions** are questions that are specific and unique to this document type {figure_type}. These questions should be tailored to the content and structure of the document.

2. **Response Format**: Use | to separate the question, explanation, and concise answer for each example. 
    (1) Follow this format: question | explanation | concise answer, e.g., what is the total revenue? | The total revenue is the sum of all revenue sources in the document, which is $2000 + $3000 + $5000 = $10000. | $10000 
    (2) Separate the question-answer pairs by double newlines (\n\n). question1 | explanation1 | answer1\n\nquestion2 | explanation2 | answer2\n\n...
    (3) Do not provide too many questions, 5-10 questions are enough. Focus on the diversity and quality of the questions. Try to cover different aspects of the document.
    (4) The concise answer should be as short as possible and directly answer the question. The answer should be faithful and exactly the same as what you would expect to see in the document, don't rephrase it. All words in the answer should be processed in natural language, no coding terms/characters.
    
Please follow the format strictly and do not include any additional text at the beginning or end of your response."""




GENERATE_DOCUMENT_CODE_LATEX_PROMPT = """You are an expert in content creation and good at writing LaTeX code to generate documents.
My persona is: "{persona}"
I have some materials about {topic} which can be used to generate a {figure_type}.

Here are the materials (JSON format):
<data>
{data}
</data>

Please write a LaTeX script to generate a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, border, shade, etc) to make the document style unique while taking topics and person into consideration.
    (2) Select the appropriate design, layout, and margin, ensuring the document is saved with all the elements visible, clear, and easy to understand, with no text overlapping, etc.
    (3) All content should be on **one page**. This is very important. Do not make the document too long or too short.

2. **Code Requirements**: Generate a **one-page** document using LaTeX.
    (1) You need to hardcode the provided data into the LaTeX script to generate the document. Be careful with the syntax and formatting of the LaTeX script.
    (2) **Do not use tikzpicture!** Use `pagecolor` instead if you want to change the background color of the page. Most of time, just use white background.
    (3) **Remove page number** from the document. Do not try to insert the example image/figure into the document (e.g., don't use `\includegraphics[]example-image`).

3. **Output Requirements**:
    Put ```latex at the beginning and ``` at the end of the script to separate the code from the text. This will help me easily extract the code.

Please don't answer with any additional text in the script. Your whole response should be the LaTeX code, which can be directly executed."""




GENERATE_DOCUMENT_CODE_HTML_PROMPT = """You are an expert web designer and are good at writing HTML to create documents.
My persona is: "{persona}"
I have some materials about {topic} which can be used to generate a {figure_type}.

Here are the materials (JSON format):
<data>
{data}
</data>

Please use HTML and CSS to generate a {figure_type} using the data provided. Here are the requirements:
1. **Style Requirements**: Feel free to use any CSS framework, libraries, JavaScript plugins, or other tools to create the document.
    (1) Try to be creative and make the web page style, fonts, colors, borders and visual layout unique with CSS. Taking persona, topic, and document type into consideration when designing the document.
    (2) Select the appropriate design scale (e.g., margins, page size, layout, etc) to ensure the information in the document is clear and easy to understand, with no text overlapping etc.
    (3) **Do not make the page too long or too sparse.** All contents should be in **one page**. This is very important.
    
2. **Code Requirements**: 
    (1) You need to hardcode the provided data into the HTML script to generate the document. Be careful with the syntax and formatting of the HTML script.
    (2) Put everything in one HTML file. Do not use external CSS or JavaScript files.

3. **Output Requirements**:
    Put ```html at the beginning and ``` at the end of the script to separate the code from the text.

Please don't answer with any additional text in the script, your whole response should be the HTML code which can be directly executed."""


GENERATE_DOCUMENT_CODE_DOCX_PROMPT = """You are an expert web designer and are good at using `.docx` to create documents.
My persona is: "{persona}"
I have some materials about {topic} which can be used to generate a {figure_type}.

Here are the materials (JSON format, already loaded as a dict):

{data}

Please define a Python function called `generate_document` that generates a {figure_type} using the data provided. Use `python-docx` to define the document and then return the `Document` object.
Here are the requirements:
1. **Style Requirements**:
    (1) Try to be creative and change the default arguments (e.g., font, color, border, page size, etc) to make the document style unique while taking topics and person into consideration.
    (2) Select appropriate design, layout and margin, ensuring the document is saved with all the elements visible, clear and easy to understand, with no text overlapping, etc.

2. **Code Requirements**: create a Python function called `generate_document` that defines the document using `python-docx` and returns the `Document` object.
    (1) The data, which is loaded as a dictionary is provided as the first argument for the function. The function has no other arguments.
    (2) Remember to import necessary libraries (e.g., `from docx import Document`) at the beginning of the script.
    (3) The `generate_document` function should return the `Document` object, e.g., `doc = Document() ... YOUR CODE ... return doc`. Be careful with the syntax and formatting of the `python-docx` script.
    (4) Only define the function and do not call it. Do not show the document. Save the document with enough resolution to be clearly visible. No need to show example usage.

3. **Output Requirements**:
    Put ```python at the beginning and ``` at the end of the script to separate the code from the text.

Please don't answer with any additional text in the script, your whole response should be the Python code which can be directly executed."""
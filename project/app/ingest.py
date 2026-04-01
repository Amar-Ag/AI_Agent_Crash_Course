import io
import zipfile
import requests
import frontmatter
import re
from minsearch import Index, VectorSearch
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import numpy as np


def read_repo_data(repo_owner, repo_name):
    """
    Download and parse all markdown files from a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization
        repo_name: Repository name
    
    Returns:
        List of dictionaries containing file content and metadata
    """
    prefix = 'https://codeload.github.com' 
    url = f'{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main'
    resp = requests.get(url)
    
    if resp.status_code != 200:
        raise Exception(f"Failed to download repository: {resp.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    
    for file_info in zf.infolist():
        filename = file_info.filename
        filename_lower = filename.lower()

        if not (filename_lower.endswith('.md') 
            or filename_lower.endswith('.mdx')):
            continue
    
        try:
            with zf.open(file_info) as f_in:
                content = f_in.read().decode('utf-8', errors='ignore')
                post = frontmatter.loads(content)
                data = post.to_dict()
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data['filename'] = filename_repo
                repository_data.append(data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    zf.close()
    return repository_data

def split_markdown_by_level(text, level=2):
    """
    Split markdown text by a specific header level.
    
    :param text: Markdown text as a string
    :param level: Header level to split on
    :return: List of sections as strings
    """
    # This regex matches markdown headers
    # For level 2, it matches lines starting with "## "
    header_pattern = r'^(#{' + str(level) + r'} )(.+)$'
    pattern = re.compile(header_pattern, re.MULTILINE)

    # Split and keep the headers
    parts = pattern.split(text)
    
    sections = []
    for i in range(1, len(parts), 3):
        # We step by 3 because regex.split() with
        # capturing groups returns:
        # [before_match, group1, group2, after_match, ...]
        # here group1 is "## ", group2 is the header text
        header = parts[i] + parts[i+1]  # "## " + "Title"
        header = header.strip()

        # Get the content after this header
        content = ""
        if i+2 < len(parts):
            content = parts[i+2].strip()

        if content:
            section = f'{header}\n\n{content}'
        else:
            section = header
        sections.append(section)
    
    return sections

def build_sections(docs):
    """
    Build chunks of text from repository data.
    
    Args:
        docs: List of dictionaries containing file content and metadata
    Returns:
        List of text chunks
    """
    repo_chunks = []
    for doc in docs:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop('content')
        sections = split_markdown_by_level(doc_content, level=2)
        for section in sections:
            section_doc = doc_copy.copy()
            section_doc['section'] = section
            repo_chunks.append(section_doc)
    return repo_chunks

def index_data(repo_owner, repo_name):
    """
    Main function to read, process, and build sections from a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization
        repo_name: Repository name
    Returns:
        Indexed and chunked data ready for model ingestion
    """
    repo_data = read_repo_data(repo_owner, repo_name)
    sections = build_sections(repo_data)

    index = Index(
        text_fields=['section', 'filename'], 
        keyword_fields=[]
    )
    index.fit(sections)

    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_embeddings = []
    

    for record in sections:
        text = record['section']
        v_doc = embedding_model.encode(text)
        chunk_embeddings.append(v_doc)

    chunk_embeddings = np.array(chunk_embeddings)

    vindex = VectorSearch()
    vindex.fit(chunk_embeddings, sections)
    return index, vindex, embedding_model
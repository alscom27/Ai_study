import os
from crewai_tools import PDFSearchTool


def save_uploaded_pdf(uploaded_file, save_dir="uploads"):
    """
    Streamlit에서 업로드한 PDF 파일을 로컬에 저장하고 경로 반환

    Args:
        uploaded_file: Streamlit의 file_uploader로 받은 파일 객체
        save_dir (str): 저장할 디렉토리 경로 (기본값: uploads)

    Returns:
        str: 저장된 PDF 파일의 전체 경로
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def get_pdf_search_tool(pdf_path):
    """
    CrewAI에서 사용할 PDFSearchTool 객체 반환

    Args:
        pdf_path (str): 분석할 PDF 파일의 경로

    Returns:
        PDFSearchTool: CrewAI에서 사용할 수 있는 Tool 객체
    """
    return PDFSearchTool(pdf=pdf_path)

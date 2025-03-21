import fitz  # PyMuPDF
import ollama
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedPDF
from .serializers import PDFSerializer

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# API Endpoint to process PDFs
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def process_pdfs(request):
    book_pdf = request.FILES.get('book_pdf')
    question_paper_pdf = request.FILES.get('question_paper_pdf')

    if not book_pdf or not question_paper_pdf:
        return Response({"error": "Both PDFs are required"}, status=400)

    book_instance = UploadedPDF.objects.create(file=book_pdf)
    question_paper_instance = UploadedPDF.objects.create(file=question_paper_pdf)

    book_text = extract_text_from_pdf(book_instance.file.path)
    question_paper_text = extract_text_from_pdf(question_paper_instance.file.path)

    prompt = f"""
    You are an AI assistant. Given the following book content, generate answers for the questions in the question paper.

    Book Content:
    {book_text[:5000]}

    Questions:
    {question_paper_text[:2000]}
    """

    # Generate response using Ollama 
    response = ollama.chat(model="gemma:7b", messages=[{"role": "user", "content": prompt}])

    return Response({"response": response["message"]["content"]})

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ConsultationForm
from .models import Consultation
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.utils import timezone
import socket
from io import BytesIO

def generate_pdf_view(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            patient_last_name = request.POST.get('patient_last_name')
            patient_first_name = request.POST.get('patient_first_name')
            patient_dob = request.POST.get('patient_dob')
            logo_path = "http://127.0.0.1:8000/media/clinic_logos/mrf-logo-1946-present-scaled.webp" 
            clinic_name = request.POST.get('clinic_name')
            consultation_note= request.POST.get('consultation_note')
            chief_complaint = request.POST.get('chief_complaint')
            physician_name = request.POST.get('physician_name')

            # Generate PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=CR_{patient_last_name}_{patient_first_name}_{patient_dob}.pdf'

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

           # Calculate the x position for the top right corner
            x_position = width - 2*inch - 50  # Subtract the image width and some padding from the page width
            y_position = height - 100  # Positioning near the top

            c.drawImage(logo_path, x_position, y_position, width=2*inch, height=0.5*inch)


            # Footer
            footer_text = f"This report is generated on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} from {request.META.get('REMOTE_ADDR', 'Unknown IP')}"
            c.drawString(50, 30, footer_text)

            # Content
            text = c.beginText(50, height - 150)
            text.setFont("Helvetica", 12)
            text.setLeading(14)

            content = (
                f"Clinic Name: {clinic_name}\n"
                f"Physician Name: {physician_name}\n"
                f"Patient Name: {patient_first_name} {patient_last_name}\n"
                f"Date of Birth: {patient_dob}\n"
                f"Chief Complaint: {chief_complaint}\n"
                f"Consultation Note: {consultation_note}"
            )

            text.textLines(content)
            c.drawText(text)

            # Finish PDF
            c.showPage()
            c.save()

            # Get PDF
            pdf = buffer.getvalue()
            buffer.close()
            
            response.write(pdf)
            print("Here is the pdf",  response)
            
            return response
        else:
            print(form.errors)
            return render(request, 'consultation.html')

    return render(request, 'consultation.html')

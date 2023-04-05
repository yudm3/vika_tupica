import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import base64
from reportlab.lib.utils import ImageReader

def on_download_click():
    st.session_state.pdf_downloaded = True
    st.session_state.show_convert_more = True

def image_to_pdf(images, output_buffer):
    pdf = canvas.Canvas(output_buffer, pagesize=letter)
    width, height = letter

    for img in images:
        img_width, img_height = img.size
        img_aspect = img_height / float(img_width)

        if (width / float(height)) < img_aspect:
            pdf_height = height
            pdf_width = pdf_height / img_aspect
        else:
            pdf_width = width
            pdf_height = pdf_width * img_aspect

        x = (width - pdf_width) / 2
        y = (height - pdf_height) / 2

        pdf.drawImage(ImageReader(img), x, y, pdf_width, pdf_height, preserveAspectRatio=True)
        pdf.showPage()

    pdf.save()

def get_image_list(uploaded_images):
    images = []
    for uploaded_image in uploaded_images:
        img = Image.open(uploaded_image)
        images.append(img)
    return images

def get_binary_file_downloader_link(file_buffer, file_name):
    file_buffer.seek(0)
    b64 = base64.b64encode(file_buffer.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download PDF</a>'

st.title(":latin_cross: HGU Image to PDF Converter :point_up_2::wolf:")
st.markdown("---")

image = Image.open('vika.jpg')
st.image(image, caption='Beautiful Vitek in Tomatillos')

uploaded_images = st.file_uploader("Upload your images (jpg, jpeg, png, webp)", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
st.markdown("---")

if uploaded_images:
    images = [Image.open(io.BytesIO(uploaded_file.read())) for uploaded_file in uploaded_images]

    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = ""

    if "pdf_downloaded" not in st.session_state:
        st.session_state.pdf_downloaded = False

    if "show_convert_more" not in st.session_state:
        st.session_state.show_convert_more = False

    if not st.session_state.pdf_downloaded:
        st.session_state.pdf_name = st.text_input("Enter the name for your PDF file (ex. 21900844_hw1.pdf)", value=st.session_state.pdf_name, max_chars=50)
        if st.session_state.pdf_name and ".pdf" not in st.session_state.pdf_name:
            st.session_state.pdf_name += ".pdf"

    if st.session_state.pdf_name and ".pdf" in st.session_state.pdf_name:
        output_buffer = io.BytesIO()
        if not st.session_state.pdf_downloaded:
            with st.spinner("Converting..."):
                image_to_pdf(images, output_buffer)
                output_buffer.seek(0)
                pdf_bytes = output_buffer.getvalue()
                st.success("Conversion completed!")

        if not st.session_state.pdf_downloaded:
            st.download_button("Download PDF", data=pdf_bytes, file_name=f"{st.session_state.pdf_name}", mime="application/pdf", on_click=on_download_click)
        elif st.session_state.show_convert_more:
            if st.button("Convert More"):
                st.session_state.pdf_downloaded = False
                st.session_state.pdf_name = ""
                st.session_state.show_convert_more = False

    else:
        if st.session_state.pdf_name != "":
            st.warning("Please enter a valid file name.")

st.caption("Made by **_Dmitriy Yugay_** | **_21900844_** | Handong Global University")
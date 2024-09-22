import os
from PIL import Image
from rembg import remove
import streamlit as st 

def save_uploaded_files(uploaded_file):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):  # Corregido os.path.exist -> os.path.exists
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def run_background_remover(input_img_file):
    input_img_path = save_uploaded_files(input_img_file)
    output_img_path = input_img_path.replace(".", "_rmbg.").replace("jpg", "png").replace("jpeg", "png")
    try:
        image = Image.open(input_img_path)  
        output = remove(image)
        output.save(output_img_path, "PNG")
        col1, col2 = st.columns(2) #subdivido en 2 columnas para hacer comparativa de antes y despues
        with col1:
            st.header("Antes") 
            st.image(input_img_path, caption="Imagen original")
            with open(input_img_path, "rb") as img_file:
                st.download_button(
                    label="Descargar imagen original",
                    data=img_file,
                    file_name=os.path.basename(input_img_path),
                    mime="image/jpeg"
                )
        with col2:
            st.header("Después")
            st.image(output_img_path, caption="Imagen con fondo removido")  # Muestra la imagen procesada
            with open(output_img_path, "rb") as img_file:  # Abrir archivo procesado para la descarga
                st.download_button(
                    label="Descargar imagen procesada",
                    data=img_file,
                    file_name=os.path.basename(output_img_path),
                    mime="image/png"
                ) 
        st.success("Fondo removido con éxito")
    except Exception as e:
        st.error(f"Error al remover el fondo: {e}") 
        
def main():
    st.title("Remover fondos")
    uploaded_file = st.file_uploader("Elige un archivo de imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        run_background_remover(uploaded_file)

if __name__ == "__main__":
    main()

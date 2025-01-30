import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

st.title("PDF to Table Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Save uploaded file to a temporary path
        temp_pdf_path = "temp_uploaded_file.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Read the first table from the PDF
        dfs = tabula.read_pdf(temp_pdf_path, pages='all', multiple_tables=True, stream=True)

        if dfs and len(dfs) > 0:
            df = dfs[0]  # ✅ Take only the first table
            st.success("Table extracted successfully!")

            st.subheader("Extracted Table")
            st.dataframe(df)

            # Convert DataFrame to Excel for download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            st.download_button(
                label="Export to Excel",
                data=output.getvalue(),
                file_name="extracted_table.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No tables found in the PDF document.")

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")

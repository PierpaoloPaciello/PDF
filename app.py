import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

st.title("PDF to Table")

uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        dfs = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True)
        
        if len(dfs) > 0:
            st.success("Table extracted successfully!")
            
            df = dfs[0]
            
            st.subheader("Extracted Table")
            st.dataframe(df)
            
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
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Women's Safety Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Title and branding
st.markdown("<h1 style='color:#1f3c88; font-weight:bold;'>🛡️ Women's Safety Insights Dashboard</h1>", unsafe_allow_html=True)

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Crime Data CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Show success message
        st.success("✅ Crime data loaded successfully.")

        # Display raw data
        st.subheader("🔍 Raw Data Preview")
        st.dataframe(df)

        # Show available columns
        st.info(f"Available columns: {list(df.columns)}")

        # ---------- DATA VALIDATION ----------
        expected_columns = {'Date', 'State', 'District', 'CrimeType', 'VictimAge', 'lat', 'lon'}
        missing_cols = expected_columns - set(df.columns)
        if missing_cols:
            st.error(f"❌ Missing important columns: {missing_cols}. Please upload a correct CSV file.")
        else:
         
            try:
                # Convert 'lat' and 'lon' columns to a numeric format
                df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
                df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

                # Drop any rows where the lat/lon conversion failed
                df.dropna(subset=['lat', 'lon'], inplace=True)
                
                if not df.empty:
                    st.subheader("📍 Crime Locations on Map")
                    st.map(df[['lat', 'lon']])
                else:
                    st.warning("No valid location data to display on the map after cleanup.")
            
            except Exception as e:
                st.warning(f"Couldn't display map due to unexpected error: {e}")

            # ---------- ANALYTICS VISUALS ----------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Crimes per State")
                fig_state = px.histogram(df, x="State", color="State", title="Number of Crimes per State")
                st.plotly_chart(fig_state, use_container_width=True)

            with col2:
                st.subheader("📈 Victim Age Distribution")
                fig_age = px.histogram(df, x="VictimAge", nbins=10, title="Age Distribution of Victims")
                st.plotly_chart(fig_age, use_container_width=True)

            st.subheader("🧭 Crimes by Type")
            crime_type_count = df['CrimeType'].value_counts().reset_index()
            crime_type_count.columns = ['CrimeType', 'Count']
            fig_type = px.pie(crime_type_count, names='CrimeType', values='Count', title="Crime Types Distribution")
            st.plotly_chart(fig_type, use_container_width=True)

    except pd.errors.EmptyDataError:
        st.error("❌ Failed to load CSV: File is empty or badly formatted.")
    except pd.errors.ParserError:
        st.error("❌ Failed to parse CSV: Please check if the file is in correct CSV format.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
else:
    st.warning("⚠️ Please upload a CSV file to proceed.")
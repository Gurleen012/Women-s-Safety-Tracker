import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# Page config
st.set_page_config(
    page_title="CrimeLens: Women's Safety Tracker",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.markdown("<h1 style='color:#1f3c88; font-weight:bold;'>🛡️ Women's Safety Insights Dashboard</h1>", unsafe_allow_html=True)

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Crime Data CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Crime data loaded successfully.")

        st.subheader("🔍 Raw Data Preview")
        st.dataframe(df)

        expected_columns = {'Date', 'State', 'District', 'CrimeType', 'VictimAge', 'lat', 'lon'}
        missing_cols = expected_columns - set(df.columns)
        if missing_cols:
            st.error(f"❌ Missing important columns: {missing_cols}. Please upload a correct CSV file.")
        else:
            # Clean numeric columns
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            df.dropna(subset=['lat', 'lon'], inplace=True)

            if not df.empty:
                st.subheader("📍 Crime Locations on Map")
                st.map(df[['lat', 'lon']])

            # Analytics
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

           
            st.header("🤖 Crime Prediction Models")

            # Prepare data
            df_ml = df.copy()
            le = LabelEncoder()
            for col in ['State', 'District', 'CrimeType']:
                df_ml[col] = le.fit_transform(df_ml[col])

            X = df_ml[['State', 'District', 'VictimAge', 'lat', 'lon']]
            y = df_ml['CrimeType']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            models = {
                "Logistic Regression": LogisticRegression(max_iter=500),
                "Random Forest": RandomForestClassifier(n_estimators=100),
                "KNN": KNeighborsClassifier(n_neighbors=5)
            }

            results = {}
            for name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                results[name] = acc

                st.subheader(f"{name} - Accuracy: {acc:.2f}")
                st.text(classification_report(y_test, y_pred))

            # Show best model
            best_model = max(results, key=results.get)
            st.success(f"🏆 Best Model: {best_model} with Accuracy {results[best_model]:.2f}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.warning("⚠️ Please upload a CSV file to proceed.")

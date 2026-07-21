import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Sidebar
st.sidebar.title("EDA Dashboard 📊")
upload = st.sidebar.file_uploader("Upload your CSV file", type="csv")
page = st.sidebar.radio("Select Page:", ["Welcome", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"])

# Check if file uploaded
if upload is not None:
    df = pd.read_csv(upload)
    if 'Sr No' in df.columns:
        df = df.drop('Sr No', axis=1)
    st.sidebar.success("✅ File uploaded successfully!")


if page == "Welcome":
    st.title("Welcome to EDA Dashboard 🎉")
    st.write("""
    This app allows you to perform complete EDA on any CSV dataset!
    
    ### How to use:
    - Upload your CSV file from the sidebar
    - Navigate between pages using the sidebar
    
    ### Features:
    - 📊 Univariate Analysis — histograms, boxplots, countplots
    - 📈 Bivariate Analysis — scatter plots, bar charts
    - 🔥 Multivariate Analysis — heatmap, pairplot
    """)
    
    if upload is not None:
        st.subheader("Dataset Preview")
        st.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        st.dataframe(df.head())

elif page == "Univariate Analysis":
    st.title("Univariate Analysis 📊")
    
    if upload is None:
        st.warning("⚠️ Please upload a CSV file from the sidebar first!")
    else:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        categorical_cols = df.select_dtypes(include='object').columns.tolist()
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Univariate Analysis", fontweight='bold')
        
        # Histogram
        hist_col = st.selectbox("Select column for Histogram:", numeric_cols)
        sns.histplot(df[hist_col], ax=axes[0,0])
        axes[0,0].set_title(f"Histogram of {hist_col}")
        
        # Boxplot
        box_col = st.selectbox("Select column for Boxplot:", numeric_cols)
        sns.boxplot(x=df[box_col], ax=axes[0,1])
        axes[0,1].set_title(f"Boxplot of {box_col}")
        
        # Countplot
        if categorical_cols:
            count_col = st.selectbox("Select column for Countplot:", categorical_cols)
            sns.countplot(data=df, x=count_col, ax=axes[1,0])
            axes[1,0].set_title(f"Countplot of {count_col}")
            axes[1,0].tick_params(axis='x', rotation=90)
        
        # Pie chart
        if categorical_cols:
            pie_col = st.selectbox("Select column for Pie Chart:", categorical_cols)
            top5 = df[pie_col].value_counts().head(5)
            axes[1,1].pie(top5, labels=top5.index, autopct='%1.1f%%')
            axes[1,1].set_title(f"Pie Chart of {pie_col}")
        
        plt.tight_layout()
        st.pyplot(fig)

elif page == "Bivariate Analysis":
    st.title("Bivariate Analysis 📈")
    
    if upload is None:
        st.warning("⚠️ Please upload a CSV file from the sidebar first!")
    else:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        categorical_cols = df.select_dtypes(include='object').columns.tolist()
        
        # Scatter plot
        x_col = st.selectbox("Select X axis column:", numeric_cols)
        y_col = st.selectbox("Select Y axis column:", numeric_cols)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        ax.set_title(f"{x_col} vs {y_col}")
        st.pyplot(fig)
        
        # Boxplot by group
        if categorical_cols:
            cat_col = st.selectbox("Select categorical column:", categorical_cols)
            num_col = st.selectbox("Select numeric column:", numeric_cols)
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x=cat_col, y=num_col, ax=ax2)
            ax2.set_title(f"{cat_col} vs {num_col}")
            ax2.tick_params(axis='x', rotation=90)
            st.pyplot(fig2)
elif page == "Multivariate Analysis":
    st.title("Multivariate Analysis 🔥")
    
    if upload is None:
        st.warning("⚠️ Please upload a CSV file from the sidebar first!")
    else:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        
        # Heatmap
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
        
        # Pairplot
        st.subheader("Pairplot")
        pairplot_cols = st.multiselect("Select columns for Pairplot:", numeric_cols, default=numeric_cols[:3])
        if pairplot_cols:
            fig2 = sns.pairplot(df[pairplot_cols])
            st.pyplot(fig2)

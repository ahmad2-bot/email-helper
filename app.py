import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Email Name/Company Extractor", layout="centered")

st.title("📧 Email → Name/Company Extractor")
st.markdown("Upload a `.txt` file with one email per line. The app will extract a name or company from each and provide a downloadable CSV (removes case-insensitive duplicates).")

uploaded_file = st.file_uploader("📂 Upload .txt File", type="txt")

# List of known personal domains
personal_domains = ['gmail', 'yahoo', 'hotmail', 'outlook', 'icloud', 'protonmail', 'aol']

def smart_extract(email):
    try:
        local, domain = email.lower().split('@')
        domain_main = domain.split('.')[0]

        # Clean local part
        cleaned_local = re.sub(r'\d+', '', local)
        cleaned_local = cleaned_local.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        cleaned_local = re.sub(r'\s+', ' ', cleaned_local).strip()

        # If personal email domain, try to extract name
        if any(p in domain for p in personal_domains):
            name_parts = cleaned_local.split()
            return ' '.join([p.capitalize() for p in name_parts]) if name_parts else local
        else:
            return domain_main
    except:
        return "Invalid Email"

if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    raw_emails = [line.strip() for line in content.splitlines() if line.strip()]

    # Remove exact duplicates (case-insensitive)
    seen = set()
    emails = []
    for email in raw_emails:
        email_lower = email.lower()
        if email_lower not in seen:
            seen.add(email_lower)
            emails.append(email)

    if emails:
        results = []
        for email in emails:
            name_or_company = smart_extract(email)
            results.append({'Email': email, 'Name/Company': name_or_company})

        df = pd.DataFrame(results)

        st.success(f"✅ Extracted {len(df)} unique records.")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, file_name="extracted_names.csv", mime='text/csv')
    else:
        st.warning("⚠️ No valid emails found after removing duplicates.")

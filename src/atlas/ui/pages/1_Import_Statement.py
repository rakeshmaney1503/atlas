from pathlib import Path

import streamlit as st
from sqlmodel import Session

from atlas.database.session import engine
from atlas.importers.icici_importer import ICICIImporter
from atlas.services.account_service import AccountService
from atlas.services.import_service import ImportService

st.title("📥 Import ICICI Statement")

with Session(engine) as session:
    accounts = AccountService.get_all(session)

if not accounts:
    st.error("No accounts configured.")
    st.stop()

selected_account = st.selectbox(
    "Account",
    accounts,
    format_func=lambda a: f"{a.name} ({a.institution})",
)

uploaded_file = st.file_uploader(
    "Select ICICI Statement",
    type=["xls"],
)

if uploaded_file:

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    preview_df = ICICIImporter.read(file_path)

    st.success(f"Found {len(preview_df)} transactions")

    st.dataframe(
        preview_df[
            [
                "Transaction Date",
                "Transaction Remarks",
                "Withdrawal Amount(INR)",
                "Deposit Amount(INR)",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

    if st.button("Import Statement"):

        with Session(engine) as session:

            account = AccountService.get_by_name(
                session,
                selected_account.name,
            )

            imported, duplicates = (
                ImportService.import_icici_statement(
                    session=session,
                    statement_path=file_path,
                    account=account,
                )
            )

        c1, c2 = st.columns(2)

        c1.metric("Imported", imported)
        c2.metric("Duplicates", duplicates)

        if imported:
            st.success("Statement imported successfully.")
        else:
            st.info("Everything in this statement has already been imported.")

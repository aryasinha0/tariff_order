import streamlit as st
import pandas as pd
master_sheet=pd.read_excel("Output_2121 (7).xlsx.xlsx")
Con_ID=st.number_input("Enter the Consumer_ID", min_value=0, step=1)
st.write(master_sheet)
flag=False
for index, row in master_sheet.iterrows():
    if row["CON_ID"] == Con_ID:
        # st.write("HI, I am here")
        
        (SUB_DIV, SECTION, CONC_LOAD,CONTRACT_DEMAND,SANC_LOAD,TARIFF_ID,BILLED_MONTH,PRE_READ,HRS_OF_SUPPLY) = (row["SUB_DIV_ID"], row["SECTION_ID"], row["CONC_LOAD"],row["CONTRACT_DEMAND"],row["SANC_LOAD"],row["TARIFF_ID"],row["BILLED_MONTH"],row["PRE_READ"],row["HRS_OF_SUPPLY"])
        st.markdown(f'''
            SUB_DIV: {SUB_DIV}<br>
            SECTION: {SECTION}<br>
            CONC_LOAD: {CONC_LOAD}<br>
            CONTRACT_DEMAND: {CONTRACT_DEMAND}<br>
            SANC_LOAD: {SANC_LOAD}<br>
            TARIFF_ID: {TARIFF_ID}<br>
            BILLED_MONTH: {BILLED_MONTH}<br>
            PRE_READ: {PRE_READ}<br>
            HRS_OF_SUPPLY: {HRS_OF_SUPPLY}
            ''', unsafe_allow_html=True)

        CUR_READ=st.number_input("Enter the current Reading",min_value=0, step=1)
        PF_VALUE=st.number_input("Enter the PF_VALUE")
        RECORD_DEM=st.number_input("Enter the recorded demand")
        if st.button("Submit details"):
            from main import tariffOrder
            c1=tariffOrder(CONC_LOAD,CONTRACT_DEMAND,SANC_LOAD,TARIFF_ID,BILLED_MONTH,CUR_READ,PRE_READ,RECORD_DEM,PF_VALUE,HRS_OF_SUPPLY)
            st.write("energy charge is ",str(c1.ec_charge()))
            st.write("units_cons is ",str(c1.unitsCons()))
            st.write("fixed charge is ",str(c1.fixed_chrg_cal()[0]))
            st.write("Maximum demand charge is ",str(c1.fixed_chrg_cal()[1]))
            st.write("shunt charge is ",str(c1.pf_charge()))

        
        flag=True
        break
    
if not flag:
    st.write("Consumer_ID not found")   


import streamlit as st

import math
class tariffOrder:

    def __init__(self,CONC_LOAD,CONTRACT_DEMAND,SANC_LOAD,TARIFF_ID,BILLED_MONTH,CUR_READ,PRE_READ,RECORD_DEM,PF_VALUE,HRS_OF_SUPPLY):
        self.CONC_LOAD=CONC_LOAD
        self.CONTRACT_DEMAND=CONTRACT_DEMAND
        self.SANC_LOAD=SANC_LOAD
        self.TARIFF_ID=TARIFF_ID
        self.BILLED_MONTH=BILLED_MONTH
        self.CUR_READ=CUR_READ
        self.PRE_READ=PRE_READ
        self.RECORD_DEM=RECORD_DEM
        self.PF_VALUE=PF_VALUE
        self.HRS=HRS_OF_SUPPLY
        
    def unitsCons (self):
        return (self.CUR_READ - self.PRE_READ)

    def fixed_chrg_cal(self):     #sanc_load,con_demand,rec_demand,tariff_rate,billing_days,hours
        fixed_charge=0
        exc_charge=0
        hrs=1
        fixed_rate_dict={'DS1D':40, 'DS2D': 80, 'DS3D': 80, 'NDS1D':60, 'LTIS1D' : 288, 'LTIS2D' : 360, 'KJ' : 20, 'IAS1' : 100, 'IAS2D' : 500, 'PWWD' : 630, 'HGN': 100, 'SS2':100, 'SS1D': 100, 'LTEV':0}

        if self.TARIFF_ID=='NDS2D':
            if self.CONTRACT_DEMAND<=0.5:
                tariff_rate=200
            else:
                tariff_rate=300
        else:
                tariff_rate=fixed_rate_dict[self.TARIFF_ID]
        if self.TARIFF_ID=='KJ':
            self.SANC_LOAD=self.SANC_LOAD/1000
            self.CONTRACT_DEMAND=self.CONTRACT_DEMAND/1000
            self.RECORD_DEM=self.RECORD_DEM/1000
        
        if 0<self.HRS<21:
            hrs=self.HRS/21
        if self.CONTRACT_DEMAND==self.SANC_LOAD or self.CONTRACT_DEMAND>self.SANC_LOAD:
            if self.RECORD_DEM>self.CONTRACT_DEMAND:
                fixed_charge= (((math.ceil(self.RECORD_DEM)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
                if self.RECORD_DEM>(105/100)*self.CONTRACT_DEMAND:
                    exc_charge=(((math.ceil(self.RECORD_DEM-self.CONTRACT_DEMAND)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
            else:
                if (75/100)*self.CONTRACT_DEMAND>self.RECORD_DEM:
                    fixed_charge= (((math.ceil((75/100)*self.CONTRACT_DEMAND)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
                else:
                    fixed_charge=(((math.ceil(self.RECORD_DEM)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
        else:
            if self.RECORD_DEM>self.SANC_LOAD:
                fixed_charge= (((math.ceil(self.RECORD_DEM)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
                if self.RECORD_DEM>(105/100)*self.SANC_LOAD:
                    exc_charge=(((math.ceil(self.RECORD_DEM-self.SANC_LOAD)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
            else:
                if (75/100)*self.SANC_LOAD>self.RECORD_DEM:
                    fixed_charge= (((math.ceil((75/100)*self.SANC_LOAD)*tariff_rate)/30)*self.BILLED_MONTH)*hrs
                else:
                    fixed_charge=(((math.ceil(self.RECORD_DEM)*tariff_rate)/30)*self.BILLED_MONTH)*hrs

        fixed_charge = round(fixed_charge, 2) if fixed_charge != int(fixed_charge) else int(fixed_charge)
        exc_charge = round(exc_charge, 2) if exc_charge != int(exc_charge) else int(exc_charge)

        return fixed_charge, exc_charge
    
    def ec_charge(self):
        if self.CONTRACT_DEMAND<=0.5:
            energy_charge={'DS1D': [7.57,8.11,50], "DS2D":[7.57,9.10,100], "DS3D":[9.18,9.18,100],'NDS1D':[7.94,8.36,100], "LTIS1D":[7.94,7.94,100],"LTIS2D":[7.94,7.94,100],"KJ":[7.57,8.11,50],"IAS1":[6.89,6.89,100],"IAS2D":[7.32,9.32,100],
                "PWWD" : [9.87,9.87,100], "HGN":[8.31,8.31,100], "SS2":[9.18,9.18,100], "SS1D":[9.18,9.18,100], "LTEV":[8.87,8.87,100], "NDS2D":[7.88,7.88,100]}
        else:
            energy_charge={'DS1D': [7.57,8.11,50], "DS2D":[7.57,9.10,100], "DS3D":[9.18,9.18,100],'NDS1D':[7.94,8.36,100], "LTIS1D":[7.94,7.94,100],"LTIS2D":[7.94,7.94,100],"KJ":[7.57,8.11,50],"IAS1":[6.89,6.89,100],"IAS2D":[7.32,9.32,100],
                "PWWD" : [9.87,9.87,100], "HGN":[8.31,8.31,100], "SS2":[9.18,9.18,100], "SS1D":[9.18,9.18,100], "LTEV":[8.87,8.87,100], "NDS2D":[7.88,9.08,100]}
        slab=energy_charge[self.TARIFF_ID][2]
        charge1=energy_charge[self.TARIFF_ID][0]
        charge2=energy_charge[self.TARIFF_ID][1]
        units_cons=self.unitsCons()
        if units_cons<=slab:
            return (units_cons*charge1)
        return ((units_cons-slab)*charge2 + slab*charge1)
    def pf_charge(self):
        req_tariff=['IAS1','IAS2D','NDS1D','NDS2D','LTIS2D']
        DEMAND_CHRG=self.fixed_chrg_cal()[0]
        EC_CHRG=self.ec_charge()
        chrg=0
        if self.TARIFF_ID in req_tariff:
            
            if 0.8<=self.PF_VALUE< 0.9:
                i=(0.9-self.PF_VALUE)/0.01
                chrg=round((i*((1/100)*DEMAND_CHRG + (1/100)*EC_CHRG)),2)

            elif self.PF_VALUE<0.8:
                i=(0.8-self.PF_VALUE)/0.01
                chrg=round((i*((1.5/100)*DEMAND_CHRG + (1.5/100)*EC_CHRG)) + (10*((1/100)*DEMAND_CHRG + (1/100)*EC_CHRG)),2)
            
            elif 0.90<self.PF_VALUE<=0.95:
                i=(self.PF_VALUE-0.90)/0.01
                chrg=-(round((i*((0.5/100)*DEMAND_CHRG + (0.5/100)*EC_CHRG)),2))

            elif 0.95<self.PF_VALUE<1:
                i=(self.PF_VALUE-0.95)/0.01
                chrg=-(round((i*((1/100)*DEMAND_CHRG + (1/100)*EC_CHRG)+(5*((0.5/100)*DEMAND_CHRG + (0.5/100)*EC_CHRG))),2))
        return chrg
# arg1 = st.number_input("Enter first argument")
# arg2 = st.number_input("Enter second argument")
# arg3 = st.number_input("Enter third argument")
# arg4 = st.text_input("Enter fourth argument")
# arg5 = st.number_input("Enter fifth argument")
# arg6 = st.number_input("Enter sixth argument")
# arg7 = st.number_input("Enter seventh argument")
# arg8 = st.number_input("Enter eighth argument")
# arg9 = st.number_input("Enter ninth argument")
# arg10 = st.number_input("Enter tenth argument")

# if st.button("Submit"):
#     # Initialize the tariffOrder object with user inputs
#     c1 = tariffOrder(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)
#     # c1=tariffOrder(1,1,1,"NDS2D",29,1727,1708,0.48,0.82,22.24)
#     st.write("energy charge is ",str(c1.ec_charge()))
#     st.write("units_cons is ",str(c1.unitsCons()))
#     st.write("fixed charge is ",str(c1.fixed_chrg_cal()))
#     st.write("shunt charge is ",str(c1.pf_charge()))

# 1,1,1,"DS1D",29,49,37,0.02,0.95,22.82
# energy charge is 90.84

# units_cons is 12

# fixed charge is (38.67, 0)

# shunt charge is 0
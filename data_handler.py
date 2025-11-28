import pandas as pd
import requests
import numpy as np
import random
from datetime import datetime, timedelta

def fetch_oncology_data(condition="Cancer"):
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": condition,
        "filter.overallStatus": "RECRUITING|ACTIVE_NOT_RECRUITING|COMPLETED",
        "fields": "NCTId,BriefTitle,OverallStatus,Phases,Conditions,Interventions,Locations,StudyFirstSubmitDate",
        "pageSize": 50
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 

        data = response.json()
        studies = data.get('studies', [])
        
        clean_data = []
        for study in studies:
            try:
                protocol = study.get('protocolSection', {})
                ident = protocol.get('identificationModule', {})
                status = protocol.get('statusModule', {})
                design = protocol.get('designModule', {})
                
                # --- EXTRAÇÃO DE CAMPOS ANINHADOS DE FORMA SEGURA ---
                locs = protocol.get('contactsLocationsModule', {})
                inters = protocol.get('armsInterventionsModule', {})
                
                # 1. LOCALIZAÇÃO (Para o Mapa Coroplético)
                locations_list = locs.get('locations', [])
                country_name = "Global"
                
                if locations_list:
                    country_name = locations_list[0].get('country', 'Global')
                
                # 2. TIPO DE INTERVENÇÃO (Tratamento)
                inter_type = "Drug"
                if inters.get('interventions') and len(inters['interventions']) > 0:
                    inter_type = inters['interventions'][0].get('type', 'Drug')

                # 3. FASE (Normalização para o Funil/Barras)
                phases = design.get('phases', ['Not Applicable'])
                phase_str = phases[0] if phases else "PHASE1"
                
                phase_clean = "Fase 1 (Segurança)"
                if "PHASE2" in phase_str: phase_clean = "Fase 2 (Eficácia)"
                elif "PHASE3" in phase_str: phase_clean = "Fase 3 (Confirmação)"
                elif "PHASE4" in phase_str or status.get('overallStatus') == 'COMPLETED': phase_clean = "Aprovado/Fase 4"

                # Adiciona ao conjunto de dados limpos
                clean_data.append({
                    "NCTId": ident.get('nctId'),
                    "Title": ident.get('briefTitle'),
                    "Status": status.get('overallStatus'),
                    "Phase": phase_clean,
                    "Condition": condition,
                    "InterventionType": inter_type,
                    "Location": country_name,
                    "Date": status.get('studyFirstSubmitDate', '2023-01-01')
                })
            
            except Exception as e:
                # Se um estudo específico estiver malformado, apenas o pula
                print(f"Skipping malformed study: {e}")
                continue 
        
        # --- CORREÇÃO: RETORNA O DATAFRAME APÓS O LOOP ---
        if clean_data:
            return pd.DataFrame(clean_data)
        else:
            raise Exception("No valid studies found in API response.") 

    except Exception as e: 
        print(f"Erro na API (Usando Mock Data): {e}")

    # --- MOCK DATA (PLANO B DE SEGURANÇA) ---
    print("Retornando dados simulados (Fallback Mode)...")
    qtde = 50
    data_mock = []
    for i in range(qtde):
        phase = random.choice(["Fase 1 (Segurança)", "Fase 2 (Eficácia)", "Fase 3 (Confirmação)"])
        i_type = random.choice(["Drug", "Radiation", "Procedure"])
        data_mock.append({
            "NCTId": f"MOCK{i + 1}",
            "Title": f"Simulated study for {condition} ({i_type})",
            "Status": random.choice(["Recruiting", "Completed", "Active"]),
            "Phase": phase,
            "Condition": condition,
            "InterventionType": i_type,
            "Location": random.choice(["United States", "China", "Brazil", "Germany", "France"]),
            "Date": "2024-01-01"
        })
    return pd.DataFrame(data_mock)
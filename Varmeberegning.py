import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def show():
    st.title("Varmeberegning for madvare")
   
    # -------------------------
    # Produktdata
   
    # -------------------------
    df = pd.read_excel("varmemaengder_komplet.xlsx")
        
    df.columns = df.columns.str.strip()  # Fjern eventuelle førende/efterfølgende mellemrum

    kolonner_tal = [
        "Maks. frysepunkt (°C)",
        "Varmekapacitet før frysning [kJ/(kg·K)]",
        "Varmekapacitet efter frysning [kJ/(kg·K)]",
        "Frysevarme Δh_ls [kJ/kg]",
    ]

    for col in kolonner_tal:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .replace("nan", "")
        )
        df[col] = pd.to_number(df[col], errors="coerce")

    df = df[df["produkt"].notna()]
    df = [df[df["produkt"].astype(str).str.strip() != ""]]

    produkter = {}
    for _, row in df.iterrows():
        navn = str(row["produkt"]).strip()
        produkter[navn] = {
            "Tc": 0.0 if pd.isna(row["Maks. frysepunkt (°C)"]) 
            else float(row["Maks. frysepunkt (°C)"]),
            "c_foer": 0.0 if pd.isna(row["Varmekapacitet før frysning [kJ/(kg·K)]"]) 
            else float(row["Varmekapacitet før frysning [kJ/(kg·K)]"]),
            "L": 0.0 if pd.isna(row["Frysevarme Δh_ls [kJ/kg]"]) 
            else float(row["Frysevarme Δh_ls [kJ/kg]"]),
            "c_efter": 0.0 if pd.isna(row["Varmekapacitet efter frysning [kJ/(kg·K)]"]) 
            else float(row["Varmekapacitet efter frysning [kJ/(kg·K)]"]),
        }

    produktnavne = list(produkter.keys())

    # -------------------------
    # Hjælpefunktion til at opdatere data pr. produkt
    # -------------------------
    def opdater_produktdata(i: int) -> None:
        valgt = st.session_state[f"produkt_{i}"]
        data = produkter[valgt]
        st.session_state[f"Tc_{i}"] = data["Tc"]
        st.session_state[f"c_foer_{i}"] = data["c_foer"]
        st.session_state[f"L_{i}"] = data["L"]
        st.session_state[f"c_efter_{i}"] = data["c_efter"]

    # -------------------------
    # Standard-initialisering for 3 mulige produkter
    # -------------------------
    for i in range(3):
        if f"produkt_{i}" not in st.session_state:
            standard = produktnavne[0]
            st.session_state[f"produkt_{i}"] = standard
            st.session_state[f"Tc_{i}"] = produkter[standard]["Tc"]
            st.session_state[f"c_foer_{i}"] = produkter[standard]["c_foer"]
            st.session_state[f"L_{i}"] = produkter[standard]["L"]
            st.session_state[f"c_efter_{i}"] = produkter[standard]["c_efter"]

    # -------------------------
    # Indstillinger
    # -------------------------
    top1, top2 = st.columns([1, 1])

    with top1:
        antal_produkter = st.selectbox(
            "Antal produkter",
            [1, 2, 3],
            index=0,
            key="antal_produkter"
        )

    with top2:
        manuel_redigering = st.checkbox(
            "Redigér produktdata manuelt",
            value=False,
            key="manuel_redigering"
        )

    # -------------------------
    # Fælles temperaturer
    # -------------------------
    st.subheader("Fælles temperaturer")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        T_varm = st.number_input(
            "T_varm [°C]",
            value=0.00,
            step=0.01,
            format="%.2f",
            key="T_varm"
        )

    with col_t2:
        T_fryserum = st.number_input(
            "T_fryserum [°C]",
            value=-18.00,
            step=0.01,
            format="%.2f",
            key="T_fryserum"
        )

    # -------------------------
    # Produktinput
    # -------------------------
    st.subheader("Produkter")

    produkt_resultater = []

    for i in range(antal_produkter):
        with st.expander(f"Produkt {i+1}", expanded=True):
            st.selectbox(
                f"Vælg produkt {i+1}",
                produktnavne,
                key=f"produkt_{i}",
                on_change=opdater_produktdata,
                args=(i,)
            )

            if not manuel_redigering:
                valgt = st.session_state[f"produkt_{i}"]
                data = produkter[valgt]
                st.session_state[f"Tc_{i}"] = data["Tc"]
                st.session_state[f"c_foer_{i}"] = data["c_foer"]
                st.session_state[f"L_{i}"] = data["L"]
                st.session_state[f"c_efter_{i}"] = data["c_efter"]

            c1, c2 = st.columns(2)

            with c1:
                masse = st.number_input(
                    f"Masse [kg] - produkt {i+1}",
                    min_value=0.00,
                    value=0.00,
                    step=0.01,
                    format="%.2f",
                    key=f"masse_{i}"
                )

                Tc = st.number_input(
                    f"T_frysetemperatur [°C] - produkt {i+1}",
                    step=0.01,
                    format="%.2f",
                    key=f"Tc_{i}",
                    disabled=not manuel_redigering
                )

            with c2:
                c_foer = st.number_input(
                    f"c før frys [kJ/kgK] - produkt {i+1}",
                    step=0.01,
                    format="%.2f",
                    key=f"c_foer_{i}",
                    disabled=not manuel_redigering
                )

                L = st.number_input(
                    f"Latent varme L [kJ/kg] - produkt {i+1}",
                    step=0.01,
                    format="%.2f",
                    key=f"L_{i}",
                    disabled=not manuel_redigering
                )

            c3, _ = st.columns(2)

            with c3:
                c_efter = st.number_input(
                    f"c efter frys [kJ/kgK] - produkt {i+1}",
                    step=0.01,
                    format="%.2f",
                    key=f"c_efter_{i}",
                    disabled=not manuel_redigering
                )

            dT1 = T_varm - Tc
            dT3 = abs(T_fryserum - Tc)

            Q1 = masse * c_foer * dT1
            Q2 = masse * L
            Q3 = masse * c_efter * dT3
            Q_total = Q1 + Q2 + Q3

            st.markdown("### Resultat for produkt")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Q1 [kJ]", f"{Q1:.2f}")
            r2.metric("Q2 [kJ]", f"{Q2:.2f}")
            r3.metric("Q3 [kJ]", f"{Q3:.2f}")
            r4.metric("Q_total [kJ]", f"{Q_total:.2f}")

            with st.expander(f"Vis delberegning for produkt {i+1}"):
                st.write(f"ΔT1 = **{dT1:.2f} K**")
                st.write(f"ΔT3 = **{dT3:.2f} K**")

            produkt_resultater.append({
                "Produkt": st.session_state[f"produkt_{i}"],
                "Masse [kg]": masse,
                "Tc [°C]": Tc,
                "c_før [kJ/kgK]": c_foer,
                "L [kJ/kg]": L,
                "c_efter [kJ/kgK]": c_efter,
                "Q1 [kJ]": Q1,
                "Q2 [kJ]": Q2,
                "Q3 [kJ]": Q3,
                "Q_total [kJ]": Q_total,
            })

    # -------------------------
    # Samlet resultat
    # -------------------------
    sum_Q1 = sum(r["Q1 [kJ]"] for r in produkt_resultater)
    sum_Q2 = sum(r["Q2 [kJ]"] for r in produkt_resultater)
    sum_Q3 = sum(r["Q3 [kJ]"] for r in produkt_resultater)
    sum_Q_total = sum(r["Q_total [kJ]"] for r in produkt_resultater)
    sum_masse = sum(r["Masse [kg]"] for r in produkt_resultater)

    st.subheader("Temperatur–Energi graf")

    fig, ax = plt.subplots()

    max_energy = 0
    min_temp = T_varm
    max_temp = T_varm

    for r in produkt_resultater:
        T = [T_varm, r["Tc [°C]"], r["Tc [°C]"], T_fryserum]
        E = [0, r["Q1 [kJ]"], r["Q1 [kJ]"] + r["Q2 [kJ]"], r["Q_total [kJ]"]]

        ax.plot(E, T, marker="o", label=r["Produkt"])

        max_energy = max(max_energy, r["Q_total [kJ]"])
        min_temp = min(min_temp, min(T))
        max_temp = max(max_temp, max(T))

    ax.set_xlabel("Energi [kJ]")
    ax.set_ylabel("Temperatur [°C]")
    ax.set_title("Temperatur vs Energi under nedfrysning")
    ax.grid(True)

    energy_margin = max(1.0, max_energy * 0.10)
    temp_margin = max(1.0, (max_temp - min_temp) * 0.10)

    ax.set_xlim(-energy_margin, max_energy + energy_margin)
    ax.set_ylim(min_temp - temp_margin, max_temp + temp_margin)

    ax.legend()

    st.pyplot(fig)

    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("Masse total [kg]", f"{sum_masse:.2f}")
    s2.metric("Q1 total [kJ]", f"{sum_Q1:.2f}")
    s3.metric("Q2 total [kJ]", f"{sum_Q2:.2f}")
    s4.metric("Q3 total [kJ]", f"{sum_Q3:.2f}")
    s5.metric("Q total [kJ]", f"{sum_Q_total:.2f}")

    # -------------------------
    # Tabel
    # -------------------------
    with st.expander("Vis samlet tabel", expanded=False):
        tabel_data = []
        for r in produkt_resultater:
            tabel_data.append({
                "Produkt": r["Produkt"],
                "Masse [kg]": f'{r["Masse [kg]"]:.2f}',
                "Tc [°C]": f'{r["Tc [°C]"]:.2f}',
                "c_før [kJ/kgK]": f'{r["c_før [kJ/kgK]"]:.2f}',
                "L [kJ/kg]": f'{r["L [kJ/kg]"]:.2f}',
                "c_efter [kJ/kgK]": f'{r["c_efter [kJ/kgK]"]:.2f}',
                "Q1 [kJ]": f'{r["Q1 [kJ]"]:.2f}',
                "Q2 [kJ]": f'{r["Q2 [kJ]"]:.2f}',
                "Q3 [kJ]": f'{r["Q3 [kJ]"]:.2f}',
                "Q_total [kJ]": f'{r["Q_total [kJ]"]:.2f}',
            })

        st.table(tabel_data)

    # -------------------------
    # Formler
    # -------------------------
    with st.expander("Vis formler", expanded=False):
        st.latex(r"Q_1 = m \cdot c_{\mathrm{før}} \cdot (T_{\mathrm{varm}} - T_c)")
        st.latex(r"Q_2 = m \cdot L")
        st.latex(r"Q_3 = m \cdot c_{\mathrm{efter}} \cdot |T_{\mathrm{fryserum}} - T_c|")
        st.latex(r"Q_{\mathrm{total}} = Q_1 + Q_2 + Q_3")
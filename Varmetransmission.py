import streamlit as st

def show():
    import streamlit as st

    st.title("Varmetransmission")
    st.latex(r"\phi_{\text{total}}=\sum U_i \cdot A_i \cdot \Delta T_i")


    def dt_block(section_key: str) -> float:
        st.markdown("### ΔT (temperaturforskel)")
        dt_mode = st.radio(
            "Vælg metode",
            ["Indtast ΔT direkte", "Indtast T_varm og T_kold"],
            horizontal=True,
            key=f"dt_mode_{section_key}",
        )

        if dt_mode == "Indtast ΔT direkte":
            dT = st.number_input(
                "ΔT [K]",
                min_value=0.000,
                value=0.000,
                step=0.500,
                key=f"dT_{section_key}",
            )
        else:
            Th = st.number_input("T_varm [°C]", value=0.000, step=0.500, key=f"Th_{section_key}")
            Tc = st.number_input("T_kold [°C]", value=0.000, step=0.500, key=f"Tc_{section_key}")
            dT = Th - Tc

        st.write(f"ΔT = **{dT:.4f} K**")
        return dT


    def u_block(section_key: str) -> float:
        st.markdown("### U-værdi")
        u_mode = st.radio(
            "Vælg metode",
            ["U er oplyst", "Beregn U fra lag (materialer)"],
            horizontal=True,
            key=f"u_mode_{section_key}",
        )

        if u_mode == "U er oplyst":
            U = st.number_input(
                "U [W/m²K]",
                min_value=0.000,
                value=0.000,
                step=0.001,
                key=f"U_{section_key}",
            )
            return U

        # Lag-beregning (vandret visning)
        st.caption("Lag i serie: R_total = Σ(s/λ) og U = 1/R_total.")
        n_layers = st.number_input(
            "Antal lag",
            min_value=1,
            value=1,
            step=1,
            key=f"n_{section_key}",
        )

        R_total = 0.000
        cols = st.columns(int(n_layers))

        for j in range(int(n_layers)):
            with cols[j]:
                st.markdown(f"**Lag {j+1}**")

                s = st.number_input(
                    "s [m]",
                    min_value=0.000,
                    value=0.000,
                    step=0.001,
                    format="%.4f",
                    key=f"s_{section_key}_{j}",
                )
                lam = st.number_input(
                    "λ [W/m·K]",
                    min_value=0.000,
                    value=0.000,
                    step=0.001,
                    format="%.4f",
                    key=f"lam_{section_key}_{j}",
                )

                R_j = (s / lam) if (s > 0.000 and lam > 0.000) else 0.0
                st.write(f"R = {R_j:.6f}")
                R_total += R_j

        U = (1.000 / R_total) if (R_total > 0.000) else 0.0
        st.write(f"R_total = **{R_total:.6f} m²K/W**")
        st.write(f"U = **{U:.6f} W/m²K**")
        return U


    def result_row(name: str, dT: float, U: float, A: float) -> dict:
        phi = U * A * dT
        return {"Del": name, "ΔT [K]": dT, "U [W/m²K]": U, "A [m²]": A, "φ [W]": phi}


    rows = []
    phi_total = 0.000
    A_total = 0.000

    # -------------------------
    # GULV
    # -------------------------
    with st.expander("Gulv (A = l · b)", expanded=True):
        dT = dt_block("gulv")
        U = u_block("gulv")

        st.markdown("### Geometri")
        l = st.number_input("l [m]", min_value=0.0, value=0.0, step=0.1, key="l_gulv")
        b = st.number_input("b [m]", min_value=0.0, value=0.0, step=0.1, key="b_gulv")
        A = l * b
        st.write(f"A = **{A:.4f} m²**")

        r = result_row("Gulv", dT, U, A)
        st.write(f"φ = **{r['φ [W]']:.4f} W**")

        rows.append(r)
        A_total += A
        phi_total += r["φ [W]"]

    # -------------------------
    # LOFT
    # -------------------------
    with st.expander("Loft (A = l · b)", expanded=True):
        dT = dt_block("loft")
        U = u_block("loft")

        st.markdown("### Geometri")
        l = st.number_input("l [m]", min_value=0.0, value=0.0, step=0.1, key="l_loft")
        b = st.number_input("b [m]", min_value=0.0, value=0.0, step=0.1, key="b_loft")
        A = l * b
        st.write(f"A = **{A:.4f} m²**")

        r = result_row("Loft", dT, U, A)
        st.write(f"φ = **{r['φ [W]']:.4f} W**")

        rows.append(r)
        A_total += A
        phi_total += r["φ [W]"]

    # -------------------------
    # VÆGGE (1–4 vægge)
    # -------------------------
    with st.expander("Vægge (valg 1–4 vægge)", expanded=True):
        dT = dt_block("vaeg")
        U = u_block("vaeg")

        st.markdown("### Geometri")
        st.caption("Vælg hvor mange lange (l·h) og korte (b·h) vægge du har med. I alt 1–4 vægge.")

        l = st.number_input("l [m]", min_value=0.0, value=0.0, step=0.1, key="l_vaeg")
        b = st.number_input("b [m]", min_value=0.0, value=0.0, step=0.1, key="b_vaeg")
        h = st.number_input("h [m]", min_value=0.0, value=0.0, step=0.1, key="h_vaeg")

        n_long = st.number_input("Antal lange vægge (l·h) [0–2]", min_value=0, max_value=2, value=0, step=1, key="n_long")
        n_short = st.number_input("Antal korte vægge (b·h) [0–2]", min_value=0, max_value=2, value=0, step=1, key="n_short")

        n_total = int(n_long) + int(n_short)
        if n_total == 0:
            st.warning("Vælg mindst 1 væg (n_long + n_short).")
        elif n_total > 4:
            st.warning("Der kan maks være 4 vægge i alt.")

        A = (int(n_long) * l * h) + (int(n_short) * b * h)
        st.write(f"A = **{A:.4f} m²** (for {n_total} vægge)")

        r = result_row("Vægge", dT, U, A)
        st.write(f"φ = **{r['φ [W]']:.4f} W**")

        rows.append(r)
        A_total += A
        phi_total += r["φ [W]"]

    # -------------------------
    # SAMLET
    # -------------------------
    st.subheader("Samlet resultat")
    c1, c2, c3 = st.columns(3)
    c1.metric("A_total [m²]", f"{A_total:.4f}")
    c2.metric("φ_total [W]", f"{phi_total:.4f}")
    c3.metric("φ_total [kW]", f"{phi_total/1000:.4f}")

    with st.expander("Vis tabel"):
        st.dataframe(rows, use_container_width=True)

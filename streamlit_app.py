"""
# To test locally
streamlit run streamlit_app.py
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import tempfile
import octadist as oc
import py3Dmol

st.set_page_config(page_title="OctaDist Web", layout="wide")

# Sidebar
st.sidebar.image(
    "https://octadist.github.io/images/molecule.png", use_container_width=True
)
st.sidebar.title("OctaDist")
st.sidebar.write(
    "A tool for calculating octahedral distortion parameters from molecular structures ([more info](https://octadist.github.io/))."
)
st.sidebar.markdown(
    f"**Developer:** {getattr(oc, '__maintainer__', 'OctaDist Development Team')}"
)
st.sidebar.markdown(f"**Version:** {getattr(oc, '__version__', 'unknown')}")
st.sidebar.markdown(
    "For requesting feature or reporting issue, please visit "
    "[here](https://github.com/OctaDist/OctaDist/issues)"
)

st.title("OctaDist: Octahedral Distortion Calculator")
# st.write("Upload an XYZ file to calculate distortion parameters.")

################
# File Uploader
################
uploaded_file = st.file_uploader("Choose an XYZ file", type=["xyz"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xyz") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        ######################
        # Extract Coordinates
        ######################
        atom_full, coord_full = oc.io.extract_coord(tmp_path)

        #################################
        # Determine octahedron structure
        #################################
        # If there are multiple metals, this identifies the octahedral part
        atom, coord = oc.io.extract_octa(atom_full, coord_full)

        #######################
        # Calculate parameters
        #######################
        dist = oc.CalcDistortion(coord)

        # Display Results
        st.subheader("Distortion Parameters")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Zeta (ζ)", f"{dist.zeta:.4f}")
        col2.metric("Delta (δ)", f"{dist.delta:.6f}")
        col3.metric("Sigma (Σ)", f"{dist.sigma:.4f}")
        col4.metric("Theta (Θ)", f"{dist.theta:.4f}")

        ################
        # Visualization
        ################
        st.subheader("3D Molecular Visualization")
        # Build XYZ string for py3Dmol model rendering
        xyz_lines = [str(len(atom_full)), "Uploaded molecule"]
        for atom_symbol, xyz in zip(atom_full, coord_full):
            xyz_lines.append(f"{atom_symbol} {xyz[0]:.6f} {xyz[1]:.6f} {xyz[2]:.6f}")
        xyz_block = "\n".join(xyz_lines)

        viewer = py3Dmol.view(width=900, height=300)
        viewer.addModel(xyz_block, "xyz")
        viewer.setStyle({"stick": {"radius": 0.15}, "sphere": {"scale": 0.25}})
        viewer.zoomTo()

        components.html(viewer._make_html(), height=300, width=920)
        st.info(
            "If you use OctaDist in your work, please cite this paper:\n\n"
            f"Rangsiman Ketkaew et al.\n"
            "OctaDist: A Tool for Calculating Distortion Parameters in Spin Crossover "
            "and Coordination Complexes.\n\n"
            f"Dalton Trans., 2021, 50, 1086-1096\n"
            f"{getattr(oc, '__doi__', 'https://doi.org/10.1039/D0DT03988H')}"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")

    finally:
        # Cleanup temporary file
        os.remove(tmp_path)
else:
    st.info("Please upload an XYZ file.")

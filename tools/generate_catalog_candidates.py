import json
from pathlib import Path

GROUPS = {
    'industrial-protocols': '''opc_ua modbus_tcp modbus_rtu mqtt sparkplug_b bacnet ethernet_ip siemens_s7 profinet profibus ethercat dnp3 can_bus socketcan canopen devicenet cc_link powerlink sercos knx iec_60870_5_104 iec_61850 hart io_link mtconnect opc_ua_pubsub''',
    'plc-scada': '''siemens_tia_portal wincc beckhoff_twincat codesys rockwell_studio_5000 factorytalk schneider_ecostruxure mitsubishi_gxworks omron_sysmac br_automation abb_automation_builder wago_ecockpit openplc beremiz ignition_scada aveva_system_platform aveva_historian wonderware ge_proficy siemens_pcs7 abb_800xa emerson_deltav honeywell_experion yokogawa_centum''',
    'mes-plm': '''siemens_opcenter sap_digital_manufacturing sap_pp sap_pm sap_mii oracle_manufacturing aveva_mes factorytalk_productioncentre ge_proficy_plant_applications plex_mes tulip sepasoft_mes ignition_mes odoo_manufacturing erpnext_manufacturing teamcenter ptc_windchill enovia_3dexperience aras_innovator fusion_manage solidworks_pdm autodesk_vault openbom''',
    'cad-cam': '''onshape solidworks siemens_nx catia ptc_creo solid_edge rhino3d grasshopper open_cascade occt salome_geometry brlcad cadquery build123d solvespace librecad kicad altium_designer autodesk_inventor freecad_path freecad_cam linuxcnc machinekit grbl fluidnc marlin klipper prusaslicer curaengine orcaslicer camotics opencamlib pycam bcnc''',
    'cae-hpc': '''ansys ansys_fluent ansys_mechanical ansys_mapdl ansys_electronics_desktop salome_meca code_saturne petsc slepc trilinos ginkgo swak4foam febio febiostudio getfem ngsolve sfepy z88 calculix_graphix simscale_api openradioss project_chrono mbdyn simbody''',
    'electromagnetics-optics': '''openems meep mpb fdtd qucs_s scikit_rf s4 raysect opticstudio zemax ansys_hfss ansys_maxwell cst_studio sonnet keysight_ads awr_microwave''',
    'control-optimization': '''python_control casadi do_mpc pyomo gekko cvxpy osqp ipopt acados sundials fmi fmpy pyfmi ompython gurobi cplex scip highs cbc glpk ortools pulp jump optuna nevergrad botorch ax pymoo deap''',
    'robotics': '''ros2 moveit2 nav2 universal_robots urscript ur_rtde abb_rapid kuka_krl kuka_sunrise fanuc yaskawa_motoplus yaskawa_inform franka kinova_kortex xarm dobot ufactory realman unitree spot_sdk clearpath fetch_robotics''',
    'digital-twin-monitoring': '''nvidia_omniverse usd openusd azure_digital_twins aws_iot_twinmaker eclipse_ditto eclipse_basyx aas fiware thingsboard node_red grafana influxdb prometheus loki tempo opentelemetry elasticsearch opensearch timescaledb postgresql duckdb clickhouse mongodb redis kafka nats rabbitmq''',
    'energy-power': '''pybamm sam_nrel p ypsa pandapower gridlabd opendss matpower powermodels_jl powerworld psse digsilent_powerfactory modelica_buildings trnsys esp_r city_energy_analyst'''.replace('p ypsa','pypsa'),
    'gis-environment': '''qgis gdal grass_gis saga_gis postgis geopandas rasterio xarray cartopy google_earth_engine cesium opentopography whitetools wrf mpas cesm geos_chem opendrift parcels delft3d telemac swmm epanet hec_ras modflow flopy''',
    'materials-databases': '''materials_project nomad aflow oqmd optimade matminer atomate2 fireworks pymatgen ase phonopy phono3py wannier90 vasp abinit gpaw siesta yambo dftb_plus gulp raspa zeopp''',
    'bioinformatics': '''ncbi pubmed pmc entrez uniprot pdb alphafold_db ensembl gene_ontology kegg reactome chembl drugbank open_targets clinicaltrials geo sra tcga gnomad string interpro pfam blast hmmer clustal_omega mafft bowtie2 bwa samtools bcftools gatk star salmon cellranger scanpy seurat biopython mdtraj openfold alphafold colabfold autodock_vina gnina rosetta''',
    'lab-automation': '''hamilton_venus tecan beckman_biomek agilent_vworks thermo_momentum autoprotocol pylabrobot sila2 labop pamlabrad bluesky ophyd doocs ni_daqmx labview''',
    'research-data': '''arxiv openalex crossref semantic_scholar europe_pmc core unpaywall orcid datacite zenodo figshare osf dryad dataverse mendeley paperpile overleaf latex pandoc quarto typst nasa_pds nasa_earthdata noaa copernicus usgs cern_open_data huggingface kaggle''',
    'hpc-workflow': '''slurm pbs_pro openpbs lsf htcondor kubernetes docker singularity apptainer mpi openmpi mpich ray dask parsl fireworks pegasus nextflow snakemake cromwell airflow prefect''',
    'ml-experiment': '''pytorch jax tensorflow deepspeed megatron_lm nemo pytorch_lightning hydra mlflow weights_biases tensorboard ray_tune dvc clearml kubeflow onnx tensorrt''',
}

def main():
    out={}
    for category, raw in GROUPS.items():
        for name in raw.split():
            out[name]={
                'category':category,
                'source':f'https://github.com/search?q={name}+MCP&type=repositories',
                'prerequisites':[f'Install or configure {name}', 'Install or implement an MCP bridge'],
                'availability':'candidate_wrapper',
                'server':{'command':f'{name}-mcp','args':[]},
            }
    path=Path(__file__).parents[1]/'ai4sci_bench/data/science_mcp_catalog_additional2.json'
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(len(out))
if __name__=='__main__': main()

# Data provenance

REVEAL uses public reference data only. It uses no patient data and no restricted data.

`scripts/setup_database.py` downloads the files below into `src/database/data/`. Then it loads them into the SQLite database `src/database/gene_database.sqlite`. Git does not track the files or the database. The database table `metadata` records the source, the release label, the download URL, the SHA-256 hash, the record count and the load time for each loaded source.

## Downloaded files

The values below are for the database that was built on 2026-08-04 (the load time is 2026-08-04 01:52 UTC).

| File | Source and release | Download URL | SHA-256 |
|------|--------------------|--------------|---------|
| `gencode.v49.annotation.gtf.gz` | GENCODE human, release 49 | https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_49/gencode.v49.annotation.gtf.gz | `d6e6fe0515c95b2a8cd36a853c1989cee9115c736c60237c56ae92b9daaaf7c4` |
| `go-basic.obo` | Gene Ontology, `data-version: releases/2026-06-15` | http://current.geneontology.org/ontology/go-basic.obo | `c72fc198a86983d55e43aac585d1ffdbeb6e3601475b3f18b6045acdc0a0734c` |
| `goa_human.gaf.gz` | GO human annotations (GAF 2.2), `date-generated: 2026-05-21` | http://current.geneontology.org/annotations/goa_human.gaf.gz | `db472faff1785878521693af62646546cea6af4a386609dd01c72c0554a46a30` |
| `GTEx_gene_median_tpm.gct.gz` | GTEx v8, median TPM for each gene in 54 tissues (RNA-SeQC v1.1.9) | https://storage.googleapis.com/adult-gtex/bulk-gex/v8/rna-seq/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz | `ee7201ff2f280b0de5657d4b08e9a240362d9757efed7f7bd5dba35a5f8617b8` |
| `9606.protein.info.v12.0.txt.gz` | STRING v12.0, human protein information | https://stringdb-downloads.org/download/protein.info.v12.0/9606.protein.info.v12.0.txt.gz | `144de4b0d98c6a7dfde6ddc2591cf88657f27b989eadff4f501450c3ed1f0f1c` |
| `9606.protein.links.v12.0.txt.gz` | STRING v12.0, human protein interactions | https://stringdb-downloads.org/download/protein.links.v12.0/9606.protein.links.v12.0.txt.gz | `3e22f32572211aa341d5b4bd08d30c32e693e294603202120936872f87719d4f` |
| `9606.protein.aliases.v12.0.txt.gz` | STRING v12.0, human protein aliases | https://stringdb-downloads.org/download/protein.aliases.v12.0/9606.protein.aliases.v12.0.txt.gz | `b65f730b993ed0c1bd72edf4565d3d425db42861101b29699704810e8f125680` |
| `Homo_sapiens.gene_info.gz` | NCBI Gene, human gene information, downloaded 2026-08-04 | https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz | `a4460d2e51ed264d515f10b0cf72e7fa33d5b4053cf2cfdc160f77c1c52e3946` |

The record counts in the `metadata` table are: GENCODE 78,691, NCBI 41,143, GO 855,293, GTEx 1,530,270 and STRING 1,858,944.

## Known provenance issues

- The GO and NCBI Gene URLs point to the current release. A new download can give different data. To identify the data, use the version lines and the hashes above.
- `scripts/setup_database.py` labels GO and NCBI Gene as release `2025-01`. The `metadata` table copies this label. The label does not agree with the downloaded files, which are from 2026.
- If a GO download fails, the script uses fallback URLs. One fallback is the fixed GO release `2024-01-17`. The `metadata` table records the primary URL only, so the table does not show if a fallback was used. For this build, the `go-basic.obo` version line confirms the 2026-06-15 release.

## Data used at run time

REVEAL queries PubMed through the NCBI E-utilities API during each run. The paper metadata and abstracts are saved in `state.json` in each run directory under `results/`. The PubMed results change over time, so a repeated run can find different papers.

The pipeline sends the gene data and the PubMed text to the OpenAI API for interpretation. All of this data is public.

## Terms of use

Check the current terms at each source before you share the data or the results.

| Source | Terms |
|--------|-------|
| GENCODE | Free use. Refer to https://www.gencodegenes.org/pages/data_access.html |
| Gene Ontology | CC BY 4.0. Refer to https://geneontology.org/docs/go-citation-policy/ |
| GTEx | Open-access summary data. Refer to the GTEx Portal, https://gtexportal.org/ |
| STRING | CC BY 4.0. Refer to https://string-db.org/cgi/access |
| NCBI Gene and PubMed | NCBI usage policies. Refer to https://www.ncbi.nlm.nih.gov/home/about/policies/. Some abstracts have publisher copyright. |

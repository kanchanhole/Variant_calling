# Variant Annotation

This software program annotates genetic variants with various pieces of information using the Variant Effect Predictor (VEP) API and input variant data.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)

## Usage

1. Clone the repository or download the source code.
2. Install the required dependencies:
  pip install requests
4. Prepare your input file containing the variants. The file should be in tab-separated format with the following columns: 
  #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT sample
5. Update the `input_file` and `output_file` variables in the script with the appropriate filenames or paths.
6. Run the script:
python annotate_variants.py
This will annotate each variant in the input file and write the annotated variants to the specified output file.
8. The annotated variants will be written to the output file in tab-separated format, including the additional annotations. The output file will have the following columns: #CHROM POS ID REF ALT QUAL FILTER INFO FORMAT sample Depth Reads Percentage Gene Variant_Type Variant_Effect
## Notes

- The script uses the VEP API to retrieve gene information, variant type, and variant effect. Make sure you have a stable internet connection for successful API calls.

- The script assumes that the required API endpoint (`https://rest.ensembl.org/vep/human/hgvs`) is accessible.

- Additional annotations can be added by modifying the `annotate_variant` function according to your requirements.

- Feel free to customize the script or integrate it into your own pipeline as needed.







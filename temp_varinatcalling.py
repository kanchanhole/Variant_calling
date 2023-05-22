"""Module providingFunction printing python version."""
import requests
# Function to parse the INFO field and extract relevant information
def parse_info_field(info):
    """
    Parses the INFO field of a VCF record and extracts relevant information into a dictionary.

    Args:
        info (str): The INFO field string.

    Returns:
        dict: A dictionary containing the parsed INFO field information.
    """
    info_dict = {}
    fields = info.split(';')
    for field in fields:
        if '=' in field:
            key, value = field.split('=')
            info_dict[key] = value
    return info_dict
# Function to annotate a variant
def annotate_variant(variant_line):
    """
    Annotates a variant with relevant information.

    Args:
        variant_line (str): The VCF variant record.

    Returns:
        dict: A dictionary containing the annotated variant information.
    """
    # Extract relevant information from the VCF record
    fields = variant_line.strip().split('\t')
    chrom, pos, _, ref, alt, _, _, info, *_ = fields
    # Initialize info_dict within the annotate_variant function
    info_dict = parse_info_field(info)
    # 1. Depth of sequence coverage
    depth = info_dict.get('DP')
    # 2. Number of reads supporting the variant
    num_reads = info_dict.get('AD')
    if num_reads:
        num_reads = num_reads.split(',')[1]  # Assuming the format is "ref_reads,alt_reads"
    # 3. Percentage of reads supporting the variant versus reference reads
    percentage = info_dict.get('AF')
    # 4. Using VEP API to get gene, type of variation, and effect
    vep_url = f"https://rest.ensembl.org/vep/human/hgvs/{chrom}:{pos}:{ref}:{alt}?"
    response = requests.get(vep_url, headers={"Content-Type": "application/json"},timeout=10)
    if response.status_code == 200:
        vep_data = response.json()
        if vep_data:
            gene = vep_data[0].get('gene_symbol')
            variation_type = vep_data[0].get('variant_class')
            effect = vep_data[0].get('most_severe_consequence')
        else:
            gene = "N/A"
            variation_type = "N/A"
            effect = "N/A"
    else:
        gene = "N/A"
        variation_type = "N/A"
        effect = "N/A"
    # 5. Minor allele frequency (if available)
    maf = info_dict.get('MAF')
    # 6. Additional annotations (add relevant information here)
    additional_annotations = {
        # Add relevant annotations here
    }
    # Return the annotated variant as a dictionary
    annotated_variant = {
        'Chromosome': chrom,
        'Position': pos,
        'Ref': ref,
        'Alt': alt,
        'Depth': depth,
        'NumReads': num_reads,
        'Percentage': percentage,
        'Gene': gene,
        'Type': variation_type,
        'Effect': effect,
        'MAF': maf,
        'AdditionalAnnotations': additional_annotations
    }
    return annotated_variant
# Read the VCF file
with open('test_vcf_data.txt', 'r',encoding='UTF-8') as file:
    vcf_data = file.readlines()
# Remove header lines if present
vcf_data = [line for line in vcf_data if not line.startswith('#')]
# Annotate each variant in the VCF file
annotated_variants = []
for variant in vcf_data:
    annotated_variants.append(annotate_variant(variant))
# Open the output file for writing
output_file = open('annotated_variants.vcf', 'w',encoding='UTF-8')
# Write the annotated variants to the output file
for variant in annotated_variants:
    output_file.write(variant + '\n')
# Close the output file
output_file.close()

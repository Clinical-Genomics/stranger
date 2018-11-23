def print_headers(vcf_obj, outfile=None, silent=False):
    """
    Print the vcf headers.
    
    If a result file is provided headers will be printed here, otherwise
    they are printed to stdout.
    
    Args:
        vcf_obj (cyvcf2.VCF)
        outfile (FileHandle): A file handle
        silent (Bool): If nothing should be printed.
        
    """
    for header_line in vcf_obj.raw_header.split('\n'):
        if len(header_line)>0:
            if outfile:
                outfile.write(header_line+'\n')
            else:
                if not silent:
                    print(header_line)
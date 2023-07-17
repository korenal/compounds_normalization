"""This is program for name normalization of chemical compounds. It accepts at the entrance names of compounds and \
returns an excel file with two columns: org_form and norm_form and with the compound's properties."""
from pubchempy import *
import xlsxwriter
import sys

compounds_file = xlsxwriter.Workbook('compounds.xlsx')
worksheet = compounds_file.add_worksheet()
worksheet.set_column(0, 3, 18)


def get_normalized_form(compound_name: str) -> str:
    """Gets the normalized name of the compound name."""
    return get_synonyms(compound_name, 'name')[0]['Synonym'][0]


def get_cid_number(compound_name: str) -> str:
    """Gets the CID number of the compound name."""
    return get_synonyms(compound_name, 'name')[0]['CID']


def get_property(property_type: str, cid_number: int):
    """Gets the property type of the compound name."""
    return get_properties(property_type, cid_number)[0][property_type]


def write_to_excel_file(list_of_items: [], column: int) -> None:
    """Writes rows into excel file."""
    row = 1
    for item in list_of_items:
        worksheet.write(row, column, item)
        row += 1


# Preprocessing
org_forms = list(sys.argv[1][1:-1].split(','))
cid_numbers = []
norm_forms = []

for org_form in org_forms:
    norm_forms.append(get_normalized_form(org_form).upper())
    cid_numbers.append(get_cid_number(org_form))

# Header in excel sheet
row = 1
data_cols = ['org_form', 'norm_form', 'canonical_smiles', 'logP', '', 'Molecular weight']
header_format = compounds_file.add_format({
    'bold': True,
    'font_name': 'Arial',
    'font_size': 10,
    'text_wrap': True,
    'center_across': True,
    'valign': 'bottom',
    'border': 1})
column = 0
for x in range(0, len(data_cols)):
    worksheet.write(0, column, data_cols[x], header_format)
    column += 1

write_to_excel_file(org_forms, 0)
write_to_excel_file(norm_forms, 1)

# Get properties
canonical_smiles = []
logPs = []
molecular_weights = []

for cid_number in cid_numbers:
    canonical_smiles.append(get_property('CanonicalSMILES', cid_number))
    logPs.append(get_property('XLogP', cid_number))
    molecular_weights.append(get_property('MolecularWeight', cid_number))

write_to_excel_file(canonical_smiles, 2)
write_to_excel_file(logPs, 3)
write_to_excel_file(molecular_weights, 5)

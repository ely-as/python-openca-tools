import json
from pathlib import Path
import re
from typing import List

from bs4 import BeautifulSoup

from openca_tools import utils

RE_VALUE = re.compile(r'(?:concept=")(\w+)(?:" value=")(\d+)')
RE_OBSVALUE = re.compile(r'(?:value=")(\d+)')


def create(input_fp: Path) -> None:
    # Find structure file
    structure_fp = (
        input_fp.parent / input_fp.name.replace('Generic', 'Structure')
    )
    # Confirm the input files exist
    if not input_fp.exists():
        raise FileNotFoundError(f"Could not find file {input_fp.name}")
    if not structure_fp.exists():
        raise FileNotFoundError(f"Could not find file {structure_fp.name}")
    # Output filepaths
    dataset_name = input_fp.name.lstrip('Generic_').rstrip('.xml')
    output_csv_fp = input_fp.parent / f'{dataset_name}.csv'
    output_json_fp = input_fp.parent / f'{dataset_name}.json'
    # Process files
    codes_dict = get_codes_dict_from_structure_file(structure_fp)
    header = get_csv_header_from_structure_file(structure_fp)
    data_dict = create_csv_file_from_sdmx_xml_file(
        input_fp, output_csv_fp, header
    )
    # Create JSON metadata file
    with open(output_json_fp, 'w') as f:
        json.dump({'data': data_dict, 'codes': codes_dict}, f, indent=4)
    # Create checksum sidecar files
    utils.create_checksum_sidecar_file(output_csv_fp, 'sha256')
    utils.create_checksum_sidecar_file(output_json_fp, 'sha256')


def get_codes_dict_from_structure_file(input_fp: Path) -> dict:
    with open(input_fp, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
    lang_set = set(
        e.attrs['xml:lang'] for e in soup.find_all(attrs={'xml:lang': True})
    )
    codes_dict: dict = {lang: {} for lang in lang_set}
    for code_list in soup.find_all('structure:CodeList'):
        id = code_list.attrs['id']
        for lang in lang_set:
            codes_dict[lang][id] = {}
        for code in code_list.find_all('structure:Code'):
            value = code.attrs['value']
            for description in code.find_all('structure:Description'):
                lang = description.attrs.get('xml:lang')
                if lang:
                    codes_dict[lang][id][value] = description.text.strip()
                else:
                    for lang in lang_set:
                        codes_dict[lang][id][value] = description.text.strip()
    return {'lang': codes_dict}


def get_csv_header_from_structure_file(fp: Path) -> List[str]:
    with open(fp, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
    dimensions = soup.find_all('structure:Dimension')
    header = [d.attrs['conceptRef'] for d in dimensions]
    if soup.find(
        'structure:PrimaryMeasure', attrs={'conceptRef': 'OBS_VALUE'}
    ):
        header += ['OBS_VALUE']
    return header


def create_csv_file_from_sdmx_xml_file(
    input_fp: Path, output_fp: Path, header: List[str]
) -> dict:
    lines_written = 0
    try:
        output_file = open(output_fp, 'a')
        output_file.truncate(0)
        _ = output_file.write(','.join(header) + '\n')
        lines_written += 1
        with open(input_fp, 'r') as input_file:
            data = {}
            for num, line in enumerate(input_file, 1):
                if '<generic:Value ' in line:
                    search = re.search(RE_VALUE, line)
                    if search:
                        data[search.group(1)] = search.group(2)
                elif '<generic:ObsValue ' in line:
                    search = re.search(RE_OBSVALUE, line)
                    if search:
                        data['OBS_VALUE'] = search.group(1)
                elif '</generic:Series>' in line:
                    csv_line = ','.join(data[_] for _ in header)
                    _ = output_file.write(csv_line + '\n')
                    lines_written += 1
                    data = {}
    finally:
        output_file.close()
    return {'filename': output_fp.name, 'lines': lines_written}

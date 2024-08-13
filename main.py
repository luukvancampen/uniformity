from helpers.general_helpers import files_to_tables
from uniformity import compute_structural_semantic_uniformity, compute_high_level_syntactic_uniformity, compute_low_level_syntactic_uniformity, \
    compute_high_level_semantic_uniformity, compute_low_level_semantic_uniformity, compute_structural_syntactic_uniformity


if __name__ == '__main__':
    print("Uniformity!")

    tables = files_to_tables("./input/")
    columns = []
    for table in tables:
        columns.extend(table.columns)

    # ________________________________________________
    print(f'High level syntactic: {compute_high_level_syntactic_uniformity(tables)}')
    print(f'Low level syntactic: {compute_low_level_syntactic_uniformity(columns)}')
    print(f'High level semantic: {compute_high_level_semantic_uniformity(tables)}')
    print(f'Low level semantic: {compute_low_level_semantic_uniformity(tables)}')
    print(f'high level syntactic: {compute_high_level_syntactic_uniformity(tables)}')
    print(f'structural syntactic: {compute_structural_syntactic_uniformity(columns)}')
    print(f'Structural semantic: {compute_structural_semantic_uniformity(columns)}')
    # ________________________________________________

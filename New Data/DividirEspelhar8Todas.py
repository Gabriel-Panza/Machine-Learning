import nibabel as nib
import numpy as np
import os
import SimpleITK as sitk

# Caminho do arquivo NIfTI original
folders = [
    "sub-00H10", "sub-02A13", "sub-03C08", "sub-06C09", "sub-14F04",
    "sub-16E03", "sub-16G09", "sub-16I12", "sub-19F09", "sub-19G04",
    "sub-22F14", "sub-25B08", "sub-26B09", "sub-29D03", "sub-31F07",
    "sub-34J06", "sub-35E12", "sub-36K02", "sub-41D08", "sub-42B05",
    "sub-44H05", "sub-51C05", "sub-52K04", "sub-54K08", "sub-56E13",
    "sub-57D04", "sub-59E09", "sub-59G00", "sub-60G06", "sub-60K04",
    "sub-71C07", "sub-72I02", "sub-72K02", "sub-76E02", "sub-76J09",
    "sub-79H07", "sub-83K08", "sub-85I05", "sub-86G08",
    "sub-87G01", "sub-89A03", "sub-90K10"
]
for name in folders:
    # Lista de caminhos de arquivo possíveis
    file_patterns = [
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-vol_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-vbm_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-mpr_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-mpr_run-01_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-vol_run-01_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-01/anat/{name}_ses-01_acq-posgado_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-02/anat/{name}_ses-02_acq-vol_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-02/anat/{name}_ses-02_acq-vbm_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-02/anat/{name}_ses-02_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-02/anat/{name}_ses-02_acq-mpr_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz",
        "Patients_Displasya/{name}/ses-02/anat/{name}_ses-02_acq-posgado_desc-reg_desc-biascorr_desc-brainext_T1w.nii.gz"
    ]
    img = None
    for pattern in file_patterns:
        file_path = pattern.format(name=name)
        try:
            img = nib.load(file_path)
            print(f"Carregado com sucesso: {file_path}")
            break
        except FileNotFoundError:
            continue
    
    if img is None:
        print(f"Nenhum arquivo encontrado para o paciente: {name}")
        exit(1)
    
    data = img.get_fdata()

    # Definir o limite para considerar os pixels não pretos
    non_black_threshold = 0.1 / 255 
    # Definir a porcentagem mínima de pixels não pretos para exibir a imagem
    min_percentage_non_black = 0.2

    # Contador para acompanhar quantas fatias foram processadas
    processed_slices = 0

    # Diretório de saída para salvar as fatias
    output_dir_left = os.path.join(f"Contralateral/{name}", "left")
    output_dir_right = os.path.join(f"Contralateral/{name}", "right")
    output_dir_lesion_left = os.path.join(f"Contralateral/{name}", "lesion_left")
    output_dir_lesion_right = os.path.join(f"Contralateral/{name}", "lesion_right")
    os.makedirs(output_dir_left, exist_ok=True)
    os.makedirs(output_dir_right, exist_ok=True)
    os.makedirs(output_dir_lesion_left, exist_ok=True)
    os.makedirs(output_dir_lesion_right, exist_ok=True)

    # Carregar a máscara de lesão NRRD
    file_patterns_lesion = [
        "Patients_Displasya/{name}/ses-01/anat/{name} Label FLAIR Questionvel.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label FLAIR.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label ses-01 FLAIR.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label ses-02 FLAIR.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label T1.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label ses-01 T1.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label ses-02 T1.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} Label T2.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} Label FLAIR Questionvel.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} Label FLAIR.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} Label T1.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} Label T2.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} FLAIR Label.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} T1 Label.seg.nrrd",
        "Patients_Displasya/{name}/ses-01/anat/{name} T2 Label.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} FLAIR Label.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} T1 Label.seg.nrrd",
        "Patients_Displasya/{name}/ses-02/anat/{name} T2 Label.seg.nrrd"
    ]
    lesion_mask = None
    for pattern in file_patterns_lesion:
        lesion_mask_path = pattern.format(name=name)
        try:
            lesion_mask = sitk.ReadImage(lesion_mask_path)
            lesion_data = sitk.GetArrayFromImage(lesion_mask)            
            print(f"Carregado com sucesso: {lesion_mask_path}")
            break
        except:
            continue
    
    if lesion_mask is None:
        print(f"Nenhum arquivo de label encontrado para o paciente: {name}")
        exit(1)

    # Loop para cada fatia axial
    for slice_idx in range(data.shape[2]):
        # Pega a lesão da fatia inteira
        lesion_slice_data = np.transpose(lesion_data, (0, 2, 1))[slice_idx, :, :]
        
        # Rotacionar a fatia em -90 graus
        rotated_lesion_slice = np.rot90(lesion_slice_data, k=-1)
        
        # Contar o número total de pixels
        total_pixels_lesion = rotated_lesion_slice.size
        
        # Contar o número de pixels que são considerados não pretos
        non_black_pixels_lesion = np.sum(rotated_lesion_slice > non_black_threshold)

        # Calcular a porcentagem de pixels não pretos
        percentage_non_black_lesion = non_black_pixels_lesion / total_pixels_lesion
        
        # Selecionar a fatia axial atual
        slice_data = data[:, :, slice_idx]
        
        # Rotacionar a fatia em -90 graus
        rotated_slice = np.rot90(slice_data, k=-1)
        
        # Contar o número total de pixels
        total_pixels = rotated_slice.size
        # Contar o número de pixels que são considerados não pretos
        non_black_pixels = np.sum(rotated_slice > non_black_threshold)

        # Calcular a porcentagem de pixels não pretos
        percentage_non_black = non_black_pixels / total_pixels

        # Se a porcentagem de pixels não pretos for maior que 20%, processar a fatia
        if percentage_non_black > min_percentage_non_black:
            output_dir_left_slice = os.path.join(output_dir_left, f"Slice{slice_idx}/")
            output_dir_right_slice = os.path.join(output_dir_right, f"Slice{slice_idx}/")
    
            os.makedirs(output_dir_left_slice, exist_ok=True)
            os.makedirs(output_dir_right_slice, exist_ok=True)
            
            processed_slices += 1
        
            # Dividir a fatia rotacionada em esquerda e direita
            midpoint = rotated_slice.shape[1] // 2
            left_half = rotated_slice[:, :midpoint]
            right_half = rotated_slice[:, midpoint:]

            # Inverter horizontalmente o lado direito
            right_half_flipped = np.fliplr(right_half)

            # Dividir as metades esquerda e direita horizontalmente em duas partes
            horizontal_mid_left = left_half.shape[0] // 2
            horizontal_mid_right = right_half_flipped.shape[0] // 2
            left_top = left_half[:horizontal_mid_left, :]
            left_bottom = left_half[horizontal_mid_left:, :]
            right_top = right_half_flipped[:horizontal_mid_right, :]
            right_bottom = right_half_flipped[horizontal_mid_right:, :]

            # Dividir cada quadrante em 2 subquadrantes (totalizando 8 divisões)
            left_top_left = left_top[:, :left_top.shape[1] // 2]
            left_top_right = left_top[:, left_top.shape[1] // 2:]
            left_bottom_left = left_bottom[:, :left_bottom.shape[1] // 2]
            left_bottom_right = left_bottom[:, left_bottom.shape[1] // 2:]
            right_top_left = right_top[:, :right_top.shape[1] // 2]
            right_top_right = right_top[:, right_top.shape[1] // 2:]
            right_bottom_left = right_bottom[:, :right_bottom.shape[1] // 2]
            right_bottom_right = right_bottom[:, right_bottom.shape[1] // 2:]

            # Lista com todas as subimagens e identificações
            subimages = [
                (left_top_left, "left_top_left"),
                (left_top_right, "left_top_right"),
                (left_bottom_left, "left_bottom_left"),
                (left_bottom_right, "left_bottom_right"),
                (right_top_left, "right_top_left"),
                (right_top_right, "right_top_right"),
                (right_bottom_left, "right_bottom_left"),
                (right_bottom_right, "right_bottom_right"),
            ]

            # Salvar cada subimagem como um arquivo NIfTI separado
            for subimage, position in subimages:
                # Definir o diretório de saída com base na posição
                if position.startswith("left"):
                    output_path = os.path.join(output_dir_left_slice, f"{position}.nii.gz")
                else:
                    output_path = os.path.join(output_dir_right_slice, f"{position}.nii.gz")

                # Converter o array numpy para um objeto NIfTI
                subimage_nii = nib.Nifti1Image(subimage, affine=np.eye(4))
                
                # Salvar o arquivo NIfTI
                nib.save(subimage_nii, output_path)
            
            output_dir_lesion_left_slice = os.path.join(output_dir_lesion_left, f"Slice{slice_idx}")
            output_dir_lesion_right_slice = os.path.join(output_dir_lesion_right, f"Slice{slice_idx}")
            
            os.makedirs(output_dir_lesion_left_slice, exist_ok=True)
            os.makedirs(output_dir_lesion_right_slice, exist_ok=True)
            
            # Dividir a fatia rotacionada em esquerda e direita
            midpoint_lesion = rotated_lesion_slice.shape[1] // 2
            left_half_lesion = rotated_lesion_slice[:, :midpoint_lesion]
            right_half_lesion = rotated_lesion_slice[:, midpoint_lesion:]

            # Inverter horizontalmente o lado direito
            right_half_lesion_flipped = np.fliplr(right_half_lesion)

            # Dividir as metades esquerda e direita horizontalmente em duas partes
            horizontal_mid_left_lesion = left_half_lesion.shape[0] // 2
            horizontal_mid_right_lesion = right_half_lesion_flipped.shape[0] // 2
            left_top_lesion = left_half_lesion[:horizontal_mid_left_lesion, :]
            left_bottom_lesion = left_half_lesion[horizontal_mid_left_lesion:, :]
            right_top_lesion = right_half_lesion_flipped[:horizontal_mid_right_lesion, :]
            right_bottom_lesion = right_half_lesion_flipped[horizontal_mid_right_lesion:, :]

            # Dividir cada quadrante em 2 subquadrantes (totalizando 8 divisões)
            left_top_left_lesion = left_top_lesion[:, :left_top_lesion.shape[1] // 2]
            left_top_right_lesion = left_top_lesion[:, left_top_lesion.shape[1] // 2:]
            left_bottom_left_lesion = left_bottom_lesion[:, :left_bottom_lesion.shape[1] // 2]
            left_bottom_right_lesion = left_bottom_lesion[:, left_bottom_lesion.shape[1] // 2:]
            right_top_left_lesion = right_top_lesion[:, :right_top_lesion.shape[1] // 2]
            right_top_right_lesion = right_top_lesion[:, right_top_lesion.shape[1] // 2:]
            right_bottom_left_lesion = right_bottom_lesion[:, :right_bottom_lesion.shape[1] // 2]
            right_bottom_right_lesion = right_bottom_lesion[:, right_bottom_lesion.shape[1] // 2:]

            # Lista com todas as subimagens e identificações
            subimages = [
                (left_top_left_lesion, "left_top_left"),
                (left_top_right_lesion, "left_top_right"),
                (left_bottom_left_lesion, "left_bottom_left"),
                (left_bottom_right_lesion, "left_bottom_right"),
                (right_top_left_lesion, "right_top_left"),
                (right_top_right_lesion, "right_top_right"),
                (right_bottom_left_lesion, "right_bottom_left"),
                (right_bottom_right_lesion, "right_bottom_right"),
            ]

            # Salvar cada subimagem como um arquivo NIfTI separado
            for subimage, position in subimages:
                # Definir o diretório de saída com base na posição
                if position.startswith("left"):
                    output_path_lesion = os.path.join(output_dir_lesion_left_slice, f"{position}.nii.gz")
                else:
                    output_path_lesion = os.path.join(output_dir_lesion_right_slice, f"{position}.nii.gz")

                # Converter o array numpy para um objeto NIfTI
                subimage_nii = nib.Nifti1Image(subimage, affine=np.eye(4))
                
                # Salvar o arquivo NIfTI
                nib.save(subimage_nii, output_path_lesion)
                
    print(f"Total de fatias processadas do paciente {name}: {processed_slices}")
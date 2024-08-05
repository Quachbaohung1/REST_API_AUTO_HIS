import numpy as np


def create_patient():
    A = list(range(24033028, 24033278))
    print(A)
    # Chia danh sách A thành 5 mảng nhỏ
    split_arrays = np.array_split(A, 1)

    # Chuyển các mảng con thành danh sách
    split_lists = [arr.tolist() for arr in split_arrays]

    # In ra các mảng con
    for i, sublist in enumerate(split_lists, 1):
        print(f"patientCodes = {sublist}")


create_patient()

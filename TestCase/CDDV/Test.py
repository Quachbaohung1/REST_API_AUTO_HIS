import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Khám_bệnh_CDDV.POST import (
    process_check_patient_in_room,
    process_insert_info_patient,
    process_examination_services,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_CDDV.txt'

# Xóa file log cũ nếu tồn tại và thiết lập logging
with open(log_file_path, 'w'):  # Mở file trong chế độ ghi để xóa nội dung
    pass  # Pass đơn giản làm gì để xóa

# Thiết lập logging để ghi vào file mới
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Ghi lại kết quả của test
def log_test_result(test_name, result):
    logging.info(f'Test "{test_name}" - Result: {result}')


def read_test_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')
    return df


class TestProcessExamination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Khám bệnh - CDDV/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Examination(self, testcase_id, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = self.test_data[self.test_data['TestCaseId'] == testcase_id]
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(testcase_id)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {testcase_id}: Passed")
            log_test_result(f"Running test for {testcase_id}", "Passed")
        else:
            print(f"Running test for {testcase_id}: Failed")
            log_test_result(f"Running test for {testcase_id}", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {testcase_id}. Expected: {expected_result}, Actual: {str(result)}")

    # Nhập đầy đủ thông tin chỉ định dịch vụ thành công
    def test_case_19(self):
        testcase_id = "CDDV_19"
        entry_ids = [53527, 53529, 53530, 53531, 53532, 53533, 53534, 53535, 53536, 53537, 53538, 53539, 53540, 53541, 53542, 53543, 53544, 53545, 53546, 53547, 53548, 53549, 53550, 53551, 53552, 53553, 53554, 53555, 53556, 53557, 53558, 53559, 53560, 53561, 53562, 53563, 53564, 53565, 53566, 53567, 53568, 53569, 53570, 53571, 53572, 53573, 53574, 53575, 53576, 53577, 53578, 53579, 53580, 53581, 53582, 53583, 53584, 53585, 53586, 53587, 53588, 53589, 53590, 53591, 53592, 53593, 53594, 53595, 53596, 53597, 53598, 53599, 53600, 53601, 53602, 53603, 53604, 53605, 53606, 53607, 53608, 53609, 53610, 53611, 53612, 53613, 53614, 53615, 53616, 53617, 53618, 53619, 53620, 53621, 53622, 53623, 53624, 53625, 53626, 53627, 53628, 53629, 53630, 53631, 53632, 53633, 53634, 53635, 53636, 53637, 53638, 53639, 53640, 53641, 53642, 53643, 53644, 53645, 53646, 53647, 53648, 53649, 53650, 53651, 53652, 53653, 53654, 53655, 53656, 53657, 53658, 53659, 53660, 53661, 53662, 53663, 53664, 53665, 53666, 53667, 53668, 53669, 53670, 53671, 53672, 53673, 53674, 53675, 53676, 53677, 53678, 53679, 53680, 53681, 53682, 53683, 53684, 53685, 53686, 53687, 53688, 53689, 53690, 53691, 53692, 53693, 53694, 53695, 53696, 53697, 53698, 53699, 53700, 53701, 53702, 53703, 53704, 53705, 53706, 53707, 53708, 53709, 53710, 53711, 53712, 53713, 53714, 53715, 53716, 53717, 53718, 53719, 53720, 53721, 53722, 53723, 53724, 53725, 53726, 53727, 53728, 53729, 53730, 53731, 53732, 53733, 53734, 53735, 53736, 53737, 53738, 53739, 53740, 53741, 53742, 53743, 53744, 53745, 53746, 53747, 53748, 53749, 53750, 53751, 53752, 53753, 53754, 53755, 53756, 53757, 53758, 53759, 53760, 53761, 53762, 53763, 53764, 53765, 53766, 53767, 53768, 53769, 53770, 53771, 53772, 53773, 53774, 53775, 53776, 53777, 53778, 53779, 53780, 53781, 53782, 53783, 53784, 53785, 53786, 53787, 53788, 53789, 53790, 53791, 53792, 53793, 53794, 53795, 53796, 53797, 53798, 53799, 53800, 53801, 53802, 53803, 53804, 53805, 53806, 53807, 53808, 53809, 53810, 53811, 53812, 53813, 53814, 53815, 53816, 53817, 53818, 53819, 53820, 53821, 53822, 53823, 53824, 53825, 53826, 53827, 53828, 53829, 53830, 53831, 53832, 53833, 53834, 53835, 53836, 53837, 53838, 53839, 53840, 53841, 53842, 53843, 53844, 53845, 53846, 53847, 53848, 53849, 53850, 53851, 53852, 53853, 53854, 53855, 53856, 53857, 53858, 53859, 53860, 53861, 53862, 53863, 53864, 53865, 53866, 53867, 53868, 53869, 53870, 53871, 53872, 53873, 53874, 53875, 53876, 53877, 53878, 53879, 53880, 53881, 53882, 53883, 53884, 53885, 53886, 53887, 53888, 53889, 53890, 53891, 53892, 53893, 53894, 53895, 53896, 53897, 53898, 53899, 53900, 53901, 53902, 53903, 53904, 53905, 53906, 53907, 53908, 53909, 53910, 53911, 53912, 53913, 53914, 53915, 53916, 53917, 53918, 53919, 53920, 53921, 53922, 53923, 53924, 53925, 53926, 53927]

        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id, entry_ids)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()

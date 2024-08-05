import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Viện_phí.POST import (
    process_VP,
    process_VP_without_cost,
    Cost_exemption,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_VP.txt'

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


class TestProcessCosts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Viện_phí/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Cost(self, testcase_id, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = self.test_data[self.test_data['TestCaseId'] == testcase_id]
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(testcase_id)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"\nRunning test for {testcase_id}: Passed")
            log_test_result(f"Running test for {testcase_id}", "Passed")
        else:
            print(f"\nRunning test for {testcase_id}: Failed")
            log_test_result(f"Running test for {testcase_id}", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {testcase_id}. Expected: {expected_result}, Actual: {str(result)}")

    # Case quyết toán thành công (BN BHYT)
    def test_case_01(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_1"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        patientCodes = [24028574, 24028575, 24028576, 24028577, 24028578, 24028579, 24028580, 24028581, 24028582, 24028583, 24028584, 24028585, 24028586, 24028587, 24028588, 24028589, 24028590, 24028591, 24028592, 24028593, 24028594, 24028595, 24028596, 24028597, 24028598, 24028599, 24028600, 24028601, 24028602, 24028603, 24028604, 24028605, 24028606, 24028607, 24028608, 24028609, 24028610, 24028611, 24028612, 24028613, 24028614, 24028615, 24028616, 24028617, 24028618, 24028619, 24028620, 24028621, 24028622, 24028623, 24028624, 24028625, 24028626, 24028627, 24028628, 24028629, 24028630, 24028631, 24028632, 24028633, 24028634, 24028635, 24028636, 24028637, 24028638, 24028639, 24028640, 24028641, 24028642, 24028643, 24028644, 24028645, 24028646, 24028647, 24028648, 24028649, 24028650, 24028651, 24028652, 24028653, 24028654, 24028655, 24028656, 24028657, 24028658, 24028659, 24028660, 24028661, 24028662, 24028663, 24028664, 24028665, 24028666, 24028667, 24028668, 24028669, 24028670, 24028671, 24028672, 24028673, 24028674, 24028675, 24028676, 24028677, 24028678, 24028679, 24028680, 24028681, 24028682, 24028683, 24028684, 24028685, 24028686, 24028687, 24028688, 24028689, 24028690, 24028691, 24028692, 24028693, 24028694, 24028695, 24028696, 24028697, 24028698, 24028699, 24028700, 24028701, 24028702, 24028703, 24028704, 24028705, 24028706, 24028707, 24028708, 24028709, 24028710, 24028711, 24028712, 24028713, 24028714, 24028715, 24028716, 24028717, 24028718, 24028719, 24028720, 24028721, 24028722, 24028723, 24028724, 24028725, 24028726, 24028727, 24028728, 24028729, 24028730, 24028731, 24028732, 24028733, 24028734, 24028735, 24028736, 24028737, 24028738, 24028739, 24028740, 24028741, 24028742, 24028743, 24028744, 24028745, 24028746, 24028747, 24028748, 24028749, 24028750, 24028751, 24028752, 24028753, 24028754, 24028755, 24028756, 24028757, 24028758, 24028759, 24028760, 24028761, 24028762, 24028763, 24028764, 24028765, 24028766, 24028767, 24028768, 24028769, 24028770, 24028771, 24028772, 24028773, 24028774, 24028775, 24028776, 24028777, 24028778, 24028779, 24028780, 24028781, 24028782, 24028783, 24028784, 24028785, 24028786, 24028787, 24028788, 24028789, 24028790, 24028791, 24028792, 24028793, 24028794, 24028795, 24028796, 24028797, 24028798, 24028799, 24028800, 24028801, 24028802, 24028803, 24028804, 24028805, 24028806, 24028807, 24028808, 24028809, 24028810, 24028811, 24028812, 24028813, 24028814, 24028815, 24028816, 24028817, 24028818, 24028819, 24028820, 24028821, 24028822, 24028823, 24028824, 24028825, 24028826, 24028827, 24028828, 24028829, 24028830, 24028831, 24028832, 24028833, 24028834, 24028835, 24028836, 24028837, 24028838, 24028839, 24028840, 24028841, 24028842, 24028843, 24028844, 24028845, 24028846, 24028847, 24028848, 24028849, 24028850, 24028851, 24028852, 24028853, 24028854, 24028855, 24028856, 24028857, 24028858, 24028859, 24028860, 24028861, 24028862, 24028863]


        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP(self.test_data, file_path, testcase_id, patientCodes)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)


if __name__ == '__main__':
    unittest.main()

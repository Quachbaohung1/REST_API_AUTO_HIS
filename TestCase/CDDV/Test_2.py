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
        entry_ids = [54330, 54331, 54332, 54333, 54334, 54335, 54336, 54337, 54338, 54339, 54340, 54341, 54342, 54343, 54344, 54345, 54346, 54347, 54348, 54349, 54350, 54351, 54352, 54353, 54354, 54355, 54356, 54357, 54358, 54359, 54360, 54361, 54362, 54363, 54364, 54365, 54366, 54367, 54368, 54369, 54370, 54371, 54372, 54373, 54374, 54375, 54376, 54377, 54378, 54379, 54380, 54381, 54382, 54383, 54384, 54385, 54386, 54387, 54388, 54389, 54390, 54391, 54392, 54393, 54394, 54395, 54396, 54397, 54398, 54399, 54400, 54401, 54402, 54403, 54404, 54405, 54406, 54407, 54408, 54409, 54410, 54411, 54412, 54413, 54414, 54415, 54416, 54417, 54418, 54419, 54420, 54421, 54422, 54423, 54424, 54425, 54426, 54427, 54428, 54429, 54430, 54431, 54432, 54433, 54434, 54435, 54436, 54437, 54438, 54439, 54440, 54441, 54442, 54443, 54444, 54445, 54446, 54447, 54448, 54449, 54450, 54451, 54452, 54453, 54454, 54455, 54456, 54457, 54458, 54459, 54460, 54461, 54462, 54463, 54464, 54465, 54466, 54467, 54468, 54470, 54471, 54472, 54473, 54474, 54475, 54476, 54477, 54478, 54479, 54480, 54481, 54482, 54483, 54484, 54485, 54486, 54487, 54488, 54489, 54490, 54491, 54492, 54493, 54494, 54495, 54496, 54497, 54498, 54499, 54500, 54501, 54502, 54503, 54504, 54505, 54506, 54507, 54508, 54509, 54510, 54511, 54512, 54513, 54514, 54515, 54516, 54517, 54518, 54519, 54520, 54521, 54522, 54523, 54524, 54525, 54526, 54527, 54528, 54529, 54530, 54531, 54532, 54533, 54534, 54535, 54536, 54537, 54538, 54539, 54540, 54541, 54542, 54543, 54544, 54545, 54546, 54547, 54548, 54549, 54550, 54551, 54552, 54553, 54554, 54555, 54556, 54557, 54558, 54559, 54560, 54561, 54562, 54563, 54564, 54565, 54566, 54567, 54568, 54569, 54570, 54571, 54572, 54573, 54574, 54575, 54576, 54577, 54578, 54579, 54580, 54581, 54582, 54583, 54584, 54585, 54586, 54587, 54588, 54589, 54590, 54591, 54592, 54593, 54594, 54595, 54596, 54597, 54598, 54599, 54600, 54601, 54602, 54603, 54604, 54605, 54606, 54607, 54608, 54609, 54610, 54611, 54612, 54613, 54614, 54615, 54616, 54617, 54618, 54619, 54620, 54621, 54622, 54623, 54624, 54625, 54626, 54627, 54628, 54629, 54630, 54631, 54632, 54633, 54634, 54635, 54636, 54637, 54638, 54639, 54640, 54641, 54642, 54643, 54644, 54645, 54646, 54647, 54648, 54649, 54650, 54651, 54652, 54653, 54654, 54655, 54656, 54657, 54658, 54659, 54660, 54661, 54662, 54663, 54664, 54665, 54666, 54667, 54668, 54669, 54670, 54671, 54672, 54673, 54674, 54675, 54676, 54677, 54678, 54679, 54680, 54681, 54682, 54683, 54684, 54685, 54686, 54687, 54688, 54689, 54690, 54691, 54692, 54693, 54694, 54695, 54696, 54697, 54698, 54699, 54700, 54701, 54702, 54703, 54704, 54705, 54706, 54707, 54708, 54709, 54710, 54711, 54712, 54713, 54714, 54715, 54716, 54717, 54718, 54719, 54720, 54721, 54722, 54723, 54724, 54725, 54726, 54727, 54728, 54729, 54730]


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

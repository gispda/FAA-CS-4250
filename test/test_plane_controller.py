__author__ = 'daemoniclegend'
from mock import *
from plane_controller.plane_ctrl import *
from plane_controller import plane
from io_package.audio import Audio
from computation_package.collision_detection import CollisionDetection
import unittest

'''
.return_value=#Value you want it to equal
.side_effect=[]#irretable thing
.call_count #{returns How times called}
mock_name.assert_called_once_with(name of paremeter)
mock_name.call_args_list =>
                        returns a list of all the parameter that was passed in to the method
                        have to be used with {call(paremater checking)
'''


class TestPlaneController(unittest.TestCase):
    def setUp(self):
        self.plane1_location, plane1_velocity = [0, 0, 0], [100, 100, 100]
        self.plane1_obj = self.plane_helper("0011", self.plane1_location, plane1_velocity)

        self.plane2_location, plane2_velocity = [0, 0, 0], [100, 100, 100]
        self.plane2_obj = self.plane_helper("0012", self.plane2_location, plane2_velocity)

        self.plane3_location, plane3_velocity = [0, 0, 0], [100, 100, 100]
        self.plane3_obj = self.plane_helper("0013", self.plane3_location, plane3_velocity)

        self.plane4_location, plane4_velocity = [0, 0, 0], [100, 100, 100]
        self.plane4_obj = self.plane_helper("0014", self.plane4_location, plane4_velocity)

        self.plane5_location, plane5_velocity = [0, 0, 0], [100, 100, 100]
        self.plane5_obj = self.plane_helper("0015", self.plane5_location, plane5_velocity)
    # patch.object if the method that you are testing is in a class
    @patch.multiple("plane_controller.plane_ctrl",
                    collision_detection_generator=DEFAULT,
                    find_highest_priority_s=DEFAULT,
                    get_corrective_action=DEFAULT,
                    dispatch_collision_alerts=DEFAULT)
    def test_plane_controller_driver(self, collision_detection_generator,
                                     find_highest_priority_s,
                                     get_corrective_action,
                                     dispatch_collision_alerts):
        '''
         This method checks to see if the plane driver calls its correct sequence of commands
        '''
        # 1. collision_detection_generator -> calculates and returns a list of all the planes on a collision course with the PA
        # 2. find_highest_priority -> returns list of 1 or 2 planes
        # 3. corrective action -> String command
        # 4. dispatch event -> sends chris's audio alert

        # action
        plane_controller_driver()
        # assert
        self.assertTrue(collision_detection_generator.call_count > 0)
        self.assertTrue(find_highest_priority_s.call_count > 0)
        self.assertTrue(get_corrective_action.call_count > 0)
        self.assertTrue(dispatch_collision_alerts > 0)

    @patch.multiple("plane_controller.plane_ctrl",
                    convert_to_cartesian_meters=DEFAULT,
                    data_verify=DEFAULT,
                    update_plane_list=DEFAULT)
    def test_input_data(self, convert_to_cartesian_meters
                        , data_verify, update_plane_list):
        '''
        This method test to see if input_data calls its correct methods and follows the correct order
        convert -> data_verify -> update_plane_list
        '''
        # arrange
        # data_in =[id,lat,long,altitude,x,y,z]
        data_in = [10, 111, 222, 2, 0, 1, 0]
        c_t_c = []
        plane_location, plane_velocity = [0, 0, 0], [100, 100, 100]
        plane_obj = self.plane_helper("0011", plane_location, plane_velocity)

        # action
        input_data(data_in)

        # assert
        self.assertEqual(convert_to_cartesian_meters.call_count, 1)
        self.assertEqual(data_verify.call_count, 1)
        self.assertEqual(update_plane_list.call_count, 1)
        convert_to_cartesian_meters.assert_called_once_with(data_in)
        data_verify.assert_called_once_with(c_t_c)
        update_plane_list.assert_called_once_with(plane_obj)

    def test_convert_to_cartesian_meters(self):
        '''
         This method test to see if the latitude longitude and elevation come back in their repsective
         cartesian coordinates
        '''
        original_data1 = ["0013136740", "1163168417", "6561"]
        c_t_c1 = [round(-5944598.358067343, 4), round(-1798356.177876519, 4), round(1449465.324689559,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data1), c_t_c1)

    def test_c_t_c_2(self):
        original_data2 = ["1067118752", "1103679115", "5815"]
        c_t_c2 = [round(-586349.9350400632, 4), round(-2409120.159576062, 4), round(-5875040.710891093, 4)]
        self.assertEquals(convert_to_cartesian_meters(original_data2), c_t_c2)

    def test_c_t_c_3(self):
        original_data3 = ["0000000000","0000000000", "2400"]
        c_t_c3 = [6373400.0, 0.0, 0.0]
        self.assertEquals(convert_to_cartesian_meters(original_data3), c_t_c3)

    def test_c_t_c_4(self):
        original_data4 = ["0054000000", "0122000000", "35"]
        c_t_c4 =  [round(6373400.0,4),round(0.0,4),round(0.0,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data4), c_t_c4)

    def test_c_t_c_5(self):
        original_data5 = ["045000000", "045000000", "2400"]
        c_t_c5 =  [round(3186700.0000000005,4),round(3186700.0,4),round(4506674.359214341,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data5), c_t_c5)

    def test_c_t_c_6(self):
        original_data6 = ["0045000000", "1000000000", "2400"]
        c_t_c6 =  [round(4506674.359214342,4),round(0.0,4),round(4506674.359214341,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data6), c_t_c6)

    def test_c_t_c_7(self):
        original_data7 = ["1090000000", "0450000000", "2400"]
        c_t_c7 =  [round(0.0,4),round(0.0,4),round(-6373400.0,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data7), c_t_c7)

    def test_c_t_c_8(self):
        original_data8 = ["0000000000", "0000000000", "35"]
        c_t_c8 =  [round(6371035.0,4),round(0.0,4),round(-6373400.0,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data8), c_t_c8)

    def test_c_t_c_9(self):
        original_data9 = ["0090000000", "0450000000", "35"]
        c_t_c9 =  [round(0.0,4),round(0.0,4),round(6371035.0,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data9), c_t_c9)

    def test_c_t_c_10(self):
        original_data10 = ["0045000000", "1177000000", "2400"]
        c_t_c10 = [round(-4500498.118632586,4),round(-235861.11206504062,4),round(4506674.359214341,4)]
        self.assertEquals(convert_to_cartesian_meters(original_data10), c_t_c10)


    def test_find_highest_priority_s1(self):
        '''
        These are testing find_highest method. It sends in a list with the 10 closest planes on a collision with the PA.
        It will return a list containing 1 or 2 planes in the same TUC

        '''
        self.plane1_obj.set_tuc_interval()
        data_in1 = [self.plane1_obj,self.plane2_obj,self.plane3_obj,self.plane4_obj,self.plane5_obj]
        data_out1 = []
        self.assertEqual(find_highest_priority_s(data_in1), data_out1)

    def test_find_highest_priority_s2(self):
        self.plane1_obj.set_tuc_interval()
        data_in1 = [self.plane1_obj,self.plane2_obj,self.plane3_obj,self.plane4_obj,self.plane5_obj]
        data_out1 = []
        self.assertEqual(find_highest_priority_s(data_in1), data_out1)

    def test_find_highest_priority_s3(self):

        self.plane1_obj.set_tuc_interval()
        data_in1 = [self.plane1_obj,self.plane2_obj,self.plane3_obj,self.plane4_obj,self.plane5_obj]
        data_out1 = []
        self.assertEqual(find_highest_priority_s(data_in1), data_out1)

    def test_find_highest_priority_s4(self):

        self.plane1_obj.set_tuc_interval()
        data_in1 = [self.plane1_obj,self.plane2_obj,self.plane3_obj,self.plane4_obj,self.plane5_obj]
        data_out1 = []
        self.assertEqual(find_highest_priority_s(data_in1), data_out1)

    def test_find_highest_priority_s5(self):

        self.plane1_obj.set_tuc_interval()
        data_in1 = [self.plane1_obj,self.plane2_obj,self.plane3_obj,self.plane4_obj,self.plane5_obj]
        data_out1 = []
        self.assertEqual(find_highest_priority_s(data_in1), data_out1)

    def test_update_plane_list(self):
        '''
        This is testing to make sure the update_plane_list method updates the global nearby_planes_list.

        '''
        global nearby_planes_list
        nearby_planes_list = []
        plane_location, plane_velocity = [0, 0, 0], [100, 100, 100]
        plane_obj = self.plane_helper("0011", plane_location, plane_velocity)
        update_plane_list(plane_obj)
        list = [plane_obj]
        self.assertEqual(nearby_planes_list, list)

    @patch.object(Audio, "audio_alert")
    def test_dispatch_collision_alerts(self, mock_audio_alert):
        '''
        This method tests to see if dispatch_collision_alerts sends the correct audio alert to the audio class.
        :param mock_audio_alert:
        :return:
        '''
        alert_type = 'climb'
        dispatch_collision_alerts(alert_type)
        mock_audio_alert.assert_called_once_with(alert_type)

    def test_get_corrective_action(self):
        '''
        This method tests get_corrective_action to see if the correct alert is sent to the user
        after it has checked for the 1 or 2 closest planes to avoid.
        '''
        global primary_aircraft
        p_plane_location1, p_plane_velocity1 = [0, 0, 0], [100, 100, 100]
        primary_aircraft = self.plane_helper("0011", p_plane_location1, p_plane_velocity1)
        plane_location1, plane_velocity1 = [0, 0, 0], [100, 100, 100]
        plane_location2, plane_velocity2 = [0, 0, 0], [100, 100, 100]
        plane_obj1 = self.plane_helper("0011", plane_location1, plane_velocity1)
        plane_obj2 = self.plane_helper("0011", plane_location2, plane_velocity2)
        planes_list = [plane_obj1, plane_obj2]
        alert_type = "ASCEND"
        self.assertEqual(get_corrective_action(planes_list), alert_type)

    @patch.object(CollisionDetection,
                  "determine_collision")
    def test_collision_detection_generator(self, mock_determine_collision):
        '''
        This test is check the collision_detection_generator method to see if the correct list is returned of
        all the planes in the area that have a potential collision with the PA

        '''
        global nearby_planes_list
        nearby_planes_list = []
        generated_tested_colided_list = collision_detection_generator()
        true_colided_list = []
        self.assertEqual(mock_determine_collision.call_count, len(nearby_planes_list))
        self.assertEqual(generated_tested_colided_list, true_colided_list)

    # def test_update_transponder_code(self):
    #     pass

    def plane_helper(self, id_code, location_vector, velocity_vector):
        return plane.PlaneObject(id_code,
                                 location_vector[0], location_vector[1], location_vector[2],
                                 velocity_vector[0], velocity_vector[1], velocity_vector[2])


if __name__ == '__main__':
    unittest.main()

# Fussplattenanschluss Stabdübel Anker

import attribute_controller as ac, element_controller as ec, cadwork as c, \
    geometry_controller as gc, utility_controller as uc, connector_axis_controller as cac
from math import floor, ceil

userprofil = uc.get_3d_userprofil_path()
file_path = userprofil + '\\api.x64\\cw_details'
import sys
sys.path.append(file_path)
import geometry as g

STABDUEBEL_DURCHMESSER = 8.
STABDUEBEL_NAME = 'SDü'
STEGPLATTE_NAME = 'FLA'
FUSSPLATTE_NAME = 'FLA'
EINLASS_DUEBEL = 'HSA' 

def main():
    element_ids = ec.get_active_identifiable_element_ids()
    for element_id in element_ids:
        p1 = gc.get_p1(element_id)
        p2 = gc.get_p2(element_id)
        xl_vec = gc.get_xl(element_id)
        yl_vec = gc.get_yl(element_id)
        zl_vec = gc.get_zl(element_id)
        height_column = gc.get_height(element_id)
        width_column = gc.get_width(element_id)

        # ========================================================
        if not check_slope_column(p1,p2):continue
        start_point, end_point = check_z_point(p1, p2)


        local_z_vector = c.point_3d(end_point.x - start_point.x, end_point.y - start_point.y, end_point.z - start_point.z)
        
        local_z_vector = g.vect3_normalized(list_point(local_z_vector))
        print(local_z_vector)
        local_z_vector = c.point_3d(*local_z_vector)
        #=========================================================
        global STABDUEBEL_DURCHMESSER
        
        # Berechnung nach SIA 265 Holzbau 
        stegplatte_length = ceil(STABDUEBEL_DURCHMESSER * 8. / 5.) * 5. + ceil(STABDUEBEL_DURCHMESSER * 1.5 / 5.) * 5.
        print(stegplatte_length)
        dicke_stegplatte = get_thickness_stegplatte(STABDUEBEL_DURCHMESSER)
        start_point = move_point('positive', start_point, dicke_stegplatte, local_z_vector)
        stegplatte = create_stegplatte(height_column, dicke_stegplatte, stegplatte_length, start_point, xl_vec, yl_vec)

        # ========================================================
        # erstelle VBA
        start_point = move_point('positive', start_point, stegplatte_length - 10., local_z_vector)
        point1_vba = move_point('positive', start_point, width_column * 0.5, yl_vec)
        point2_vba = move_point('negative', start_point, width_column * 0.5, yl_vec)

        # hart/weich Verschneidung Platte - Pfosten
        ec.subtract_elements([stegplatte], [element_id])

        sdb = create_standard_vba('Duebel_8', point1_vba, point2_vba)
        
        
    

    return


# =================================================
def check_slope_column(p1, p2, tolerance=.001):
    ''' wenn False dann ...'''
    if abs(p1.x - p2.x) > tolerance:
        print('Stuetze in x-Richtung nicht senkrecht, wurde fuer die Berechnung ignoriert')
        return False
    elif abs(p1.y - p2.y) > tolerance:
        print('Stuetze in y-Richtung nicht senkrecht, wurde fuer die Berechnung ignoriert') 
        return False
    else:
        return True
    

def check_z_point(p1, p2):
    '''Takes in a number n, returns the square of n'''

    if p1.z < p2.z:
        return p1, p2
    else:
        return p2, p1


def create_stegplatte(length, width, height, p1, xl, zl):
    '''
    Erzeug eine Stegplatte
    in double width
    in double thickness
    in double length
    in point_3d p1
    in point_3d x_l
    in point_3d z_l
    '''
    stegplatte = ec.create_rectangular_panel_vectors(length, width, height, p1, xl, zl)
    return stegplatte


def get_thickness_stegplatte(stabduebel_durchmesser):
    ''' '''
    if 8. <= stabduebel_durchmesser <= 10.:
        dicke_stegplatte = 10.
    elif 10. < stabduebel_durchmesser <= 12.:
        dicke_stegplatte = 12.
    elif 12. < stabduebel_durchmesser <= 15.:
        dicke_stegplatte = 15.
    else:
        return

    return dicke_stegplatte


def move_point(operator, point, distance, vector):
    """
    """
                
    return {
        'positive': lambda: c.point_3d(point.x + (vector.x * distance), point.y + (vector.y * distance),
		 point.z + (vector.z * distance)),
        'negative': lambda: c.point_3d(point.x - (vector.x * distance), point.y - (vector.y * distance),
		 point.z - (vector.z * distance)),
    }.get(operator, None)()


def list_point(point_3d):
    return(point_3d.x, point_3d.y, point_3d.z)

def create_standard_vba(name:str, start, end):
    '''erstelle VBA'''
    cac.create_standard_connector(name, start, end)
    


if __name__ == '__main__':
    main()
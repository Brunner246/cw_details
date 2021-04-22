import utility_controller as uc
userprofil = uc.get_3d_userprofil_path()
file_path = userprofil + '\\api.x64\\cw_details'
import sys
sys.path.append(file_path)
import cw_fpsa

cw_fpsa.main()


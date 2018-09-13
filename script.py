import subprocess
import sys
import time
from multiprocessing import Queue, Pool, Manager, cpu_count
from multiprocessing.pool import ThreadPool


NOT_INSTALLED_QUOTES = ['not recognized as an internal or external command']
if sys.platform.find('linux') != -1:
    NOT_INSTALLED_QUOTES = ['not installed', 'No such file or directory']

def install_apk(device_name, apk_address, q=None):
    print("Installing on device {0}".format(device_name))
    t = time.time()
    r = subprocess.run(['adb', '-s', device_name, 'install', '-r', apk_address], capture_output=True)
    o = str(r.stdout)
    if o.find('signatures do not match the previously installed version') != -1:
        print("Previous version with different signature on device {0}. This version of the script can not deal with such problem, You should manually install the package from device and try again".format(device_name))
        '''
        print("Previous version with different signature on device {0}. Will uninstall program and try to install it again".format(device_name))
        m = subprocess.run(['aapt', 'dump', 'badging', package_name], capture_output=True)
        sto = str(m.stdout)
        ster = str(m.stderr)
        for quote in NOT_INSTALLED_QUOTES:
            if ster.find(quote)!=-1 or sto.find(quote) != -1:
                print("Device {0}. You need to install aapt.")
            else:
                print("Device {0}. Finding package name".format(device_name))
                package_i = sto.find('package')
                if package_i != -1:
                    package_name = sto[package_i:sto[package_i:].find("'") + package_i]
                    print("Device {0}. Package name found: {1}".format(device_name, package_name))
                    print("Trying to uninstall package {1} on device {0}".format(device_name, package_name))
                    adbu = subprocess.run(['adb', '-s', device_name,'uninstall', package_name], shell=True, capture_output=True)
                    adbuo = str(adbu.stdout)
                    if adbuo.find('Success') != -1:
                        print("Uninstall completed on device {0}, now installing again.".format(device_name))
                        r = subprocess.run(['adb', '-s', device_name, 'install', '-r', apk_address],shell=True, capture_output=True)
                        o = str(r.stdout)
                    else:
                        print("Device {0}. Could not uninstall package {1}".format(device_name, package_name))
                else:
                    print("Device {0}. Package name not found".format(device_name))
                    print(sto)
       '''

    t = time.time() - t
    print("Device {0}, Time: {1}, Output: {2}".format(device_name, t, o))
    if q:
        q.put((device_name, o))

def get_all_devices():
    r = subprocess.run(['adb', 'devices'], capture_output=True)
    r = str(r.stdout)
    devices = [(t.split("\\")[0], t.split("\\")[1][1:]) for t in r.split("\\n")[1:] if 'device' in t or 'unauthorized' in t]

    return devices

def main():
    oo = subprocess.run(['adb'], shell=True, capture_output=True)
    sto = str(oo.stdout)
    sterr = str(oo.stderr)
    for quote in NOT_INSTALLED_QUOTES:
        if sto.find(quote) != -1 or sterr.find(quote) != -1:
            print("This script does not works withtout ADB, please install it.")
            return -1

    whole_time = time.time()
    apk_address = sys.argv[1] 
    processes = cpu_count() 
    if len(sys.argv) == 3:
        processes = int(sys.argv[2])
    d = [r for r in get_all_devices() if r[1] == 'device']
    if len(d) == 0:
        print("No installable devices found")
        d.append('a')
    #    return -1 
    print("Installing {0} in {1} devices".format(apk_address, len(d)))
    m = Manager()
    #p = Pool(processes=processes)
    p = ThreadPool(processes=processes)
    q = m.Queue()
    
    for i in d:
        t = p.apply_async(install_apk, (i[0], apk_address, q,))
        try:
            t.get(0.000000000000000001)
        except:
            pass
    p.close()
    p.join()
    i = 0
    while i < len(d):
        q.get()
        i += 1

    whole_time = time.time() - whole_time
    print("Whole time {0}".format(whole_time))

if __name__ == "__main__":
   main() 

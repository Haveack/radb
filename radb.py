import subprocess
import sys
import os


def execute(command):
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    return stdout.strip()


def parse_device(line):
    words = line.split()
    if len(words) < 2:
        return None
    elif words[1] == 'device' or words[1] == 'offline':
        id = words[0]
        if words[1] == 'offline':
            online = False
        else:
            online = True
        if online:
            product = words[2][len('product:'):]
            model = words[3][len('model:'):]
            device = words[4][len('device:'):]
            return {
                'id': id,
                'online': online,
                'product': product, 'model': model, 'device': device}
        else:
            return {
                'id': id,
                'online': online,
                'product': None, 'model': None, 'device': None}
    else:
        return None


def parse_devices(text):
    devicelines = text.split(os.linesep)
    devices = []
    for line in devicelines:
        device = parse_device(line)
        if device is not None:
            devices.append(device)
    return devices


def build_cmd(cmd, device):
    if device is None:
        return 'adb ' + cmd
    else:
        return 'adb -s ' + device['id'] + ' ' + cmd


def command_to_device(cmd, device):
    os.system(build_cmd(cmd, device))


def promote_for_device():
    result = execute('adb devices -l')
    devices = parse_devices(result)
    if len(devices) == 0:
        # print 'No connected device'
        # exit()
        return None
    elif len(devices) == 1:
        return devices[0]
    else:
        print 'Please choose deivce:'
        for i in range(0, len(devices)):
            device = devices[i]
            print '%d:' % (i + 1),
            print '%-22s%+8s%+20s' % (
                device['id'],
                'online' if device['online'] else 'offline',
                device['model'])
        index = input()
        return devices[int(index) - 1]


def main():
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        device = promote_for_device()
        redirected_cmd = build_cmd(cmd, device)
        print redirected_cmd
        os.system(redirected_cmd)
    else:
        print 'Please input command'


if __name__ == "__main__":
    main()
